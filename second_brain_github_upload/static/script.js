const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Add chip logic
document.querySelectorAll('.prompt-chip').forEach(chip => {
    chip.addEventListener('click', () => {
        userInput.value = chip.textContent;
        userInput.style.height = 'auto';
        userInput.style.height = (userInput.scrollHeight) + 'px';
        userInput.focus();
    });
});

// Auto-resize textarea
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Handle enter key
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

async function sendMessage() {
    const text = userInput.value.trim();

    if (!text) return;

    // Aggiungi messaggio utente
    appendMessage(text, 'user');
    userInput.value = '';
    userInput.style.height = 'auto';

    // Aggiungi loader AI
    const loaderId = 'loader-' + Date.now();
    appendLoader(loaderId);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: text
            })
        });

        const data = await response.json();
        
        // Rimuovi loader
        document.getElementById(loaderId).remove();

        if (response.ok) {
            appendMessage(data.answer, 'ai', data.context);
        } else {
            appendMessage("Errore: " + data.error, 'ai');
        }
    } catch (err) {
        document.getElementById(loaderId).remove();
        appendMessage("Errore di connessione al server locale.", 'ai');
    }
}

function appendMessage(text, sender, context = null) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}-message`;
    
    let avatar = sender === 'user' ? 'TU' : 'AI';
    
    // Format testo per l'AI
    let formattedText = text;
    // Sostituiamo gli a capo con <br> (se non c'è già HTML)
    if (!formattedText.includes('<br>') && !formattedText.includes('</p>')) {
        formattedText = formattedText.replace(/\n/g, '<br>');
    }
    
    let contextHtml = '';
    if (context) {
        contextHtml = `<details class="context-block">
            <summary style="cursor: pointer; font-weight: bold;">[+] Visualizza le Fonti estratte</summary>
            <div style="margin-top: 10px; white-space: pre-wrap;">${context}</div>
        </details>`;
    }

    let copyBtnHtml = '';
    if (sender === 'ai') {
        copyBtnHtml = `
            <button class="copy-btn" onclick="copyToClipboard(this)" title="Copia negli appunti">
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
            </button>
        `;
    }

    msgDiv.innerHTML = `
        <div class="avatar">${avatar}</div>
        <div class="bubble">
            ${formattedText}
            ${contextHtml}
            ${copyBtnHtml}
        </div>
    `;
    
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Copy button function
window.copyToClipboard = function(btn) {
    const bubble = btn.closest('.bubble');
    const clone = bubble.cloneNode(true);
    
    // Rimuovi la sezione context se presente e il pulsante copia stesso
    const details = clone.querySelector('details');
    if (details) details.remove();
    const copyBtn = clone.querySelector('.copy-btn');
    if (copyBtn) copyBtn.remove();
    
    // Preserva i ritorni a capo sostituendo i <br> con \n
    let textToCopy = clone.innerHTML.replace(/<br\s*[\/]?>/gi, '\n');
    
    // Rimuovi eventuali tag HTML rimanenti
    const tmp = document.createElement('div');
    tmp.innerHTML = textToCopy;
    textToCopy = tmp.textContent || tmp.innerText || "";
    textToCopy = textToCopy.trim();
    
    const handleSuccess = () => {
        const originalHtml = btn.innerHTML;
        btn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg> Copiato!';
        btn.classList.add('copied');
        setTimeout(() => {
            btn.innerHTML = originalHtml;
            btn.classList.remove('copied');
        }, 2000);
    };

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(textToCopy).then(handleSuccess).catch(err => console.error("Errore clipboard:", err));
    } else {
        // Fallback per reti locali (HTTP senza localhost) come sul cellulare
        const textArea = document.createElement("textarea");
        textArea.value = textToCopy;
        
        // Evita lo scrolling su mobile
        textArea.style.position = "fixed";
        textArea.style.top = "0";
        textArea.style.left = "0";
        textArea.style.opacity = "0";
        
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            handleSuccess();
        } catch (err) {
            console.error('Errore fallback clipboard:', err);
        }
        
        document.body.removeChild(textArea);
    }
}

function appendLoader(id) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ai-message`;
    msgDiv.id = id;
    
    msgDiv.innerHTML = `
        <div class="avatar">AI</div>
        <div class="bubble">
            Sto frugando tra i tuoi file... <span class="typing-indicator"></span>
        </div>
    `;
    
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
