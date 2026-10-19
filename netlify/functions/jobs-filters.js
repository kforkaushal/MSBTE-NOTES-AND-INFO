/**
 * Netlify Function: /api/jobs/filters
 * Proxies filter requests to artha.link Public Jobs API
 */

const { handleFiltersRequest, applyCors } = require('../../functions/jobs-proxy');

exports.handler = async (event) => {
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers: applyCors({}),
      body: ''
    };
  }

  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      headers: applyCors({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        success: false,
        error: { code: 'METHOD_NOT_ALLOWED', message: 'Method not allowed' }
      })
    };
  }

  try {
    const result = await handleFiltersRequest();

    return {
      statusCode: result.status,
      headers: applyCors(result.headers),
      body: result.body
    };
  } catch (err) {
    console.error('[Netlify Function /api/jobs/filters Error]:', err.message);
    return {
      statusCode: 502,
      headers: applyCors({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        success: false,
        error: { code: 'EXTERNAL_API_ERROR', message: 'Job data temporarily unavailable; retry shortly' }
      })
    };
  }
};
