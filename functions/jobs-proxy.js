/**
 * MSBTE Notes & Info - artha.link Public Jobs API Backend Proxy
 * 
 * Requirements & Architecture:
 * - Regional base URL from ARTHA_API_BASE_URL (defaults to https://api-india.artha.link/api/v1)
 * - Auth header: X-API-Key: <ARTHA_API_KEY>
 * - Never log or return the API key.
 * - Allowlist-only query parameter filtering.
 * - Default location=IN when client sends no location, state, or city.
 * - Retry on 502 (up to 2 retries with short backoff).
 * - Edge & in-memory caching: max-age=3600 for /jobs/filters, max-age=60 for /jobs.
 * - 429 Retry-After propagation & X-Request-Id error logging.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

// Lightweight env loader if not already loaded (e.g., in local dev without Netlify CLI)
function loadEnv() {
  if (process.env.ARTHA_API_KEY) return;
  const envCandidates = [
    path.resolve(process.cwd(), '.env'),
    path.resolve(__dirname, '../.env'),
    path.resolve(__dirname, '.env')
  ];
  for (const envPath of envCandidates) {
    if (fs.existsSync(envPath)) {
      try {
        const content = fs.readFileSync(envPath, 'utf8');
        for (const line of content.split(/\r?\n/)) {
          const trimmed = line.trim();
          if (!trimmed || trimmed.startsWith('#')) continue;
          const eqIdx = trimmed.indexOf('=');
          if (eqIdx !== -1) {
            const key = trimmed.slice(0, eqIdx).trim();
            let val = trimmed.slice(eqIdx + 1).trim();
            if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
              val = val.slice(1, -1);
            }
            if (!process.env[key]) {
              process.env[key] = val;
            }
          }
        }
      } catch (err) {
        console.warn('[Proxy Env] Could not load .env file:', err.message);
      }
      break;
    }
  }
}

loadEnv();

function getBaseUrl() {
  return (process.env.ARTHA_API_BASE_URL || 'https://api-india.artha.link/api/v1').replace(/\/+$/, '');
}

// Allowlist for GET /jobs query parameters based on Help Center docs & verified params
const ALLOWED_JOB_PARAMS = [
  'limit',
  'offset',
  'q',
  'location',
  'state',
  'city',
  'categories',
  'job_type',
  'work_mode',
  'sort_by',
  // Verified / supported unverified params
  'niche_keywords',
  'negative_keywords',
  'exp_level',
  'company',
  'salary_min',
  'salary_max',
  'posted_after'
];

// In-memory cache structures (Edge Cache-Control also emitted for Netlify CDN)
const jobsCache = new Map();
const JOBS_CACHE_TTL_MS = 60 * 1000; // 1 minute
const FILTERS_CACHE_TTL_MS = 60 * 60 * 1000; // 60 minutes
let filtersCache = null;

/**
 * Sanitize and validate incoming query parameters according to the allowlist
 * Also enforces the Geolocation rule: defaults location=IN if no location/state/city sent
 */
function sanitizeJobParams(rawQuery) {
  const cleanParams = new URLSearchParams();

  for (const key of ALLOWED_JOB_PARAMS) {
    const rawVal = rawQuery[key];
    if (rawVal === undefined || rawVal === null || rawVal === '') continue;

    const strVal = String(rawVal).trim();
    if (!strVal) continue;

    if (key === 'limit') {
      let num = parseInt(strVal, 10);
      if (isNaN(num) || num < 1) num = 10;
      if (num > 100) num = 100;
      cleanParams.set(key, String(num));
    } else if (key === 'offset') {
      let num = parseInt(strVal, 10);
      if (isNaN(num) || num < 0) num = 0;
      cleanParams.set(key, String(num));
    } else if (key === 'salary_min' || key === 'salary_max') {
      const num = Number(strVal);
      if (!isNaN(num) && num >= 0) {
        cleanParams.set(key, String(num));
      }
    } else if (key === 'job_type') {
      const validTypes = ['full-time', 'part-time', 'contract', 'internship'];
      const normalized = strVal.toLowerCase();
      if (validTypes.includes(normalized)) {
        cleanParams.set(key, normalized);
      }
    } else if (key === 'work_mode') {
      const validModes = ['remote', 'hybrid', 'onsite'];
      const normalized = strVal.toLowerCase();
      if (validModes.includes(normalized)) {
        cleanParams.set(key, normalized);
      }
    } else if (key === 'sort_by') {
      const validSorts = ['most_relevant', 'newest', 'high_cpa'];
      const normalized = strVal.toLowerCase();
      if (validSorts.includes(normalized)) {
        cleanParams.set(key, normalized);
      }
    } else {
      // General strings (q, location, state, city, categories, niche_keywords, negative_keywords, exp_level, company, posted_after)
      cleanParams.set(key, strVal.slice(0, 200));
    }
  }

  // Geolocation gotcha: If no location, state, or city is provided, default to location=IN
  const hasLocation = cleanParams.has('location') && cleanParams.get('location').trim() !== '';
  const hasState = cleanParams.has('state') && cleanParams.get('state').trim() !== '';
  const hasCity = cleanParams.has('city') && cleanParams.get('city').trim() !== '';

  if (!hasLocation && !hasState && !hasCity) {
    cleanParams.set('location', 'IN');
  }

  return cleanParams;
}

/**
 * Fetch helper with automatic 502 retry
 */
async function fetchWithRetry(url, options, maxRetries = 2) {
  let attempt = 0;
  while (true) {
    try {
      const res = await fetch(url, options);
      if (res.status === 502 && attempt < maxRetries) {
        attempt++;
        const delay = attempt * 500;
        console.warn(`[Artha Proxy] 502 Bad Gateway from upstream, retrying in ${delay}ms (attempt ${attempt}/${maxRetries})...`);
        await new Promise(r => setTimeout(r, delay));
        continue;
      }
      return res;
    } catch (err) {
      if (attempt < maxRetries) {
        attempt++;
        const delay = attempt * 500;
        console.warn(`[Artha Proxy] Fetch failed (${err.message}), retrying in ${delay}ms (attempt ${attempt}/${maxRetries})...`);
        await new Promise(r => setTimeout(r, delay));
        continue;
      }
      throw err;
    }
  }
}

/**
 * Handle GET /api/jobs/filters
 */
async function handleFiltersRequest() {
  const now = Date.now();
  if (filtersCache && (now - filtersCache.timestamp < FILTERS_CACHE_TTL_MS)) {
    return {
      status: filtersCache.status,
      headers: { ...filtersCache.headers, 'X-Cache': 'HIT' },
      body: filtersCache.body
    };
  }

  const apiKey = process.env.ARTHA_API_KEY;
  if (!apiKey) {
    console.error('[Artha Proxy Error] Missing ARTHA_API_KEY environment variable');
    return {
      status: 503,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: false,
        error: { code: 'TEMPORARILY_UNAVAILABLE', message: 'Jobs are temporarily unavailable' }
      })
    };
  }

  const targetUrl = `${getBaseUrl()}/jobs/filters`;

  try {
    const res = await fetchWithRetry(targetUrl, {
      method: 'GET',
      headers: {
        'X-API-Key': apiKey,
        'Accept': 'application/json',
        'User-Agent': 'MSBTE-Notes-JobsProxy/1.0'
      }
    });

    const status = res.status;
    const requestId = res.headers.get('x-request-id') || 'unknown';
    const retryAfter = res.headers.get('retry-after');

    if (!res.ok) {
      console.error(`[Artha Proxy Error] /jobs/filters status: ${status}, Request-Id: ${requestId}`);
    }

    // 401 or 403: Hide internal auth errors from client
    if (status === 401 || status === 403) {
      return {
        status: 503,
        headers: { 'Content-Type': 'application/json', 'X-Request-Id': requestId },
        body: JSON.stringify({
          success: false,
          error: { code: 'TEMPORARILY_UNAVAILABLE', message: 'Jobs are temporarily unavailable' }
        })
      };
    }

    const responseBody = await res.text();
    const returnHeaders = {
      'Content-Type': 'application/json; charset=utf-8',
      'X-Request-Id': requestId,
      'Cache-Control': 'public, max-age=3600'
    };
    if (retryAfter) {
      returnHeaders['Retry-After'] = retryAfter;
    }

    if (res.ok) {
      filtersCache = {
        status,
        headers: returnHeaders,
        body: responseBody,
        timestamp: now
      };
    }

    return {
      status,
      headers: returnHeaders,
      body: responseBody
    };
  } catch (err) {
    console.error('[Artha Proxy Network Error] /jobs/filters:', err.message);
    return {
      status: 502,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: false,
        error: { code: 'EXTERNAL_API_ERROR', message: 'Job data temporarily unavailable; retry shortly' }
      })
    };
  }
}

/**
 * Handle GET /api/jobs
 */
async function handleJobsRequest(rawQuery) {
  const cleanParams = sanitizeJobParams(rawQuery);
  const queryString = cleanParams.toString();
  const cacheKey = queryString || 'default';
  const now = Date.now();

  const cached = jobsCache.get(cacheKey);
  if (cached && (now - cached.timestamp < JOBS_CACHE_TTL_MS)) {
    return {
      status: cached.status,
      headers: { ...cached.headers, 'X-Cache': 'HIT' },
      body: cached.body
    };
  }

  const apiKey = process.env.ARTHA_API_KEY;
  if (!apiKey) {
    console.error('[Artha Proxy Error] Missing ARTHA_API_KEY environment variable');
    return {
      status: 503,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: false,
        error: { code: 'TEMPORARILY_UNAVAILABLE', message: 'Jobs are temporarily unavailable' }
      })
    };
  }

  const targetUrl = queryString ? `${getBaseUrl()}/jobs?${queryString}` : `${getBaseUrl()}/jobs`;

  try {
    const res = await fetchWithRetry(targetUrl, {
      method: 'GET',
      headers: {
        'X-API-Key': apiKey,
        'Accept': 'application/json',
        'User-Agent': 'MSBTE-Notes-JobsProxy/1.0'
      }
    });

    const status = res.status;
    const requestId = res.headers.get('x-request-id') || 'unknown';
    const retryAfter = res.headers.get('retry-after');

    if (!res.ok) {
      console.error(`[Artha Proxy Error] /jobs status: ${status}, Request-Id: ${requestId}`);
    }

    // 401 or 403: Hide internal authentication details from client
    if (status === 401 || status === 403) {
      return {
        status: 503,
        headers: { 'Content-Type': 'application/json', 'X-Request-Id': requestId },
        body: JSON.stringify({
          success: false,
          error: { code: 'TEMPORARILY_UNAVAILABLE', message: 'Jobs are temporarily unavailable' }
        })
      };
    }

    const responseBody = await res.text();
    const returnHeaders = {
      'Content-Type': 'application/json; charset=utf-8',
      'X-Request-Id': requestId,
      'Cache-Control': 'public, max-age=60'
    };
    if (retryAfter) {
      returnHeaders['Retry-After'] = retryAfter;
    }

    if (res.ok) {
      if (jobsCache.size >= 100) {
        const oldestKey = jobsCache.keys().next().value;
        jobsCache.delete(oldestKey);
      }
      jobsCache.set(cacheKey, {
        status,
        headers: returnHeaders,
        body: responseBody,
        timestamp: now
      });
    }

    return {
      status,
      headers: returnHeaders,
      body: responseBody
    };
  } catch (err) {
    console.error('[Artha Proxy Network Error] /jobs:', err.message);
    return {
      status: 502,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: false,
        error: { code: 'EXTERNAL_API_ERROR', message: 'Job data temporarily unavailable; retry shortly' }
      })
    };
  }
}

/**
 * Standard HTTP Request Router
 */
async function processApiRequest(pathname, query) {
  const normalized = pathname.replace(/^\/api/, '').replace(/\/+$/, '') || '/';

  if (normalized === '/jobs/filters' || normalized === '/filters') {
    return await handleFiltersRequest();
  }

  if (normalized === '/jobs' || normalized === '') {
    return await handleJobsRequest(query);
  }

  return {
    status: 404,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      success: false,
      error: { code: 'NOT_FOUND', message: 'Endpoint not found' }
    })
  };
}

function applyCors(headers) {
  return {
    ...headers,
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-API-Key, Authorization, X-Requested-With'
  };
}

/**
 * Standalone HTTP Server for local dev and testing
 */
function startStandaloneServer(port = process.env.PORT || 3000) {
  const rootDir = path.resolve(__dirname, '..');

  const mimeTypes = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.xml': 'application/xml',
    '.txt': 'text/plain'
  };

  const server = http.createServer(async (req, res) => {
    const host = req.headers.host || 'localhost';
    const parsedUrl = new URL(req.url, `http://${host}`);
    const pathname = parsedUrl.pathname;
    const query = Object.fromEntries(parsedUrl.searchParams.entries());

    if (req.method === 'OPTIONS') {
      res.writeHead(204, applyCors({}));
      return res.end();
    }

    if (pathname.startsWith('/api/')) {
      if (req.method !== 'GET') {
        res.writeHead(405, applyCors({ 'Content-Type': 'application/json' }));
        return res.end(JSON.stringify({ success: false, error: { code: 'METHOD_NOT_ALLOWED', message: 'Method not allowed' } }));
      }
      const result = await processApiRequest(pathname, query);
      res.writeHead(result.status, applyCors(result.headers));
      return res.end(result.body);
    }

    let filePath = path.join(rootDir, pathname === '/' ? 'index.html' : pathname);
    if (!path.extname(filePath)) {
      if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
        filePath = path.join(filePath, 'index.html');
      } else if (fs.existsSync(filePath + '.html')) {
        filePath = filePath + '.html';
      }
    }

    if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
      const ext = path.extname(filePath).toLowerCase();
      const contentType = mimeTypes[ext] || 'application/octet-stream';
      res.writeHead(200, { 'Content-Type': contentType });
      fs.createReadStream(filePath).pipe(res);
    } else {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
    }
  });

  server.listen(port, () => {
    console.log(`[Artha Jobs Proxy] Running at http://localhost:${port}`);
  });

  return server;
}

if (require.main === module) {
  startStandaloneServer();
}

module.exports = {
  processApiRequest,
  handleJobsRequest,
  handleFiltersRequest,
  sanitizeJobParams,
  startStandaloneServer,
  applyCors
};
