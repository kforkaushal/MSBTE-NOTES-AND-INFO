/**
 * End-to-End Integration & Security Verification for Jobs Page & Artha Proxy
 */

const http = require('http');
const assert = require('assert');
const path = require('path');
const fs = require('fs');

// Set dummy test key and regional base URL
process.env.ARTHA_API_KEY = 'ak_live_mock_secret_test_key_xyz';
process.env.ARTHA_API_BASE_URL = 'https://api-india.artha.link/api/v1';

const { startStandaloneServer } = require('../functions/jobs-proxy');
const netlifyJobsHandler = require('../netlify/functions/jobs').handler;
const netlifyFiltersHandler = require('../netlify/functions/jobs-filters').handler;

async function runE2ETests() {
  console.log('=== Starting Jobs Page E2E & Security Tests ===\n');

  const TEST_PORT = 3899;
  let server;

  let upstreamRequests = [];

  // Mock Artha API upstream HTTP server on port 3999
  const MOCK_ARTHA_PORT = 3999;
  const mockArthaServer = http.createServer((req, res) => {
    const parsed = new URL(req.url, `http://localhost:${MOCK_ARTHA_PORT}`);
    upstreamRequests.push({
      path: parsed.pathname,
      query: parsed.search,
      headers: req.headers
    });

    // Check X-API-Key auth header
    const apiKey = req.headers['x-api-key'];
    if (apiKey !== 'ak_live_mock_secret_test_key_xyz') {
      res.writeHead(401, { 'Content-Type': 'application/json', 'X-Request-Id': 'req-unauthorized' });
      return res.end(JSON.stringify({ success: false, error: { code: 'INVALID_API_KEY', message: 'Invalid API key' } }));
    }

    if (parsed.pathname === '/api/v1/jobs/filters') {
      res.writeHead(200, {
        'Content-Type': 'application/json',
        'X-Request-Id': 'req-filter-mock-id-777'
      });
      return res.end(JSON.stringify({
        success: true,
        data: {
          categories: [{ value: 'software technology', count: 77 }],
          job_types: [{ value: 'full-time', count: 42 }, { value: 'internship', count: 18 }],
          work_modes: [{ value: 'remote', count: 15 }, { value: 'hybrid', count: 20 }, { value: 'onsite', count: 25 }]
        }
      }));
    }

    if (parsed.pathname === '/api/v1/jobs') {
      const q = parsed.searchParams.get('q');
      if (q === 'rate_limit_test') {
        res.writeHead(429, {
          'Content-Type': 'application/json',
          'Retry-After': '5',
          'X-Request-Id': 'req-rate-limit-999'
        });
        return res.end(JSON.stringify({
          success: false,
          error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Rate limit exceeded' }
        }));
      }

      const limit = parseInt(parsed.searchParams.get('limit') || '10', 10);
      const offset = parseInt(parsed.searchParams.get('offset') || '0', 10);

      const sampleJobs = [
        {
          id: 'job-101',
          title: 'Software Development Engineer - Fresher',
          company: 'Amazon',
          location: 'Bengaluru, KA, IN',
          city: 'Bengaluru',
          state: 'Karnataka',
          country: 'India',
          job_type: 'full-time',
          work_mode: 'hybrid',
          salary_min: 450000,
          salary_max: 850000,
          salary_curr: '₹',
          skills: ['Java', 'Python', 'Data Structures', 'SQL'],
          posted_date: new Date(Date.now() - 3600000 * 4).toISOString(),
          url: 'https://artha.link/jobs/view/job-101'
        },
        {
          id: 'job-102',
          title: 'Lead Engineer - Mechanical Component 2',
          company: 'GE Vernova',
          location: 'Bengaluru, IN',
          city: 'Bengaluru',
          state: 'Karnataka',
          country: 'India',
          job_type: 'full-time',
          work_mode: 'onsite',
          salary_min: 350000,
          salary_max: 520000,
          salary_curr: '₹',
          skills: ['Mechanical', 'CAD', 'Design'],
          posted_date: new Date(Date.now() - 86400000 * 2).toISOString(),
          url: 'https://artha.link/jobs/view/job-102'
        }
      ];

      res.writeHead(200, {
        'Content-Type': 'application/json',
        'X-Request-Id': 'req-jobs-list-888'
      });
      return res.end(JSON.stringify({
        success: true,
        data: {
          items: sampleJobs,
          total: 2,
          limit,
          offset,
          has_more: false
        }
      }));
    }

    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ success: false, error: { code: 'NOT_FOUND', message: 'Not Found' } }));
  });

  await new Promise(resolve => mockArthaServer.listen(MOCK_ARTHA_PORT, resolve));
  console.log(`[Mock Upstream] Listening on port ${MOCK_ARTHA_PORT}`);

  const originalFetch = global.fetch;
  global.fetch = async (inputUrl, opts) => {
    const redirectedUrl = String(inputUrl).replace(/https:\/\/api(-india|-usa)?\.artha\.link/, `http://127.0.0.1:${MOCK_ARTHA_PORT}`);
    return originalFetch(redirectedUrl, opts);
  };

  try {
    server = startStandaloneServer(TEST_PORT);
    await new Promise(resolve => setTimeout(resolve, 500));

    function get(reqPath, headers = {}) {
      return new Promise((resolve, reject) => {
        const req = http.get(`http://127.0.0.1:${TEST_PORT}${reqPath}`, { headers }, res => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body: data }));
        });
        req.on('error', reject);
      });
    }

    // 1. Verify GET /api/jobs/filters
    console.log('Test 1: GET /api/jobs/filters');
    const filterRes = await get('/api/jobs/filters');
    assert.strictEqual(filterRes.status, 200);
    const filterJson = JSON.parse(filterRes.body);
    assert(filterJson.success);
    assert(filterJson.data.job_types.length > 0);
    assert.strictEqual(filterRes.headers['x-request-id'], 'req-filter-mock-id-777');
    console.log('  Passed: /api/jobs/filters successfully returns filter counts.\n');

    // 2. Verify Query Parameter Filtering, Location=IN default & Clamping
    console.log('Test 2: GET /api/jobs with allowlist filtering, clamping, and location=IN default');
    const jobsRes = await get('/api/jobs?limit=500&offset=0&q=engineer&job_type=FULL-TIME&malicious_param=evil_attack');
    assert.strictEqual(jobsRes.status, 200);
    const jobsJson = JSON.parse(jobsRes.body);
    assert(jobsJson.success);
    assert.strictEqual(jobsJson.data.items.length, 2);

    const lastUpstreamReq = upstreamRequests[upstreamRequests.length - 1];
    assert.strictEqual(lastUpstreamReq.headers['x-api-key'], 'ak_live_mock_secret_test_key_xyz', 'X-API-Key sent to upstream');
    assert(!lastUpstreamReq.query.includes('malicious_param'), 'malicious_param was properly stripped');
    assert(lastUpstreamReq.query.includes('limit=100'), 'limit clamped to 100 max');
    assert(lastUpstreamReq.query.includes('job_type=full-time'), 'job_type normalized to lowercase');
    assert(lastUpstreamReq.query.includes('location=IN'), 'location=IN defaulted when no location/state/city sent');
    console.log('  Passed: Query params allowlisted, clamped, normalized, and location=IN injected.\n');

    // 3. Verify Netlify Functions Direct Invocation
    console.log('Test 3: Netlify Serverless Functions (jobs.js & jobs-filters.js)');
    const netlifyEventJobs = {
      httpMethod: 'GET',
      queryStringParameters: { limit: '5', q: 'engineer' }
    };
    const netlifyJobsRes = await netlifyJobsHandler(netlifyEventJobs);
    assert.strictEqual(netlifyJobsRes.statusCode, 200);
    assert(netlifyJobsRes.headers['Cache-Control'].includes('max-age=60'));

    const netlifyEventFilters = {
      httpMethod: 'GET',
      queryStringParameters: {}
    };
    const netlifyFiltersRes = await netlifyFiltersHandler(netlifyEventFilters);
    assert.strictEqual(netlifyFiltersRes.statusCode, 200);
    assert(netlifyFiltersRes.headers['Cache-Control'].includes('max-age=3600'));
    console.log('  Passed: Netlify functions handler executed cleanly with correct edge Cache-Control.\n');

    // 4. Verify Security: Key never leaked in client response
    console.log('Test 4: Security - ARTHA_API_KEY is NEVER present in responses');
    assert(!jobsRes.body.includes('ak_live_mock_secret_test_key_xyz'), 'API key leaked in jobs body!');
    assert(!filterRes.body.includes('ak_live_mock_secret_test_key_xyz'), 'API key leaked in filter body!');
    assert(!netlifyJobsRes.body.includes('ak_live_mock_secret_test_key_xyz'), 'API key leaked in netlify response!');
    for (const h of Object.values(jobsRes.headers)) {
      assert(!String(h).includes('ak_live_mock_secret_test_key_xyz'), 'API key leaked in header!');
    }
    console.log('  Passed: API key is completely concealed from client.\n');

    // 5. Verify 429 Rate Limiting & Retry-After propagation
    console.log('Test 5: 429 Rate limit response forwarding with Retry-After');
    const rateLimitRes = await get('/api/jobs?q=rate_limit_test');
    assert.strictEqual(rateLimitRes.status, 429);
    assert.strictEqual(rateLimitRes.headers['retry-after'], '5');
    assert.strictEqual(rateLimitRes.headers['x-request-id'], 'req-rate-limit-999');
    console.log('  Passed: 429 and Retry-After header cleanly passed to client.\n');

    // 6. Verify Static File Serving & UI elements
    console.log('Test 6: Static serving of Jobs/index.html, Jobs/jobs.css, Jobs/jobs.js');
    const htmlRes = await get('/Jobs/');
    assert.strictEqual(htmlRes.status, 200);
    assert(htmlRes.headers['content-type'].includes('text/html'));
    assert(htmlRes.body.includes('Jobs for Freshers &amp; Diploma/Engineering Students'));
    assert(htmlRes.body.includes('artha.link'));
    assert(htmlRes.body.includes('categorySelect'));
    assert(htmlRes.body.includes('jobSearchInput'));
    assert(htmlRes.body.includes('jobTypeSelect'));
    assert(htmlRes.body.includes('loadMoreBtn'));

    const cssRes = await get('/Jobs/jobs.css');
    assert.strictEqual(cssRes.status, 200);
    assert(cssRes.headers['content-type'].includes('text/css'));

    const jsRes = await get('/Jobs/jobs.js');
    assert.strictEqual(jsRes.status, 200);
    assert(jsRes.headers['content-type'].includes('javascript'));
    console.log('  Passed: Static assets served properly with correct MIME types.\n');

    // 7. Verify Acceptance Checklist items:
    console.log('Test 7: Acceptance Checklist Verifications');
    const gitignoreContent = fs.readFileSync(path.resolve(__dirname, '../.gitignore'), 'utf8');
    assert(gitignoreContent.includes('.env'), '.gitignore must contain .env');

    const envExample = fs.readFileSync(path.resolve(__dirname, '../.env.example'), 'utf8');
    assert(envExample.includes('ARTHA_API_KEY=ak_live_xxxxxxxxxxxxxxxx'));
    assert(envExample.includes('ARTHA_API_BASE_URL=https://api-india.artha.link/api/v1'));

    const netlifyToml = fs.readFileSync(path.resolve(__dirname, '../netlify.toml'), 'utf8');
    assert(netlifyToml.includes('functions = "netlify/functions"'));
    assert(netlifyToml.includes('from = "/api/jobs"'));
    assert(netlifyToml.includes('from = "/api/jobs/filters"'));

    // Check direct job.url usage
    assert(jsRes.body.includes('job.url'));
    assert(!jsRes.body.includes('job-detail.html?id='), 'jobs.js must link directly to job.url');

    console.log('  Passed: All acceptance checklist items confirmed.\n');

    console.log('========================================================');
    console.log('🎉 ALL INTEGRATION & SECURITY TESTS PASSED SUCCESSFULLY! 🎉');
    console.log('========================================================');
  } finally {
    global.fetch = originalFetch;
    delete process.env.ARTHA_API_KEY;
    if (server) server.close();
    if (mockArthaServer) mockArthaServer.close();
  }
}

runE2ETests().catch(err => {
  console.error('\n❌ E2E Test Failure:', err);
  process.exit(1);
});
