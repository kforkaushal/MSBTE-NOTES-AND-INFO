const http = require('http');
const { spawn } = require('child_process');

function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

async function waitForHttp(url, maxAttempts = 20) {
    for (let i = 0; i < maxAttempts; i++) {
        try {
            await new Promise((resolve, reject) => {
                const req = http.get(url, (res) => {
                    if (res.statusCode === 200) resolve();
                    else reject(new Error('status ' + res.statusCode));
                });
                req.on('error', reject);
                req.setTimeout(500, () => {
                    req.destroy();
                    reject(new Error('timeout'));
                });
            });
            return true;
        } catch (e) {
            await sleep(300);
        }
    }
    return false;
}

async function getWebSocketDebuggerUrl() {
    return new Promise((resolve, reject) => {
        http.get('http://127.0.0.1:9222/json/list', (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    if (json.length > 0 && json[0].webSocketDebuggerUrl) {
                        resolve(json[0].webSocketDebuggerUrl);
                    } else {
                        reject(new Error('No target with webSocketDebuggerUrl found: ' + data));
                    }
                } catch (e) {
                    reject(new Error('Parse error: ' + data + ' ' + e.message));
                }
            });
        }).on('error', reject);
    });
}

class CDPClient {
    constructor(wsUrl) {
        this.ws = new WebSocket(wsUrl);
        this.id = 1;
        this.callbacks = new Map();
    }

    async connect() {
        return new Promise((resolve, reject) => {
            this.ws.onopen = resolve;
            this.ws.onerror = reject;
            this.ws.onmessage = (event) => {
                const msg = JSON.parse(event.data);
                if (msg.id && this.callbacks.has(msg.id)) {
                    const cb = this.callbacks.get(msg.id);
                    this.callbacks.delete(msg.id);
                    if (msg.error) cb.reject(msg.error);
                    else cb.resolve(msg.result);
                }
            };
        });
    }

    send(method, params = {}) {
        const id = this.id++;
        return new Promise((resolve, reject) => {
            this.callbacks.set(id, { resolve, reject });
            this.ws.send(JSON.stringify({ id, method, params }));
        });
    }

    async eval(expr) {
        const res = await this.send('Runtime.evaluate', {
            expression: expr,
            awaitPromise: true,
            returnByValue: true
        });
        if (res.exceptionDetails) {
            throw new Error(JSON.stringify(res.exceptionDetails));
        }
        return res.result ? res.result.value : undefined;
    }

    async setViewport(width, height) {
        await this.send('Emulation.setDeviceMetricsOverride', {
            width,
            height,
            deviceScaleFactor: 2,
            mobile: width < 900
        });
    }

    async navigate(url) {
        await this.send('Page.navigate', { url });
        await sleep(2000);
    }

    close() {
        this.ws.close();
    }
}

async function runMobileAudit() {
    console.log('Starting HTTP server...');
    const serverProc = spawn('python', ['-m', 'http.server', '3000', '--bind', '127.0.0.1']);
    await waitForHttp('http://127.0.0.1:3000/');

    console.log('Starting headless Chrome...');
    const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
    const chromeProc = spawn(chromePath, [
        '--headless=new',
        '--remote-debugging-port=9222',
        '--user-data-dir=C:\\tmp\\chrome-cdp-mobile-audit',
        '--disable-gpu',
        'about:blank'
    ]);

    await waitForHttp('http://127.0.0.1:9222/json/version');

    let client;
    try {
        const wsUrl = await getWebSocketDebuggerUrl();
        client = new CDPClient(wsUrl);
        await client.connect();
        await client.send('Page.enable');
        await client.send('Network.enable');
        await client.send('Network.setCacheDisabled', { cacheDisabled: true });

        const viewports = [
            { name: 'Ultra-compact Phone (320px)', width: 320, height: 600 },
            { name: 'Small Android (360px)', width: 360, height: 740 },
            { name: 'iPhone SE / Mini (375px)', width: 375, height: 667 },
            { name: 'Standard iPhone 14 (390px)', width: 390, height: 844 },
            { name: 'Pixel 7 (412px)', width: 412, height: 915 },
            { name: 'Tablet Portrait (768px)', width: 768, height: 1024 },
            { name: 'Desktop (1280px)', width: 1280, height: 800 }
        ];

        console.log('\n======================================================');
        console.log('MOBILE AUDIT: Notes/index.html');
        console.log('======================================================');

        for (const vp of viewports) {
            await client.setViewport(vp.width, vp.height);
            await client.navigate('http://127.0.0.1:3000/Notes/index.html');

            const audit = await client.eval(`
                (() => {
                    const scrollW = document.documentElement.scrollWidth;
                    const innerW = window.innerWidth;
                    const hasHScroll = scrollW > innerW;

                    // Find all overflowing elements
                    const overflowingElements = [];
                    document.querySelectorAll('*').forEach(el => {
                        const r = el.getBoundingClientRect();
                        if (r.right > innerW + 1) { // 1px margin for subpixel
                            overflowingElements.push({
                                tag: el.tagName.toLowerCase(),
                                id: el.id || '',
                                class: (el.className && typeof el.className === 'string') ? el.className.slice(0, 50) : '',
                                width: Math.round(r.width),
                                right: Math.round(r.right),
                                overflowBy: Math.round(r.right - innerW)
                            });
                        }
                    });

                    // Input font-size check for iOS zoom (must be >= 16px)
                    const searchInput = document.querySelector('#search-input');
                    const searchFontSize = searchInput ? window.getComputedStyle(searchInput).fontSize : null;

                    // Touch target sizes
                    const touchTargets = [];
                    document.querySelectorAll('button, a, input, select, .folder-card').forEach(el => {
                        const r = el.getBoundingClientRect();
                        if (r.width > 0 && r.height > 0 && (r.width < 44 || r.height < 44)) {
                            // Check if inside visible area
                            if (r.top < window.innerHeight && r.bottom > 0) {
                                touchTargets.push({
                                    tag: el.tagName.toLowerCase(),
                                    text: el.textContent.trim().slice(0, 20),
                                    w: Math.round(r.width),
                                    h: Math.round(r.height)
                                });
                            }
                        }
                    });

                    // Check resource grid column count
                    const firstCard = document.querySelector('#resource-grid .resource-card');
                    const grid = document.querySelector('#resource-grid');
                    const cols = (firstCard && grid) ? Math.round(grid.getBoundingClientRect().width / firstCard.getBoundingClientRect().width) : 0;

                    return {
                        scrollW,
                        innerW,
                        hasHScroll,
                        overflowCount: overflowingElements.length,
                        overflowSample: overflowingElements.slice(0, 3),
                        searchFontSize,
                        smallTouchTargetsCount: touchTargets.length,
                        smallTouchTargetsSample: touchTargets.slice(0, 5),
                        gridColumns: cols
                    };
                })()
            `);

            console.log('\n[' + vp.name + ']:');
            console.log('  - Horizontal overflow: ' + (audit.hasHScroll ? 'FAIL (scrollWidth=' + audit.scrollW + ', innerWidth=' + audit.innerW + ')' : 'PASS (no scrollbar)'));
            if (audit.overflowCount > 0) {
                console.log('  - Overflowing elements (' + audit.overflowCount + '):', audit.overflowSample);
            }
            console.log('  - Search input font-size: ' + audit.searchFontSize + ' (' + (parseFloat(audit.searchFontSize) >= 16 ? 'PASS: No iOS auto-zoom' : 'WARN: May trigger iOS auto-zoom') + ')');
            console.log('  - Grid columns: ' + audit.gridColumns);
            console.log('  - Small touch targets in viewport: ' + audit.smallTouchTargetsCount);
        }

        console.log('\n======================================================');
        console.log('MOBILE AUDIT: index.html (#notes section)');
        console.log('======================================================');

        for (const vp of [viewports[0], viewports[2], viewports[6]]) {
            await client.setViewport(vp.width, vp.height);
            await client.navigate('http://127.0.0.1:3000/index.html#notes');

            const homeAudit = await client.eval(`
                (() => {
                    const scrollW = document.documentElement.scrollWidth;
                    const innerW = window.innerWidth;
                    const hasHScroll = scrollW > innerW;

                    const searchInput = document.querySelector('#searchInput');
                    const searchFontSize = searchInput ? window.getComputedStyle(searchInput).fontSize : null;

                    const grid = document.querySelector('#notesGrid');
                    const firstCard = document.querySelector('#notesGrid > div');
                    const cols = (firstCard && grid) ? Math.round(grid.getBoundingClientRect().width / firstCard.getBoundingClientRect().width) : 0;

                    return {
                        scrollW,
                        innerW,
                        hasHScroll,
                        searchFontSize,
                        gridColumns: cols
                    };
                })()
            `);

            console.log('\n[' + vp.name + ']:');
            console.log('  - Horizontal overflow: ' + (homeAudit.hasHScroll ? 'FAIL' : 'PASS'));
            console.log('  - Search font-size: ' + homeAudit.searchFontSize);
            console.log('  - Grid columns: ' + homeAudit.gridColumns);
        }

    } catch (e) {
        console.error('Audit error:', e);
    } finally {
        if (client) client.close();
        chromeProc.kill();
        serverProc.kill();
    }
}

runMobileAudit();
