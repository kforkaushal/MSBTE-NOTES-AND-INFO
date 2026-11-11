/**
 * MSBTE Notes & Resources Portal - Interactive Directory & Search Engine
 * Features:
 * - Multi-dimensional hierarchical filtering: Branch, Year, Semester, Category
 * - Real-time full-text search with highlighting and clear button
 * - URL state synchronization (shareable search & folder filters)
 * - Mobile-first responsive touch interactions (min 44px touch targets)
 * - Zero emoji, clean SVG icons, high contrast typography
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const grid = document.getElementById('resource-grid');
    const searchInput = document.getElementById('search-input');
    const searchClearBtn = document.getElementById('search-clear-btn');
    const sortDropdown = document.getElementById('sort-dropdown');
    const noResults = document.getElementById('no-results');
    const resultsCountEl = document.getElementById('results-count');
    const activeFiltersBar = document.getElementById('active-filters-bar');
    const activeFiltersList = document.getElementById('active-filters-list');
    const clearAllFiltersBtn = document.getElementById('clear-all-filters-btn');
    const paginationContainer = document.getElementById('pagination-container');

    // Breadcrumb Elements
    const breadcrumbBranch = document.getElementById('breadcrumb-branch');
    const breadcrumbBranchSep = document.getElementById('breadcrumb-branch-sep');
    const breadcrumbSem = document.getElementById('breadcrumb-sem');
    const breadcrumbSemSep = document.getElementById('breadcrumb-sem-sep');

    // Filter Containers
    const branchContainer = document.getElementById('branch-filters');
    const yearContainer = document.getElementById('year-filters');
    const semesterContainer = document.getElementById('semester-filters');
    const categoryContainer = document.getElementById('category-filters');
    const folderCardsContainer = document.getElementById('folder-cards-grid');

    // State
    let resources = [];
    let currentPage = 1;
    const itemsPerPage = 12; // 12 items for clean 1/2/3/4-col grids

    let state = {
        branch: 'all',
        year: 'all',
        sem: 'all',
        category: 'all',
        search: '',
        sort: 'date-desc'
    };

    // Branch Definitions
    const BRANCHES = [
        { id: 'all', name: 'All Branches', short: 'All' },
        { id: 'common', name: 'First Year Common', short: 'FY' },
        { id: 'co', name: 'Computer Engg', short: 'CO' },
        { id: 'if', name: 'Information Tech', short: 'IF' },
        { id: 'an', name: 'AI & ML / DS', short: 'AN' },
        { id: 'me', name: 'Mechanical Engg', short: 'ME' },
        { id: 'ce', name: 'Civil Engg', short: 'CE' },
        { id: 'ee', name: 'Electrical Engg', short: 'EE' },
        { id: 'ej', name: 'Electronics & TC', short: 'EJ' }
    ];

    // Year Definitions
    const YEARS = [
        { id: 'all', name: 'All Years' },
        { id: '1', name: '1st Year (FY - Sem 1 & 2)' },
        { id: '2', name: '2nd Year (SY - Sem 3 & 4)' },
        { id: '3', name: '3rd Year (TY - Sem 5 & 6)' }
    ];

    // Semester Definitions
    const SEMESTERS = [
        { id: 'all', name: 'All Semesters', year: null },
        { id: '1', name: 'Sem 1', year: 1 },
        { id: '2', name: 'Sem 2', year: 1 },
        { id: '3', name: 'Sem 3', year: 2 },
        { id: '4', name: 'Sem 4', year: 2 },
        { id: '5', name: 'Sem 5', year: 3 },
        { id: '6', name: 'Sem 6', year: 3 }
    ];

    // Category Definitions
    const CATEGORIES = [
        { id: 'all', name: 'All Materials' },
        { id: 'notes', name: 'Notes' },
        { id: 'model-answer', name: 'Model Answers' },
        { id: 'question-bank', name: 'Question Banks' },
        { id: 'lab-manual', name: 'Lab Manuals' },
        { id: 'micro-project', name: 'Micro-Projects' },
        { id: 'subject-guide', name: 'Subject Guides' }
    ];

    // Fetch Resources
    async function fetchResources() {
        try {
            const response = await fetch('/Notes/resources.json');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            resources = await response.json();
            return resources;
        } catch (error) {
            console.error("Could not fetch resources:", error);
            grid.innerHTML = `
                <div class="col-span-full text-center py-12 bg-white rounded-2xl border border-red-100 p-8">
                    <p class="text-red-600 font-semibold mb-2">Unable to load study materials at this time.</p>
                    <p class="text-gray-500 text-sm mb-4">Please check your internet connection or reload the page.</p>
                    <button onclick="location.reload()" class="px-5 py-2.5 bg-blue-600 text-white rounded-xl font-medium text-sm hover:bg-blue-700 transition">
                        Retry Loading
                    </button>
                </div>`;
            return [];
        }
    }

    // Read URL Parameters on startup
    function readUrlParams() {
        const params = new URLSearchParams(window.location.search);
        if (params.has('branch')) state.branch = params.get('branch').toLowerCase();
        if (params.has('year')) state.year = params.get('year');
        if (params.has('sem')) state.sem = params.get('sem');
        if (params.has('type')) state.category = params.get('type').toLowerCase();
        if (params.has('sort')) state.sort = params.get('sort');
        if (params.has('q')) state.search = params.get('q');
        if (params.has('page')) currentPage = parseInt(params.get('page')) || 1;

        if (state.search && searchInput) {
            searchInput.value = state.search;
            if (searchClearBtn) searchClearBtn.classList.remove('hidden');
        }
        if (state.sort && sortDropdown) {
            sortDropdown.value = state.sort;
        }
    }

    // Sync State to URL
    function updateUrl() {
        const params = new URLSearchParams();
        if (state.branch !== 'all') params.set('branch', state.branch);
        if (state.year !== 'all') params.set('year', state.year);
        if (state.sem !== 'all') params.set('sem', state.sem);
        if (state.category !== 'all') params.set('type', state.category);
        if (state.sort !== 'date-desc') params.set('sort', state.sort);
        if (state.search.trim()) params.set('q', state.search.trim());
        if (currentPage > 1) params.set('page', currentPage);

        const newUrl = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
        window.history.replaceState({}, '', newUrl);
    }

    // Highlight search term in text safely
    function highlightText(text, term) {
        if (!text) return '';
        if (!term || !term.trim()) return text;
        const cleanTerm = term.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(`(${cleanTerm})`, 'gi');
        return text.replace(regex, `<mark class="bg-yellow-200 text-gray-900 rounded px-0.5">$1</mark>`);
    }

    // Category Badges Styling & SVGs
    function getCategoryBadge(category) {
        const config = {
            'notes': { label: 'Notes', bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
            'model-answer': { label: 'Model Answer', bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200' },
            'question-bank': { label: 'Question Bank', bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
            'lab-manual': { label: 'Lab Manual', bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-200' },
            'micro-project': { label: 'Micro-Project', bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-200' },
            'subject-guide': { label: 'Subject Guide', bg: 'bg-indigo-50', text: 'text-indigo-700', border: 'border-indigo-200' }
        };
        const c = config[category] || config['notes'];
        return `<span class="inline-flex items-center text-xs font-semibold px-2.5 py-0.5 rounded-full ${c.bg} ${c.text} border ${c.border}">
            ${c.label}
        </span>`;
    }

    // Category SVG Fallback Illustration
    function getCategoryFallbackIllustration(category, code, title) {
        const svgIcons = {
            'notes': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>',
            'model-answer': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>',
            'question-bank': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>',
            'lab-manual': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.977l-.51.342a6 6 0 01-3.86.977l-2.387.477a2 2 0 00-1.022.547m3.234-1.234a6 6 0 013.86-.977l1.022.204a2 2 0 011.022.547m-3.234-1.234a6 6 0 00-3.86.977l-1.022.204a2 2 0 00-1.022.547m10.234-4.234a6 6 0 01-3.86-.977l-.51-.342a6 6 0 00-3.86-.977l-2.387-.477a2 2 0 00-1.022.547m3.234-1.234a6 6 0 013.86-.977l1.022.204a2 2 0 011.022.547m-3.234-1.234a6 6 0 00-3.86.977l-1.022.204a2 2 0 00-1.022.547"/>',
            'micro-project': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>',
            'subject-guide': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>'
        };
        const icon = svgIcons[category] || svgIcons['notes'];

        return `
            <div class="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50/60 p-4 border-b border-gray-100 relative group-hover:from-blue-50/80 group-hover:to-indigo-50/80 transition-colors">
                <div class="w-12 h-12 rounded-xl bg-white shadow-sm border border-gray-100 flex items-center justify-center text-blue-600 mb-2 group-hover:scale-110 transition-transform">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">${icon}</svg>
                </div>
                ${code ? `<span class="text-xs font-mono font-bold text-gray-500 uppercase tracking-wider">${code}</span>` : ''}
            </div>
        `;
    }

    // Render Resources Grid
    function renderResources(items, searchTerm = '') {
        grid.innerHTML = '';

        if (items.length === 0) {
            noResults.classList.remove('hidden');
            grid.classList.add('hidden');
            return;
        }

        noResults.classList.add('hidden');
        grid.classList.remove('hidden');

        const fragment = document.createDocumentFragment();

        items.forEach((resource, index) => {
            const card = document.createElement('article');
            card.className = 'resource-card bg-white rounded-2xl shadow-sm border border-gray-200/80 hover:border-blue-300 overflow-hidden hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col h-full note-card-enter';
            card.style.animationDelay = `${Math.min(index * 35, 300)}ms`;

            const highlightedTitle = highlightText(resource.title, searchTerm);
            const highlightedDescription = highlightText(resource.description, searchTerm);

            // Thumbnail vs Fallback
            const hasCustomThumb = resource.thumbnail && 
                !resource.thumbnail.includes('MSBTE%20NOTES%20AND%20INFORMATION.png') &&
                !resource.thumbnail.includes('default');

            let thumbnailHTML;
            if (hasCustomThumb) {
                thumbnailHTML = `
                    <div class="relative w-full aspect-video overflow-hidden bg-gray-50 border-b border-gray-100">
                        <img src="${resource.thumbnail}" 
                             alt="${resource.title}" 
                             class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500" 
                             loading="lazy">
                    </div>
                `;
            } else {
                thumbnailHTML = `
                    <div class="relative w-full aspect-video overflow-hidden border-b border-gray-100">
                        ${getCategoryFallbackIllustration(resource.category, resource.code, resource.title)}
                    </div>
                `;
            }

            // Branch Badges
            let branchBadgesHTML = '';
            if (resource.branches && resource.branches.length > 0) {
                const branchList = resource.branches.includes('COMMON') ? ['Common'] : resource.branches.slice(0, 3);
                branchBadgesHTML = branchList.map(b => `
                    <span class="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-gray-100 text-gray-700 border border-gray-200">
                        ${b}
                    </span>
                `).join('');
            }

            // Semester Badge
            let semBadgeHTML = '';
            if (resource.semester) {
                semBadgeHTML = `
                    <span class="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-blue-50 text-blue-700 border border-blue-100">
                        Sem ${resource.semester}
                    </span>
                `;
            }

            // Code Badge
            let codeBadgeHTML = '';
            if (resource.code) {
                codeBadgeHTML = `
                    <span class="text-[11px] font-mono font-medium px-2 py-0.5 rounded-md bg-slate-100 text-slate-700">
                        ${highlightText(resource.code, searchTerm)}
                    </span>
                `;
            }

            card.innerHTML = `
                <a href="${resource.url}" class="flex flex-col h-full group focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-2xl">
                    ${thumbnailHTML}
                    <div class="p-5 flex-grow flex flex-col">
                        <!-- Top Metadata Row -->
                        <div class="flex flex-wrap items-center gap-1.5 mb-3">
                            ${getCategoryBadge(resource.category)}
                            ${semBadgeHTML}
                            ${codeBadgeHTML}
                            ${branchBadgesHTML}
                        </div>

                        <!-- Title -->
                        <h3 class="text-base md:text-lg font-bold text-gray-900 mb-2 leading-snug group-hover:text-blue-600 transition-colors line-clamp-2">
                            ${highlightedTitle}
                        </h3>

                        <!-- Description -->
                        <p class="text-xs md:text-sm text-gray-500 mb-4 line-clamp-3 leading-relaxed flex-grow">
                            ${highlightedDescription}
                        </p>

                        <!-- Bottom Action Link -->
                        <div class="mt-auto pt-3 border-t border-gray-100 flex items-center justify-between">
                            <span class="text-xs text-gray-400 font-medium">Free Verified PDF</span>
                            <span class="inline-flex items-center gap-1 text-xs md:text-sm font-semibold text-blue-600 group-hover:translate-x-1 transition-transform">
                                Open Study Material
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                                </svg>
                            </span>
                        </div>
                    </div>
                </a>
            `;

            fragment.appendChild(card);
        });

        grid.appendChild(fragment);
    }

    // Filter and Sort Engine
    function filterAndRender() {
        const searchTerm = state.search.trim().toLowerCase();

        let filtered = resources.filter(res => {
            // Category Filter
            if (state.category !== 'all' && res.category !== state.category) {
                return false;
            }

            // Year Filter
            if (state.year !== 'all') {
                const reqYear = parseInt(state.year);
                if (res.year && res.year !== reqYear) {
                    return false;
                }
            }

            // Semester Filter
            if (state.sem !== 'all') {
                const reqSem = parseInt(state.sem);
                if (res.semester && res.semester !== reqSem) {
                    return false;
                }
            }

            // Branch Filter
            if (state.branch !== 'all') {
                const reqBranch = state.branch.toUpperCase();
                const resBranches = res.branches || [];

                if (reqBranch === 'COMMON') {
                    const isCommon = resBranches.includes('COMMON') || (res.semester && res.semester <= 2);
                    if (!isCommon) return false;
                } else {
                    const matchesBranch = resBranches.includes(reqBranch) || resBranches.includes('COMMON');
                    if (!matchesBranch) return false;
                }
            }

            // Full-Text Search
            if (searchTerm) {
                const title = (res.title || '').toLowerCase();
                const desc = (res.description || '').toLowerCase();
                const code = (res.code || '').toLowerCase();
                const shortCode = (res.shortCode || '').toLowerCase();
                const tags = (res.tags || []).map(t => t.toLowerCase());

                // Multi-term matching (all terms in query must be present in at least one field)
                const terms = searchTerm.split(/\s+/).filter(Boolean);
                const matchesAllTerms = terms.every(term => 
                    title.includes(term) ||
                    desc.includes(term) ||
                    code.includes(term) ||
                    shortCode.includes(term) ||
                    tags.some(tag => tag.includes(term))
                );

                if (!matchesAllTerms) return false;
            }

            return true;
        });

        // Sorting Logic
        switch (state.sort) {
            case 'title-asc':
                filtered.sort((a, b) => a.title.localeCompare(b.title));
                break;
            case 'title-desc':
                filtered.sort((a, b) => b.title.localeCompare(a.title));
                break;
            case 'code-asc':
                filtered.sort((a, b) => (a.code || '999999').localeCompare(b.code || '999999'));
                break;
            case 'date-asc':
                filtered.sort((a, b) => new Date(a.dateAdded || '2026-01-01') - new Date(b.dateAdded || '2026-01-01'));
                break;
            case 'date-desc':
            default:
                filtered.sort((a, b) => new Date(b.dateAdded || '2026-01-01') - new Date(a.dateAdded || '2026-01-01'));
                break;
        }

        // Update Counter
        if (resultsCountEl) {
            resultsCountEl.textContent = `Showing ${filtered.length} of ${resources.length} resources`;
        }

        // Update Active Filters Status Bar
        renderActiveFiltersBar();

        // Update Breadcrumb Path
        updateBreadcrumb();

        // Paginate
        const totalPages = Math.ceil(filtered.length / itemsPerPage);
        if (currentPage > totalPages && totalPages > 0) currentPage = totalPages;
        if (currentPage < 1) currentPage = 1;

        const paginatedItems = filtered.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

        renderResources(paginatedItems, searchTerm);
        renderPagination(filtered.length);
        updateUrl();
    }

    // Active Filters Status Bar
    function renderActiveFiltersBar() {
        if (!activeFiltersBar || !activeFiltersList) return;

        const hasActiveFilter = state.branch !== 'all' || 
                               state.year !== 'all' || 
                               state.sem !== 'all' || 
                               state.category !== 'all' || 
                               Boolean(state.search.trim());

        if (!hasActiveFilter) {
            activeFiltersBar.classList.add('hidden');
            return;
        }

        activeFiltersBar.classList.remove('hidden');
        activeFiltersList.innerHTML = '';

        // Helper to add filter pill
        function addPill(label, onRemove) {
            const pill = document.createElement('span');
            pill.className = 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200';
            pill.innerHTML = `
                <span>${label}</span>
                <button type="button" class="hover:text-blue-900 focus:outline-none p-0.5 rounded-full" aria-label="Remove filter ${label}">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                </button>
            `;
            pill.querySelector('button').addEventListener('click', onRemove);
            activeFiltersList.appendChild(pill);
        }

        if (state.branch !== 'all') {
            const b = BRANCHES.find(item => item.id === state.branch);
            addPill(`Branch: ${b ? b.name : state.branch.toUpperCase()}`, () => {
                setBranch('all');
            });
        }

        if (state.year !== 'all') {
            addPill(`Year: ${state.year}${state.year === '1' ? 'st' : state.year === '2' ? 'nd' : 'rd'} Year`, () => {
                setYear('all');
            });
        }

        if (state.sem !== 'all') {
            addPill(`Semester: ${state.sem}`, () => {
                setSem('all');
            });
        }

        if (state.category !== 'all') {
            const c = CATEGORIES.find(item => item.id === state.category);
            addPill(`Type: ${c ? c.name : state.category}`, () => {
                setCategory('all');
            });
        }

        if (state.search.trim()) {
            addPill(`"${state.search.trim()}"`, () => {
                state.search = '';
                if (searchInput) searchInput.value = '';
                if (searchClearBtn) searchClearBtn.classList.add('hidden');
                currentPage = 1;
                filterAndRender();
            });
        }
    }

    // Update Breadcrumb Trail
    function updateBreadcrumb() {
        if (!breadcrumbBranch || !breadcrumbBranchSep) return;

        if (state.branch !== 'all') {
            const b = BRANCHES.find(item => item.id === state.branch);
            breadcrumbBranch.textContent = b ? b.name : state.branch.toUpperCase();
            breadcrumbBranch.classList.remove('hidden');
            breadcrumbBranchSep.classList.remove('hidden');
        } else {
            breadcrumbBranch.classList.add('hidden');
            breadcrumbBranchSep.classList.add('hidden');
        }

        if (state.sem !== 'all') {
            breadcrumbSem.textContent = `Semester ${state.sem}`;
            breadcrumbSem.classList.remove('hidden');
            breadcrumbSemSep.classList.remove('hidden');
        } else {
            breadcrumbSem.classList.add('hidden');
            breadcrumbSemSep.classList.add('hidden');
        }
    }

    // Accessible Pagination
    function renderPagination(totalItems) {
        paginationContainer.innerHTML = '';
        const totalPages = Math.ceil(totalItems / itemsPerPage);

        if (totalPages <= 1) return;

        // Previous Button
        const prevBtn = document.createElement('button');
        prevBtn.className = 'pagination-btn';
        prevBtn.innerHTML = `
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
            Prev
        `;
        prevBtn.disabled = currentPage === 1;
        prevBtn.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                filterAndRender();
                scrollToGrid();
            }
        });
        paginationContainer.appendChild(prevBtn);

        // Smart page numbers (show max 5 buttons around currentPage)
        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, currentPage + 2);

        if (startPage > 1) {
            const firstPageBtn = document.createElement('button');
            firstPageBtn.className = 'pagination-btn';
            firstPageBtn.textContent = '1';
            firstPageBtn.addEventListener('click', () => { currentPage = 1; filterAndRender(); scrollToGrid(); });
            paginationContainer.appendChild(firstPageBtn);

            if (startPage > 2) {
                const ellipsis = document.createElement('span');
                ellipsis.className = 'px-2 text-gray-400 font-bold';
                ellipsis.textContent = '…';
                paginationContainer.appendChild(ellipsis);
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            const pageBtn = document.createElement('button');
            pageBtn.className = `pagination-btn ${i === currentPage ? 'active' : ''}`;
            pageBtn.textContent = i;
            pageBtn.setAttribute('aria-label', `Page ${i}`);
            if (i === currentPage) pageBtn.setAttribute('aria-current', 'page');
            pageBtn.addEventListener('click', () => {
                currentPage = i;
                filterAndRender();
                scrollToGrid();
            });
            paginationContainer.appendChild(pageBtn);
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                const ellipsis = document.createElement('span');
                ellipsis.className = 'px-2 text-gray-400 font-bold';
                ellipsis.textContent = '…';
                paginationContainer.appendChild(ellipsis);
            }
            const lastPageBtn = document.createElement('button');
            lastPageBtn.className = 'pagination-btn';
            lastPageBtn.textContent = totalPages;
            lastPageBtn.addEventListener('click', () => { currentPage = totalPages; filterAndRender(); scrollToGrid(); });
            paginationContainer.appendChild(lastPageBtn);
        }

        // Next Button
        const nextBtn = document.createElement('button');
        nextBtn.className = 'pagination-btn';
        nextBtn.innerHTML = `
            Next
            <svg class="w-4 h-4 inline ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        `;
        nextBtn.disabled = currentPage === totalPages;
        nextBtn.addEventListener('click', () => {
            if (currentPage < totalPages) {
                currentPage++;
                filterAndRender();
                scrollToGrid();
            }
        });
        paginationContainer.appendChild(nextBtn);
    }

    // Smooth Scroll Helper
    function scrollToGrid() {
        const target = document.getElementById('resource-section-anchor') || grid;
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    // Setters for Filter States
    function setBranch(branchId) {
        state.branch = branchId;
        currentPage = 1;
        updateButtonsUI();
        filterAndRender();
    }

    function setYear(yearId) {
        state.year = yearId;
        // If year changes, check if sem is incompatible
        if (state.year !== 'all') {
            const y = parseInt(state.year);
            const validSems = y === 1 ? ['1', '2'] : (y === 2 ? ['3', '4'] : ['5', '6']);
            if (state.sem !== 'all' && !validSems.includes(state.sem)) {
                state.sem = 'all';
            }
        }
        currentPage = 1;
        updateButtonsUI();
        filterAndRender();
    }

    function setSem(semId) {
        state.sem = semId;
        // If sem is selected, auto-align year
        if (semId !== 'all') {
            const semNum = parseInt(semId);
            state.year = semNum <= 2 ? '1' : (semNum <= 4 ? '2' : '3');
        }
        currentPage = 1;
        updateButtonsUI();
        filterAndRender();
    }

    function setCategory(catId) {
        state.category = catId;
        currentPage = 1;
        updateButtonsUI();
        filterAndRender();
    }

    // Build & Sync Filter Button UIs
    function buildFilterControls() {
        // 1. Branch Buttons
        if (branchContainer) {
            branchContainer.innerHTML = '';
            BRANCHES.forEach(b => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = `filter-chip ${b.id === state.branch ? 'active' : ''}`;
                btn.dataset.branch = b.id;
                btn.textContent = b.name;
                btn.addEventListener('click', () => setBranch(b.id));
                branchContainer.appendChild(btn);
            });
        }

        // 2. Year Buttons
        if (yearContainer) {
            yearContainer.innerHTML = '';
            YEARS.forEach(y => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = `filter-chip ${y.id === state.year ? 'active' : ''}`;
                btn.dataset.year = y.id;
                btn.textContent = y.name;
                btn.addEventListener('click', () => setYear(y.id));
                yearContainer.appendChild(btn);
            });
        }

        // 3. Semester Buttons
        if (semesterContainer) {
            semesterContainer.innerHTML = '';
            SEMESTERS.forEach(s => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = `filter-chip ${s.id === state.sem ? 'active' : ''}`;
                btn.dataset.sem = s.id;
                btn.textContent = s.name;
                btn.addEventListener('click', () => setSem(s.id));
                semesterContainer.appendChild(btn);
            });
        }

        // 4. Category Buttons
        if (categoryContainer) {
            categoryContainer.innerHTML = '';
            CATEGORIES.forEach(c => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = `filter-chip ${c.id === state.category ? 'active' : ''}`;
                btn.dataset.cat = c.id;
                btn.textContent = c.name;
                btn.addEventListener('click', () => setCategory(c.id));
                categoryContainer.appendChild(btn);
            });
        }

        // 5. Folder Cards Clicks
        if (folderCardsContainer) {
            const folderCards = folderCardsContainer.querySelectorAll('[data-folder-branch]');
            folderCards.forEach(card => {
                card.addEventListener('click', (e) => {
                    e.preventDefault();
                    const branch = card.dataset.folderBranch;
                    const sem = card.dataset.folderSem;
                    const year = card.dataset.folderYear;

                    if (branch) state.branch = branch;
                    if (year) state.year = year;
                    if (sem) state.sem = sem;

                    currentPage = 1;
                    updateButtonsUI();
                    filterAndRender();
                    scrollToGrid();
                });
            });
        }
    }

    // Refresh active states of all buttons
    function updateButtonsUI() {
        if (branchContainer) {
            branchContainer.querySelectorAll('.filter-chip').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.branch === state.branch);
            });
        }
        if (yearContainer) {
            yearContainer.querySelectorAll('.filter-chip').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.year === state.year);
            });
        }
        if (semesterContainer) {
            semesterContainer.querySelectorAll('.filter-chip').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.sem === state.sem);
            });
        }
        if (categoryContainer) {
            categoryContainer.querySelectorAll('.filter-chip').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.cat === state.category);
            });
        }
        if (folderCardsContainer) {
            folderCardsContainer.querySelectorAll('[data-folder-branch]').forEach(card => {
                const matches = card.dataset.folderBranch === state.branch;
                card.classList.toggle('folder-active', matches);
            });
        }
    }

    // Debounce search input for performance
    let searchDebounceTimer = null;
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchDebounceTimer);
            const val = e.target.value;
            state.search = val;

            if (searchClearBtn) {
                searchClearBtn.classList.toggle('hidden', !val.trim());
            }

            searchDebounceTimer = setTimeout(() => {
                currentPage = 1;
                filterAndRender();
            }, 200);
        });

        // Keyboard Shortcut: press '/' to focus search, 'Escape' to clear
        document.addEventListener('keydown', (e) => {
            if (e.key === '/' && document.activeElement !== searchInput) {
                e.preventDefault();
                searchInput.focus();
                searchInput.select();
            } else if (e.key === 'Escape' && document.activeElement === searchInput) {
                if (searchInput.value) {
                    searchInput.value = '';
                    state.search = '';
                    if (searchClearBtn) searchClearBtn.classList.add('hidden');
                    filterAndRender();
                }
                searchInput.blur();
            }
        });
    }

    // Clear Search Button
    if (searchClearBtn) {
        searchClearBtn.addEventListener('click', () => {
            if (searchInput) {
                searchInput.value = '';
                searchInput.focus();
            }
            state.search = '';
            searchClearBtn.classList.add('hidden');
            currentPage = 1;
            filterAndRender();
        });
    }

    // Sort Dropdown
    if (sortDropdown) {
        sortDropdown.addEventListener('change', (e) => {
            state.sort = e.target.value;
            currentPage = 1;
            filterAndRender();
        });
    }

    // Clear All Filters Button
    if (clearAllFiltersBtn) {
        clearAllFiltersBtn.addEventListener('click', () => {
            state.branch = 'all';
            state.year = 'all';
            state.sem = 'all';
            state.category = 'all';
            state.search = '';
            if (searchInput) searchInput.value = '';
            if (searchClearBtn) searchClearBtn.classList.add('hidden');
            currentPage = 1;
            updateButtonsUI();
            filterAndRender();
        });
    }

    // Quick Search Tags (DSU, OSY, JPR, etc.)
    const quickTags = document.querySelectorAll('.quick-tag-chip');
    quickTags.forEach(tag => {
        tag.addEventListener('click', () => {
            const query = tag.dataset.query;
            if (query && searchInput) {
                searchInput.value = query;
                state.search = query;
                if (searchClearBtn) searchClearBtn.classList.remove('hidden');
                currentPage = 1;
                filterAndRender();
                scrollToGrid();
            }
        });
    });

    // Mobile Menu Toggle
    window.toggleMobileMenu = function() {
        const menu = document.getElementById('mobileNav');
        const button = document.querySelector('button[onclick="toggleMobileMenu()"]');
        if (menu) {
            menu.classList.toggle('hidden');
            const isExpanded = !menu.classList.contains('hidden');
            if (button) button.setAttribute('aria-expanded', isExpanded);
        }
    };

    // Initialize Everything
    async function init() {
        readUrlParams();
        buildFilterControls();
        updateButtonsUI();

        await fetchResources();

        // Hide pre-loader if present
        const preloader = document.getElementById('notes-loading-state');
        if (preloader) preloader.remove();

        filterAndRender();
    }

    init();
});
