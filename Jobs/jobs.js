/**
 * MSBTE Notes & Info - Jobs Page Client Logic
 * Powered by artha.link Public Jobs API (via Netlify proxy /api/jobs)
 */

(() => {
  'use strict';

  // --- Configuration & Constants ---
  const API_BASE = '/api';
  const PAGE_LIMIT = 12;
  const MAX_AUTO_RETRIES = 3;
  const DEBOUNCE_DELAY_MS = 400;

  const AVATAR_GRADIENTS = [
    'linear-gradient(135deg, #3b82f6, #1d4ed8)',
    'linear-gradient(135deg, #10b981, #047857)',
    'linear-gradient(135deg, #8b5cf6, #6d28d9)',
    'linear-gradient(135deg, #f59e0b, #d97706)',
    'linear-gradient(135deg, #ec4899, #be185d)',
    'linear-gradient(135deg, #06b6d4, #0e7490)',
    'linear-gradient(135deg, #6366f1, #4338ca)'
  ];

  // --- State Variables ---
  let currentOffset = 0;
  let totalJobs = 0;
  let hasMoreJobs = false;
  let isLoading = false;
  let retryCount429 = 0;
  let countdownTimer = null;
  let searchDebounceTimer = null;
  let bookmarkedJobs = {};

  // Active filters (mapped strictly to API reference)
  let filterState = {
    q: '',
    categories: '',
    job_type: '',
    work_mode: '',
    location: '',
    sort_by: 'most_relevant'
  };

  // --- DOM Elements ---
  let jobsGrid = null;
  let loadMoreBtn = null;
  let loadMoreWrap = null;
  let statusContainer = null;
  let resultsCountEl = null;
  let clearFiltersBtn = null;

  // Filter inputs
  let searchInput = null;
  let categorySelect = null;
  let typeSelect = null;
  let modeSelect = null;
  let locationSelect = null;
  let sortSelect = null;

  // --- Initialization ---
  document.addEventListener('DOMContentLoaded', () => {
    cacheDomElements();
    loadBookmarks();
    initUrlParams();
    bindEvents();
    loadFilterOptions();
    fetchJobs(true);
  });

  function cacheDomElements() {
    jobsGrid = document.getElementById('jobsGrid');
    loadMoreBtn = document.getElementById('loadMoreBtn');
    loadMoreWrap = document.getElementById('loadMoreWrap');
    statusContainer = document.getElementById('statusContainer');
    resultsCountEl = document.getElementById('resultsCount');
    clearFiltersBtn = document.getElementById('clearFiltersBtn');

    searchInput = document.getElementById('jobSearchInput');
    categorySelect = document.getElementById('categorySelect');
    typeSelect = document.getElementById('jobTypeSelect');
    modeSelect = document.getElementById('workModeSelect');
    locationSelect = document.getElementById('locationSelect');
    sortSelect = document.getElementById('sortSelect');

    // Mobile nav toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileNav = document.getElementById('mobileNav');
    if (mobileMenuBtn && mobileNav) {
      mobileMenuBtn.addEventListener('click', () => {
        mobileNav.classList.toggle('hidden');
      });
    }
  }

  // --- URL & Filter State Sync ---
  function initUrlParams() {
    const params = new URLSearchParams(window.location.search);
    if (params.has('q')) filterState.q = params.get('q');
    if (params.has('categories')) filterState.categories = params.get('categories');
    if (params.has('job_type')) filterState.job_type = params.get('job_type');
    if (params.has('work_mode')) filterState.work_mode = params.get('work_mode');
    if (params.has('location')) filterState.location = params.get('location');
    if (params.has('sort_by')) filterState.sort_by = params.get('sort_by');

    // Update UI controls to match
    if (searchInput) searchInput.value = filterState.q;
    if (categorySelect) categorySelect.value = filterState.categories;
    if (typeSelect) typeSelect.value = filterState.job_type;
    if (modeSelect) modeSelect.value = filterState.work_mode;
    if (locationSelect) locationSelect.value = filterState.location;
    if (sortSelect) sortSelect.value = filterState.sort_by;
  }

  function syncUrlWithState() {
    const params = new URLSearchParams();
    for (const [key, val] of Object.entries(filterState)) {
      if (val && val !== 'most_relevant') {
        params.set(key, val);
      }
    }
    const newQuery = params.toString();
    const newUrl = newQuery ? `${window.location.pathname}?${newQuery}` : window.location.pathname;
    window.history.pushState(filterState, '', newUrl);
  }

  window.addEventListener('popstate', (e) => {
    if (e.state) {
      filterState = { ...e.state };
    } else {
      initUrlParams();
    }
    if (searchInput) searchInput.value = filterState.q || '';
    if (categorySelect) categorySelect.value = filterState.categories || '';
    if (typeSelect) typeSelect.value = filterState.job_type || '';
    if (modeSelect) modeSelect.value = filterState.work_mode || '';
    if (locationSelect) locationSelect.value = filterState.location || '';
    if (sortSelect) sortSelect.value = filterState.sort_by || 'most_relevant';

    currentOffset = 0;
    fetchJobs(true);
  });

  // --- Event Bindings ---
  function bindEvents() {
    // Debounced search
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(() => {
          filterState.q = e.target.value.trim();
          onFilterChange();
        }, DEBOUNCE_DELAY_MS);
      });
    }

    // Dropdown filters
    const filterElements = [
      { el: categorySelect, key: 'categories' },
      { el: typeSelect, key: 'job_type' },
      { el: modeSelect, key: 'work_mode' },
      { el: locationSelect, key: 'location' },
      { el: sortSelect, key: 'sort_by' }
    ];

    filterElements.forEach(({ el, key }) => {
      if (el) {
        el.addEventListener('change', (e) => {
          filterState[key] = e.target.value;
          onFilterChange();
        });
      }
    });

    // Clear filters
    if (clearFiltersBtn) {
      clearFiltersBtn.addEventListener('click', resetFilters);
    }

    // Load More
    if (loadMoreBtn) {
      loadMoreBtn.addEventListener('click', () => {
        if (!isLoading && hasMoreJobs) {
          fetchJobs(false);
        }
      });
    }

    // Bookmark clicks on job cards delegation
    if (jobsGrid) {
      jobsGrid.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-job-bookmark');
        if (!btn) return;
        const jobId = btn.dataset.jobId;
        const jobTitle = btn.dataset.jobTitle;
        const jobCompany = btn.dataset.jobCompany;
        const jobUrl = btn.dataset.jobUrl;
        const jobLogo = btn.dataset.jobLogo;
        const jobLocation = btn.dataset.jobLocation;
        const jobType = btn.dataset.jobType;

        toggleBookmark({
          id: jobId,
          title: jobTitle,
          company: jobCompany,
          url: jobUrl,
          logo: jobLogo,
          location: jobLocation,
          type: jobType
        }, btn);
      });
    }
  }

  function onFilterChange() {
    currentOffset = 0;
    syncUrlWithState();
    fetchJobs(true);
  }

  function resetFilters() {
    filterState = {
      q: '',
      categories: '',
      job_type: '',
      work_mode: '',
      location: '',
      sort_by: 'most_relevant'
    };

    if (searchInput) searchInput.value = '';
    if (categorySelect) categorySelect.value = '';
    if (typeSelect) typeSelect.value = '';
    if (modeSelect) modeSelect.value = '';
    if (locationSelect) locationSelect.value = '';
    if (sortSelect) sortSelect.value = 'most_relevant';

    onFilterChange();
  }

  // --- API: Load Filters ---
  async function loadFilterOptions() {
    try {
      const res = await fetch(`${API_BASE}/jobs/filters`, {
        headers: { 'Accept': 'application/json' }
      });
      if (!res.ok) return;

      const data = await res.json();
      const filters = data.data || data;

      populateSelect(categorySelect, filters.categories, filterState.categories, 'All Categories');
      populateSelect(typeSelect, filters.job_types, filterState.job_type, 'All Job Types');
      populateSelect(modeSelect, filters.work_modes, filterState.work_mode, 'All Work Modes');
    } catch (err) {
      console.warn('[Jobs] Dynamic filter options load fallback:', err.message);
    }
  }

  function populateSelect(selectEl, items, selectedValue, defaultLabel) {
    if (!selectEl || !Array.isArray(items) || items.length === 0) return;

    selectEl.innerHTML = `<option value="">${defaultLabel}</option>`;
    items.forEach(item => {
      const val = typeof item === 'object' ? item.value : item;
      const count = typeof item === 'object' && item.count !== undefined ? ` (${item.count.toLocaleString()})` : '';
      const text = `${formatLabel(val)}${count}`;

      const opt = document.createElement('option');
      opt.value = val;
      opt.textContent = text;
      if (String(val).toLowerCase() === String(selectedValue).toLowerCase()) {
        opt.selected = true;
      }
      selectEl.appendChild(opt);
    });
  }

  function formatLabel(str) {
    if (!str) return '';
    return String(str)
      .replace(/[-_]/g, ' ')
      .replace(/\b\w/g, c => c.toUpperCase());
  }

  // --- API: Fetch Jobs ---
  async function fetchJobs(isInitial = false) {
    if (isLoading) return;
    isLoading = true;

    if (isInitial) {
      currentOffset = 0;
      clearStatus();
      renderSkeletons();
      if (loadMoreWrap) loadMoreWrap.classList.add('hidden');
    } else {
      setLoadMoreSpinner(true);
    }

    // Build query params
    const params = new URLSearchParams();
    params.set('limit', String(PAGE_LIMIT));
    params.set('offset', String(currentOffset));

    if (filterState.q) params.set('q', filterState.q);
    if (filterState.categories) params.set('categories', filterState.categories);
    if (filterState.job_type) params.set('job_type', filterState.job_type);
    if (filterState.work_mode) params.set('work_mode', filterState.work_mode);
    if (filterState.sort_by && filterState.sort_by !== 'most_relevant') {
      params.set('sort_by', filterState.sort_by);
    }

    // Location parameter handling
    if (filterState.location) {
      const loc = filterState.location.trim();
      if (loc.toLowerCase() === 'maharashtra') {
        params.set('state', 'Maharashtra');
        params.set('location', 'IN');
      } else if (['pune', 'mumbai', 'bengaluru'].includes(loc.toLowerCase())) {
        params.set('city', loc);
        params.set('location', 'IN');
      } else {
        params.set('location', loc);
      }
    } else {
      // Default location to IN (India) as instructed
      params.set('location', 'IN');
    }

    try {
      const res = await fetch(`${API_BASE}/jobs?${params.toString()}`, {
        headers: { 'Accept': 'application/json' }
      });

      // Handle 429 Rate Limit Backoff
      if (res.status === 429) {
        await handleRateLimit(res, isInitial);
        return;
      }

      // Handle 401, 403 or server errors
      if (!res.ok) {
        const reqId = res.headers.get('x-request-id');
        if (reqId) console.warn(`[Jobs API Request ID: ${reqId}]`);

        if (res.status === 401 || res.status === 403 || res.status === 503) {
          renderErrorState('Jobs are temporarily unavailable. Please check back later.', true);
        } else {
          renderErrorState('Unable to load job listings right now.', false);
        }
        return;
      }

      // Reset 429 retry counter on success
      retryCount429 = 0;

      const json = await res.json();
      const payload = json.data || json;
      const items = Array.isArray(payload.items) ? payload.items : (Array.isArray(payload) ? payload : []);
      totalJobs = payload.total !== undefined ? payload.total : items.length;
      hasMoreJobs = payload.has_more !== undefined ? payload.has_more : (items.length >= PAGE_LIMIT);

      if (isInitial) {
        jobsGrid.innerHTML = '';
      }

      if (items.length === 0 && isInitial) {
        renderEmptyState();
        updateResultsCount(0);
        return;
      }

      // Render cards
      items.forEach(job => {
        const card = createJobCard(job);
        jobsGrid.appendChild(card);
      });

      // Update offset and results count
      currentOffset += items.length;
      updateResultsCount(totalJobs);

      // Manage Load More button
      if (loadMoreWrap && loadMoreBtn) {
        if (hasMoreJobs && items.length > 0) {
          loadMoreWrap.classList.remove('hidden');
          loadMoreBtn.disabled = false;
        } else {
          loadMoreWrap.classList.add('hidden');
        }
      }
    } catch (err) {
      console.error('[Jobs Client Network Error]:', err);
      renderErrorState('Network connection issue. Please check your internet and retry.', false);
    } finally {
      isLoading = false;
      setLoadMoreSpinner(false);
    }
  }

  // --- 429 Rate Limit Backoff Handler ---
  async function handleRateLimit(response, isInitial) {
    isLoading = false;
    setLoadMoreSpinner(false);

    const retryHeader = response.headers.get('retry-after');
    let waitSeconds = parseInt(retryHeader, 10);
    if (isNaN(waitSeconds) || waitSeconds <= 0) {
      waitSeconds = 5;
    }

    if (retryCount429 >= MAX_AUTO_RETRIES) {
      renderErrorState('High traffic volume. Please click Retry below in a moment.', false);
      retryCount429 = 0;
      return;
    }

    retryCount429++;
    renderRateLimitCountdown(waitSeconds, () => {
      fetchJobs(isInitial);
    });
  }

  function renderRateLimitCountdown(seconds, retryCallback) {
    clearInterval(countdownTimer);
    let remaining = seconds;

    if (jobsGrid && jobsGrid.children.length === 0) {
      jobsGrid.innerHTML = '';
    }

    if (statusContainer) {
      statusContainer.innerHTML = `
        <div class="rate-limit-banner" role="alert">
          <div class="flex items-center gap-2">
            <svg class="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.414-1.415L11 9.586V6z" clip-rule="evenodd" />
            </svg>
            <span>High request volume. Automatically retrying in <strong id="rateLimitCountdown" class="rate-limit-badge">${remaining}s</strong>...</span>
          </div>
          <button id="cancelRetryBtn" class="text-xs text-amber-800 underline hover:text-amber-950 font-medium">Cancel</button>
        </div>
      `;
      statusContainer.classList.remove('hidden');

      const cancelBtn = document.getElementById('cancelRetryBtn');
      if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
          clearInterval(countdownTimer);
          clearStatus();
          renderErrorState('Request cancelled.', false);
        });
      }
    }

    countdownTimer = setInterval(() => {
      remaining--;
      const badge = document.getElementById('rateLimitCountdown');
      if (badge) badge.textContent = `${remaining}s`;

      if (remaining <= 0) {
        clearInterval(countdownTimer);
        clearStatus();
        retryCallback();
      }
    }, 1000);
  }

  // --- Rendering UI States ---
  function renderSkeletons() {
    if (!jobsGrid) return;
    jobsGrid.innerHTML = '';
    for (let i = 0; i < 6; i++) {
      const card = document.createElement('div');
      card.className = 'skeleton-card';
      card.innerHTML = `
        <div class="flex items-center gap-3 mb-4">
          <div class="skeleton-box w-12 h-12 rounded-lg flex-shrink-0"></div>
          <div class="flex-1">
            <div class="skeleton-box h-4 w-3/4 mb-2"></div>
            <div class="skeleton-box h-3 w-1/2"></div>
          </div>
        </div>
        <div class="skeleton-box h-3 w-full mb-2"></div>
        <div class="skeleton-box h-3 w-4/5 mb-4"></div>
        <div class="flex gap-2 mb-4">
          <div class="skeleton-box h-5 w-16 rounded-full"></div>
          <div class="skeleton-box h-5 w-20 rounded-full"></div>
        </div>
        <div class="skeleton-box h-9 w-full rounded-md mt-auto"></div>
      `;
      jobsGrid.appendChild(card);
    }
  }

  function renderEmptyState() {
    clearStatus();
    if (!statusContainer) return;

    statusContainer.innerHTML = `
      <div class="jobs-status-panel">
        <div class="status-icon-wrap status-icon-empty">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 class="jobs-status-title">No jobs found</h2>
        <p class="jobs-status-desc">We couldn't find any listings matching your active filters. Try searching for different keywords or clearing some filters.</p>
        <button id="emptyClearFiltersBtn" class="btn-retry">Clear All Filters</button>
      </div>
    `;
    statusContainer.classList.remove('hidden');

    const btn = document.getElementById('emptyClearFiltersBtn');
    if (btn) btn.addEventListener('click', resetFilters);
  }

  function renderErrorState(message, isAuthError = false) {
    clearStatus();
    if (!statusContainer) return;

    statusContainer.innerHTML = `
      <div class="jobs-status-panel">
        <div class="status-icon-wrap status-icon-error">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h2 class="jobs-status-title">${isAuthError ? 'Service Temporarily Unavailable' : 'Failed to Load Jobs'}</h2>
        <p class="jobs-status-desc">${escapeHtml(message)}</p>
        ${isAuthError ? '' : '<button id="manualRetryBtn" class="btn-retry">Retry Now</button>'}
      </div>
    `;
    statusContainer.classList.remove('hidden');

    if (!isAuthError) {
      const btn = document.getElementById('manualRetryBtn');
      if (btn) btn.addEventListener('click', () => fetchJobs(true));
    }
  }

  function clearStatus() {
    clearInterval(countdownTimer);
    if (statusContainer) {
      statusContainer.innerHTML = '';
      statusContainer.classList.add('hidden');
    }
  }

  function updateResultsCount(count) {
    if (!resultsCountEl) return;
    if (count > 0) {
      resultsCountEl.innerHTML = `Showing <strong>${count}</strong> available positions in India`;
    } else {
      resultsCountEl.innerHTML = `Showing <strong>0</strong> positions`;
    }
  }

  function setLoadMoreSpinner(show) {
    if (!loadMoreBtn) return;
    if (show) {
      loadMoreBtn.disabled = true;
      loadMoreBtn.innerHTML = `
        <svg class="spinner-icon" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg>
        Loading more jobs...
      `;
    } else {
      loadMoreBtn.disabled = false;
      loadMoreBtn.innerHTML = `
        <span>Load More Jobs</span>
        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      `;
    }
  }

  // --- Job Card Creation ---
  function createJobCard(job) {
    const card = document.createElement('article');
    card.className = 'job-card';
    card.id = `job-${job.id || Math.random().toString(36).substr(2, 9)}`;

    const title = escapeHtml(job.title || 'Job Opening');
    const company = escapeHtml(job.company || 'Confidential Company');
    const jobUrl = job.url || '#';
    const logoUrl = job.logo;
    const isSaved = isJobBookmarked(job.id);

    // Location formatting
    const locationParts = [];
    if (job.city) locationParts.push(job.city);
    if (job.state) locationParts.push(job.state);
    if (job.country && !job.city && !job.state) locationParts.push(job.country);
    if (locationParts.length === 0 && job.location) locationParts.push(job.location);
    const locationText = escapeHtml(locationParts.join(', ') || 'India');

    // Relative date
    const postedText = getRelativeTime(job.posted_date || job.posted);

    // Salary formatting (hide row if both min & max are null)
    const salaryHtml = formatSalaryBadge(job.salary_min, job.salary_max, job.salary_curr);

    // Badges (Job Type, Work Mode)
    let badgesHtml = '';
    if (job.job_type) {
      const typeClass = getBadgeClass(job.job_type);
      badgesHtml += `<span class="job-badge ${typeClass}">${escapeHtml(job.job_type)}</span>`;
    }
    if (job.work_mode) {
      const modeClass = getBadgeClass(job.work_mode);
      badgesHtml += `<span class="job-badge ${modeClass}">${escapeHtml(job.work_mode)}</span>`;
    }

    // Skills chips (up to 4)
    let skillsHtml = '';
    const skills = Array.isArray(job.skills) ? job.skills.slice(0, 4) : [];
    if (skills.length > 0) {
      skillsHtml = `
        <div class="job-card-skills">
          ${skills.map(s => `<span class="job-skill-chip">${escapeHtml(s)}</span>`).join('')}
        </div>
      `;
    }

    // Plain-text sanitized description snippet
    const snippetText = getSafeSnippet(job.description, 115);
    const snippetHtml = snippetText ? `<p class="job-card-snippet">${escapeHtml(snippetText)}</p>` : '';

    // Company logo or Fallback avatar
    const { initial, gradient } = getCompanyAvatar(company);

    card.innerHTML = `
      <div>
        <div class="job-card-header">
          <div class="job-card-logo-wrap">
            ${logoUrl ? `
              <img src="${escapeHtml(logoUrl)}" 
                   alt="${company} Logo" 
                   class="job-card-logo" 
                   loading="lazy" 
                   width="48" 
                   height="48"
                   onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
              <div class="job-card-avatar" style="display:none; background:${gradient};">${initial}</div>
            ` : `
              <div class="job-card-avatar" style="background:${gradient};">${initial}</div>
            `}
          </div>
          <div class="job-card-meta">
            <h3 class="job-card-title">
              <a href="${escapeHtml(jobUrl)}" target="_blank" rel="noopener noreferrer">${title}</a>
            </h3>
            <p class="job-card-company">${company}</p>
          </div>
        </div>

        <div class="job-card-details">
          <span class="job-card-detail-item">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
            </svg>
            <span>${locationText}</span>
          </span>
          <span class="job-card-detail-item">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.414-1.415L11 9.586V6z" clip-rule="evenodd" />
            </svg>
            <span>${postedText}</span>
          </span>
        </div>

        ${badgesHtml ? `<div class="job-card-badges">${badgesHtml}</div>` : ''}
        ${salaryHtml}
        ${snippetHtml}
        ${skillsHtml}
      </div>

      <div class="job-card-footer">
        <a href="${escapeHtml(jobUrl)}" 
           target="_blank" 
           rel="noopener noreferrer" 
           class="btn-job-apply"
           aria-label="View and apply for ${title} at ${company}">
          <span>View &amp; Apply</span>
          <svg class="w-4 h-4 ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </a>
        <button class="btn-job-bookmark ${isSaved ? 'is-bookmarked' : ''}" 
                data-job-id="${escapeHtml(job.id || '')}"
                data-job-title="${title}"
                data-job-company="${company}"
                data-job-url="${escapeHtml(jobUrl)}"
                data-job-logo="${escapeHtml(logoUrl || '')}"
                data-job-location="${locationText}"
                data-job-type="${escapeHtml(job.job_type || '')}"
                aria-label="${isSaved ? 'Remove bookmark' : 'Bookmark this job'}"
                title="${isSaved ? 'Bookmarked' : 'Bookmark job'}">
          <svg fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
          </svg>
        </button>
      </div>
    `;

    return card;
  }

  // --- Helper Functions ---
  function formatSalaryBadge(min, max, curr) {
    const hasMin = min !== null && min !== undefined && Number(min) > 0;
    const hasMax = max !== null && max !== undefined && Number(max) > 0;

    if (!hasMin && !hasMax) return '';

    const currencySymbol = curr || '₹';
    let label = '';

    if (hasMin && hasMax) {
      label = `${currencySymbol} ${formatSalaryNumber(min)} - ${formatSalaryNumber(max)}`;
    } else if (hasMin) {
      label = `From ${currencySymbol} ${formatSalaryNumber(min)}`;
    } else {
      label = `Up to ${currencySymbol} ${formatSalaryNumber(max)}`;
    }

    return `
      <div class="job-card-salary">
        <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>${escapeHtml(label)}</span>
      </div>
    `;
  }

  function formatSalaryNumber(val) {
    const num = Number(val);
    if (isNaN(num)) return '';
    if (num >= 100000) {
      const lpa = (num / 100000).toFixed(1).replace(/\.0$/, '');
      return `${lpa} LPA`;
    }
    return num.toLocaleString('en-IN');
  }

  function getBadgeClass(str) {
    if (!str) return 'badge-onsite';
    const s = String(str).toLowerCase().trim();
    if (s.includes('full')) return 'badge-full-time';
    if (s.includes('intern')) return 'badge-internship';
    if (s.includes('part')) return 'badge-part-time';
    if (s.includes('contract')) return 'badge-contract';
    if (s.includes('remote')) return 'badge-remote';
    if (s.includes('hybrid')) return 'badge-hybrid';
    return 'badge-onsite';
  }

  function getRelativeTime(dateStr) {
    if (!dateStr) return 'Recently';
    const posted = new Date(dateStr);
    if (isNaN(posted.getTime())) return 'Recently';

    const diffMs = Date.now() - posted.getTime();
    const diffSec = Math.floor(diffMs / 1000);
    const diffMin = Math.floor(diffSec / 60);
    const diffHours = Math.floor(diffMin / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffDays > 30) {
      const months = Math.floor(diffDays / 30);
      return `${months} month${months > 1 ? 's' : ''} ago`;
    }
    if (diffDays > 0) {
      return diffDays === 1 ? '1 day ago' : `${diffDays} days ago`;
    }
    if (diffHours > 0) {
      return diffHours === 1 ? '1 hour ago' : `${diffHours} hours ago`;
    }
    if (diffMin > 0) {
      return `${diffMin} mins ago`;
    }
    return 'Just now';
  }

  function getCompanyAvatar(companyName) {
    const name = (companyName || 'C').trim();
    const initial = name.charAt(0).toUpperCase();
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    const gradient = AVATAR_GRADIENTS[Math.abs(hash) % AVATAR_GRADIENTS.length];
    return { initial, gradient };
  }

  function getSafeSnippet(htmlContent, maxLength = 120) {
    if (!htmlContent) return '';
    const cleanText = String(htmlContent)
      .replace(/<[^>]*>/g, ' ')
      .replace(/&nbsp;/gi, ' ')
      .replace(/&amp;/gi, '&')
      .replace(/&lt;/gi, '<')
      .replace(/&gt;/gi, '>')
      .replace(/&quot;/gi, '"')
      .replace(/&#39;/gi, "'")
      .replace(/\s+/g, ' ')
      .trim();

    if (cleanText.length > maxLength) {
      return cleanText.slice(0, maxLength).trim() + '...';
    }
    return cleanText;
  }

  function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // --- Bookmark Storage ---
  function loadBookmarks() {
    try {
      const saved = localStorage.getItem('bookmarkedJobs');
      bookmarkedJobs = saved ? JSON.parse(saved) : {};
    } catch {
      bookmarkedJobs = {};
    }
  }

  function saveBookmarks() {
    try {
      localStorage.setItem('bookmarkedJobs', JSON.stringify(bookmarkedJobs));
    } catch {
      // Storage unavailable or full
    }
  }

  function isJobBookmarked(id) {
    return Boolean(id && bookmarkedJobs[id]);
  }

  function toggleBookmark(job, btn) {
    if (!job || !job.id) return;

    if (bookmarkedJobs[job.id]) {
      delete bookmarkedJobs[job.id];
      btn.classList.remove('is-bookmarked');
      btn.setAttribute('aria-label', 'Bookmark this job');
      btn.title = 'Bookmark job';
    } else {
      bookmarkedJobs[job.id] = job;
      btn.classList.add('is-bookmarked');
      btn.setAttribute('aria-label', 'Remove bookmark');
      btn.title = 'Bookmarked';
    }
    saveBookmarks();
  }
})();