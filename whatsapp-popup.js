(function () {
    if (document.getElementById('whatsappPopup')) return;

    const popupHTML = `
    <div id="whatsappPopup"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 hidden transition-opacity duration-300 opacity-0"
        style="z-index: 99999; position: fixed; inset: 0; background-color: rgba(0, 0, 0, 0.65); backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px); display: none; align-items: center; justify-content: center; padding: 1rem;">
        <div class="bg-white rounded-2xl shadow-2xl p-6 max-w-sm w-full mx-auto text-center transform transition-all scale-95 relative"
            style="background: #ffffff; border-radius: 1.25rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); padding: 1.75rem 1.5rem; max-width: 24rem; width: 100%; text-align: center; position: relative; border: 1px solid #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
            
            <!-- Close 'x' button -->
            <button id="closePopupBtn" aria-label="Close popup"
                style="position: absolute; top: 0.75rem; right: 0.75rem; background: none; border: none; color: #9ca3af; font-size: 1.5rem; line-height: 1; cursor: pointer; padding: 0.25rem 0.5rem; border-radius: 9999px; transition: color 0.2s;"
                onmouseover="this.style.color='#1f2937'"
                onmouseout="this.style.color='#9ca3af'">
                &times;
            </button>

            <!-- WhatsApp Community Badge Icon -->
            <div style="display: flex; justify-content: center; margin-bottom: 0.85rem;">
                <div style="width: 3.5rem; height: 3.5rem; border-radius: 1rem; background: #dcfce7; color: #16a34a; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 14px rgba(22, 163, 74, 0.18);">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" style="width: 2rem; height: 2rem; fill: #16a34a;" aria-hidden="true">
                        <path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/>
                    </svg>
                </div>
            </div>

            <!-- Official Badge Pill -->
            <div style="display: inline-flex; align-items: center; gap: 0.35rem; background: #f0fdf4; border: 1px solid #bbf7d0; color: #15803d; font-weight: 700; font-size: 0.72rem; padding: 0.2rem 0.65rem; border-radius: 9999px; margin-bottom: 0.65rem; text-transform: uppercase; letter-spacing: 0.04em;">
                <span style="display: inline-block; width: 0.5rem; height: 0.5rem; border-radius: 9999px; background: #22c55e;"></span>
                Official MNI Community
            </div>

            <!-- Title / Question -->
            <h3 style="font-size: 1.15rem; font-weight: 800; color: #111827; margin: 0 0 0.45rem 0; line-height: 1.35;">
                Are you joined to our official MNI community to get daily updates?
            </h3>

            <!-- Subtitle / Value Proposition -->
            <p style="color: #4b5563; font-size: 0.85rem; line-height: 1.5; margin: 0 0 1.25rem 0;">
                Get real-time MSBTE exam timetables, verified model answers, syllabus circulars, and study notes directly on WhatsApp.
            </p>

            <!-- Actions -->
            <div style="display: flex; flex-direction: column; gap: 0.6rem;">
                <a href="https://whatsapp.com/channel/0029Vap8lWS3QxRxxdmaSR36" target="_blank" rel="noopener noreferrer"
                    id="followWhatsappBtn"
                    style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; width: 100%; background: #22c55e; background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: #ffffff; font-weight: 700; font-size: 0.95rem; padding: 0.8rem 1rem; border-radius: 0.75rem; text-decoration: none; box-shadow: 0 4px 12px rgba(34, 197, 94, 0.32); transition: all 0.2s;"
                    onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 6px 16px rgba(34, 197, 94, 0.42)'"
                    onmouseout="this.style.transform='none'; this.style.boxShadow='0 4px 12px rgba(34, 197, 94, 0.32)'">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" style="width: 1.2rem; height: 1.2rem; fill: #ffffff;" aria-hidden="true">
                        <path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/>
                    </svg>
                    <span>Follow</span>
                </a>

                <button id="alreadyFollowedBtn"
                    style="width: 100%; background: #f8fafc; color: #4b5563; font-weight: 600; font-size: 0.85rem; padding: 0.65rem 1rem; border: 1px solid #e2e8f0; border-radius: 0.75rem; cursor: pointer; transition: all 0.2s;"
                    onmouseover="this.style.backgroundColor='#e2e8f0'; this.style.color='#111827'"
                    onmouseout="this.style.backgroundColor='#f8fafc'; this.style.color='#4b5563'">
                    I'm already followed
                </button>
            </div>
        </div>
    </div>
    `;

    const div = document.createElement('div');
    div.innerHTML = popupHTML;
    document.body.appendChild(div);

    const popup = document.getElementById('whatsappPopup');
    const followBtn = document.getElementById('followWhatsappBtn');
    const alreadyBtn = document.getElementById('alreadyFollowedBtn');
    const closeBtn = document.getElementById('closePopupBtn');

    function showPopup() {
        if (!popup) return;
        popup.classList.remove('hidden');
        popup.style.display = 'flex';

        setTimeout(() => {
            popup.classList.remove('opacity-0');
            popup.style.opacity = '1';

            const content = popup.firstElementChild || popup.querySelector('div');
            if (content) {
                content.classList.remove('scale-95');
                content.classList.add('scale-100');
                content.style.transform = 'scale(1)';
            }
        }, 10);
    }

    function closePopup() {
        if (!popup) return;
        popup.classList.add('opacity-0');
        popup.style.opacity = '0';

        const content = popup.firstElementChild || popup.querySelector('div');
        if (content) {
            content.classList.remove('scale-100');
            content.classList.add('scale-95');
            content.style.transform = 'scale(0.95)';
        }

        setTimeout(() => {
            popup.classList.add('hidden');
            popup.style.display = 'none';
        }, 300);
    }

    if (followBtn) {
        followBtn.addEventListener('click', () => {
            localStorage.setItem('mniCommunityPopupFollowed', 'true');
            closePopup();
        });
    }

    if (alreadyBtn) {
        alreadyBtn.addEventListener('click', () => {
            localStorage.setItem('mniCommunityPopupFollowed', 'true');
            closePopup();
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            localStorage.setItem('mniCommunityPopupLastDismissed', Date.now().toString());
            closePopup();
        });
    }

    // Close on backdrop click
    popup.addEventListener('click', (e) => {
        if (e.target === popup) {
            localStorage.setItem('mniCommunityPopupLastDismissed', Date.now().toString());
            closePopup();
        }
    });

    const isFollowed = localStorage.getItem('mniCommunityPopupFollowed') === 'true';
    const lastDismissed = localStorage.getItem('mniCommunityPopupLastDismissed');
    const now = Date.now();
    const twentyFourHours = 24 * 60 * 60 * 1000;

    if (!isFollowed) {
        if (!lastDismissed || (now - parseInt(lastDismissed, 10)) > twentyFourHours) {
            setTimeout(showPopup, 2000);
        }
    }

})();
