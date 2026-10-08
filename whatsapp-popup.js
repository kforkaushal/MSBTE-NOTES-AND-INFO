(function () {
    if (document.getElementById('whatsappPopup')) return;

    const popupHTML = `
    <div id="whatsappPopup"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 hidden transition-opacity duration-300 opacity-0"
        style="z-index: 9999; position: fixed; inset: 0; background-color: rgba(0, 0, 0, 0.6); display: none; align-items: center; justify-content: center; padding: 1rem;">
        <div class="bg-white rounded-2xl shadow-2xl p-6 max-w-sm w-full mx-auto text-center transform transition-all scale-95 relative"
            style="background: #ffffff; border-radius: 1.25rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); padding: 1.5rem; max-width: 24rem; width: 100%; text-align: center; position: relative;">
            
            <!-- Close 'x' button -->
            <button id="closePopupBtn" aria-label="Close popup"
                style="position: absolute; top: 0.75rem; right: 0.75rem; background: none; border: none; color: #9ca3af; font-size: 1.25rem; line-height: 1; cursor: pointer; padding: 0.25rem 0.5rem; border-radius: 9999px;">
                &times;
            </button>

            <!-- Bullseye Target Badge Icon -->
            <div style="display: flex; justify-content: center; margin-bottom: 0.75rem;">
                <div style="width: 3.25rem; height: 3.25rem; border-radius: 1rem; background: #fee2e2; color: #dc2626; display: flex; align-items: center; justify-content: center;">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 1.75rem; height: 1.75rem;">
                        <circle cx="12" cy="12" r="10"></circle>
                        <circle cx="12" cy="12" r="6"></circle>
                        <circle cx="12" cy="12" r="2"></circle>
                    </svg>
                </div>
            </div>

            <!-- Title -->
            <h3 style="font-size: 1.15rem; font-weight: 800; color: #111827; margin-bottom: 0.25rem; line-height: 1.3;">
                🎯 MSBTE IMPORTANT QUESTION BANK
            </h3>

            <!-- Subtitle -->
            <p style="color: #2563eb; font-weight: 700; font-size: 0.875rem; margin-bottom: 0.75rem;">
                📚 Exam Preparation Made Easier!
            </p>

            <!-- Description -->
            <p style="color: #4b5563; font-size: 0.875rem; line-height: 1.55; margin-bottom: 0.75rem;">
                Get our <strong>Important Question Bank</strong> prepared to help you focus on the most important questions for your MSBTE exams.
            </p>

            <!-- Limited Availability Pill -->
            <div style="display: inline-flex; align-items: center; gap: 0.35rem; background: #fffbeb; border: 1px solid #fde68a; color: #b45309; font-weight: 700; font-size: 0.75rem; padding: 0.25rem 0.75rem; border-radius: 9999px; margin-bottom: 1rem;">
                <span>🔥</span> Limited Availability
            </div>

            <!-- Contact Box -->
            <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 0.75rem; padding: 0.65rem 0.75rem; margin-bottom: 1rem; text-align: center;">
                <p style="font-size: 0.75rem; font-weight: 800; color: #1e40af; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.2rem;">
                    💬 Want the Question Bank?
                </p>
                <p style="font-size: 0.85rem; color: #374151; margin: 0;">
                    WhatsApp DM us on <a href="https://wa.me/917083236221?text=Hello%2C%20I%20want%20the%20MSBTE%20Important%20Question%20Bank" target="_blank" rel="noopener" style="color: #1d4ed8; font-weight: 800; text-decoration: underline;">70832 36221</a>
                </p>
            </div>

            <!-- Actions -->
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                <a href="https://wa.me/917083236221?text=Hello%2C%20I%20want%20the%20MSBTE%20Important%20Question%20Bank" target="_blank" rel="noopener"
                    id="joinWhatsappBtn"
                    style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; width: 100%; background-color: #22c55e; color: white; font-weight: 700; font-size: 0.95rem; padding: 0.85rem 1rem; border-radius: 0.75rem; text-decoration: none; transition: background-color 0.2s; box-shadow: 0 4px 6px -1px rgba(34, 197, 94, 0.2);"
                    onmouseover="this.style.backgroundColor='#16a34a'"
                    onmouseout="this.style.backgroundColor='#22c55e'">
                    <svg xmlns="http://www.w3.org/2000/svg" style="width: 1.25rem; height: 1.25rem;" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
                    <span>👉</span> WhatsApp DM Now
                </a>

                <button id="denyWhatsappBtn"
                    style="background: none; border: none; color: #9ca3af; font-size: 0.8rem; font-weight: 500; cursor: pointer; padding: 0.35rem 0; transition: color 0.2s;"
                    onmouseover="this.style.color='#4b5563'"
                    onmouseout="this.style.color='#9ca3af'">
                    Maybe Later
                </button>
            </div>
        </div>
    </div>
    `;

    const div = document.createElement('div');
    div.innerHTML = popupHTML;
    document.body.appendChild(div);

    const popup = document.getElementById('whatsappPopup');
    const joinBtn = document.getElementById('joinWhatsappBtn');
    const denyBtn = document.getElementById('denyWhatsappBtn');
    const closeBtn = document.getElementById('closePopupBtn');

    function showPopup() {
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

        localStorage.setItem('msbteQuestionBankPopupLastShown', new Date().getTime().toString());
    }

    if (joinBtn) joinBtn.addEventListener('click', closePopup);
    if (denyBtn) denyBtn.addEventListener('click', closePopup);
    if (closeBtn) closeBtn.addEventListener('click', closePopup);

    // Close on backdrop click
    popup.addEventListener('click', (e) => {
        if (e.target === popup) closePopup();
    });

    const lastShown = localStorage.getItem('msbteQuestionBankPopupLastShown');
    const now = new Date().getTime();
    const twentyFourHours = 24 * 60 * 60 * 1000;

    if (!lastShown || (now - parseInt(lastShown)) > twentyFourHours) {
        setTimeout(showPopup, 2000);
    }

})();