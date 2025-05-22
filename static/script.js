document.addEventListener('DOMContentLoaded', function() {
    const inputBox = document.getElementById('inputBox');
    const chatBox = document.getElementById('chatBox');
    const editTitle = document.getElementById('editTitle');
    const editBox = document.getElementById('editBox');
    const submitBtn = document.getElementById('editSubmitBtn');
    const spinner = document.getElementById('spinner');

    inputBox.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && inputBox.value.trim() !== '') {
            const msg = document.createElement('div');
            msg.className = 'message';
            // Generate timestamp
            const now = new Date();
            const timestamp = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            msg.innerHTML = `<span class="msg-text">${inputBox.value}</span> <span class="msg-time">${timestamp}</span>`;
            msg.dataset.timestamp = now.toISOString();
            chatBox.insertBefore(msg, chatBox.firstChild);
            chatBox.scrollTop = 0;
            inputBox.value = '';
        }
    });

    // Modal elements
    let modal = document.getElementById('aiModal');
    let modalContent = document.getElementById('aiModalContent');
    let modalClose = document.getElementById('aiModalClose');

    function showModal(content) {
        modalContent.textContent = content;
        modal.style.display = 'block';
    }
    modalClose.onclick = function() {
        modal.style.display = 'none';
    }
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    submitBtn.addEventListener('click', async function() {
        spinner.style.display = 'inline-block';
        submitBtn.disabled = true;
        try {
            // Collect chat messages (bottom to top)
            const messages = Array.from(document.querySelectorAll('#chatBox .message'))
                .reverse()
                .map(msg => ({
                    date: msg.dataset.timestamp || '', // Use stored ISO timestamp
                    chat_log: msg.querySelector('.msg-text') ? msg.querySelector('.msg-text').textContent : msg.textContent
                }));

            const payload = {
                ticket_id: editTitle.value,
                initial_request: editBox.value,
                request_updates: messages,
                // Optionally, you can add a date field here
            };

            const response = await fetch('/generate_document', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            showModal(data.document);
        } finally {
            spinner.style.display = 'none';
            submitBtn.disabled = false;
        }
    });
});
