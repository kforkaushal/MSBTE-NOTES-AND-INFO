/**
 * Test suite for MSBTE Notes & Info - Jobs Proxy
 */

const assert = require('assert');
const {
  sanitizeJobParams,
  processApiRequest
} = require('../functions/jobs-proxy');

async function runTests() {
  console.log('Running Jobs Proxy Tests...\n');

  // Test 1: Query Sanitization, Geolocation default, & Clamping
  console.log('Test 1: Query parameter sanitization, clamping, and location=IN default');
  const rawQuery = {
    limit: '250',
    offset: '-5',
    q: 'software engineer',
    job_type: 'Full-Time', // Should normalize to lowercase
    work_mode: 'REMOTE',   // Should normalize to lowercase
    sort_by: 'newest',
    categories: 'software-development',
    malicious_param: 'select * from users',
    unknown_filter: 'random'
  };

  const clean = sanitizeJobParams(rawQuery);
  assert.strictEqual(clean.get('limit'), '100', 'limit should be clamped to 100');
  assert.strictEqual(clean.get('offset'), '0', 'offset should not be negative');
  assert.strictEqual(clean.get('q'), 'software engineer');
  assert.strictEqual(clean.get('job_type'), 'full-time', 'job_type normalized');
  assert.strictEqual(clean.get('work_mode'), 'remote', 'work_mode normalized');
  assert.strictEqual(clean.get('categories'), 'software-development');
  assert.strictEqual(clean.get('sort_by'), 'newest');
  assert.strictEqual(clean.get('location'), 'IN', 'location must default to IN when not sent');
  assert.strictEqual(clean.get('malicious_param'), null, 'unallowed param stripped');
  assert.strictEqual(clean.get('unknown_filter'), null, 'unknown param stripped');

  // Explicit location should override default
  const cleanWithLocation = sanitizeJobParams({ location: 'US' });
  assert.strictEqual(cleanWithLocation.get('location'), 'US');

  // Explicit state should satisfy geo condition
  const cleanWithState = sanitizeJobParams({ state: 'Maharashtra' });
  assert.strictEqual(cleanWithState.get('state'), 'Maharashtra');
  assert(!cleanWithState.has('location'), 'does not force location if state sent');

  console.log('  Passed: Query sanitization, clamping, location=IN default, and allowlisting work as expected.\n');

  // Test 2: Handling without API Key
  console.log('Test 2: Graceful error when ARTHA_API_KEY is not set');
  const savedKey = process.env.ARTHA_API_KEY;
  delete process.env.ARTHA_API_KEY;

  const noKeyRes = await processApiRequest('/api/jobs', {});
  assert.strictEqual(noKeyRes.status, 503, 'Missing API key should return 503');
  const noKeyBody = JSON.parse(noKeyRes.body);
  assert.strictEqual(noKeyBody.success, false);
  assert.strictEqual(noKeyBody.error.message, 'Jobs are temporarily unavailable');
  // Confirm no leak of API key name or env details in client response
  assert(!noKeyRes.body.includes('ARTHA_API_KEY'), 'Response must not mention internal key variable');
  console.log('  Passed: API key is never leaked and 503 is cleanly returned.\n');

  // Test 3: 404 for unknown endpoints
  console.log('Test 3: 404 for unknown API paths');
  const notFoundRes = await processApiRequest('/api/unknown', {});
  assert.strictEqual(notFoundRes.status, 404);
  console.log('  Passed: Unknown path returns 404.\n');

  // Test 4: Mock Artha API responses (200, Caching, 429 with Retry-After, X-API-Key auth, 502 retry)
  console.log('Test 4: Mocked API interactions (200, Caching, 429, 502 retry, X-API-Key)');
  process.env.ARTHA_API_KEY = 'ak_live_mock_test_key_12345';
  process.env.ARTHA_API_BASE_URL = 'https://api-india.artha.link/api/v1';
  const originalFetch = global.fetch;

  try {
    let fetchCalls = 0;
    let attempts502 = 0;

    global.fetch = async (url, options) => {
      fetchCalls++;
      // Check X-API-Key header as per official artha.link help article
      assert.strictEqual(options.headers['X-API-Key'], 'ak_live_mock_test_key_12345', 'X-API-Key header must be sent');
      assert(url.startsWith('https://api-india.artha.link/api/v1'), 'Must use ARTHA_API_BASE_URL');

      if (url.includes('trigger_502_retry')) {
        attempts502++;
        if (attempts502 < 2) {
          return {
            status: 502,
            ok: false,
            headers: new Headers({ 'content-type': 'application/json', 'x-request-id': 'req-502-mock' }),
            text: async () => JSON.stringify({ success: false, error: { code: 'EXTERNAL_API_ERROR' } })
          };
        }
        return {
          status: 200,
          ok: true,
          headers: new Headers({ 'content-type': 'application/json', 'x-request-id': 'req-502-recovered' }),
          text: async () => JSON.stringify({ success: true, data: { items: [], total: 0 } })
        };
      }

      if (url.includes('/jobs/filters')) {
        return {
          status: 200,
          ok: true,
          headers: new Headers({
            'content-type': 'application/json',
            'x-request-id': 'req-filter-mock-123'
          }),
          text: async () => JSON.stringify({
            success: true,
            data: {
              categories: [{ value: 'software technology', count: 77 }],
              job_types: [{ value: 'full-time', count: 12 }],
              work_modes: [{ value: 'remote', count: 5 }]
            }
          })
        };
      }

      if (url.includes('trigger_429')) {
        return {
          status: 429,
          ok: false,
          headers: new Headers({
            'content-type': 'application/json',
            'retry-after': '7',
            'x-request-id': 'req-rate-limit-429'
          }),
          text: async () => JSON.stringify({
            success: false,
            error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Rate limit exceeded' }
          })
        };
      }

      return {
        status: 200,
        ok: true,
        headers: new Headers({
          'content-type': 'application/json',
          'x-request-id': 'req-jobs-mock-456'
        }),
        text: async () => JSON.stringify({
          success: true,
          data: {
            items: [{ id: 'job-1', title: 'Software Engineer', company: 'micro1', url: 'https://artha.link/job1' }],
            total: 1,
            limit: 10,
            offset: 0,
            has_more: false
          }
        })
      };
    };

    // Test filters fetching and caching
    const filterRes1 = await processApiRequest('/api/jobs/filters', {});
    assert.strictEqual(filterRes1.status, 200);
    assert.strictEqual(fetchCalls, 1, 'First filters call hits network');

    const filterRes2 = await processApiRequest('/api/jobs/filters', {});
    assert.strictEqual(filterRes2.status, 200);
    assert.strictEqual(filterRes2.headers['X-Cache'], 'HIT', 'Second filters call hits cache');
    assert.strictEqual(fetchCalls, 1, 'No new network call made due to cache');

    // Test 429 forwarding
    const rateLimitRes = await processApiRequest('/api/jobs', { q: 'trigger_429' });
    assert.strictEqual(rateLimitRes.status, 429, 'Proxy forwards 429 status code');
    assert.strictEqual(rateLimitRes.headers['Retry-After'], '7', 'Proxy forwards Retry-After header');
    assert.strictEqual(rateLimitRes.headers['X-Request-Id'], 'req-rate-limit-429', 'Proxy forwards X-Request-Id header');

    // Test 502 automatic retry
    const retryRes = await processApiRequest('/api/jobs', { q: 'trigger_502_retry' });
    assert.strictEqual(retryRes.status, 200, '502 recovers on automatic retry');
    assert.strictEqual(attempts502, 2, '2 attempts made before success');

    console.log('  Passed: X-API-Key auth, 200 data, 429 forwarding, 502 retry, and caching work.\n');
  } finally {
    global.fetch = originalFetch;
    delete process.env.ARTHA_API_KEY;
    if (savedKey) process.env.ARTHA_API_KEY = savedKey;
  }

  console.log('All backend proxy tests passed successfully!');
}

runTests().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
