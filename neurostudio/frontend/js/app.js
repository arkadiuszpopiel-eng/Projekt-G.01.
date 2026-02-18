/**
 * NeuroForge - Frontend Application
 * Handles WebSocket chat, model management, and UI interactions.
 */

// ──── State ────
const state = {
    ws: null,
    sessionId: null,
    connected: false,
    modelLoaded: false,
    sending: false,
};

// ──── DOM Elements ────
const $ = (id) => document.getElementById(id);
const chatMessages = $('chat-messages');
const chatInput = $('chat-input');
const btnSend = $('btn-send');
const btnNewChat = $('btn-new-chat');
const modelSelect = $('model-select');
const btnLoadModel = $('btn-load-model');
const btnUnloadModel = $('btn-unload-model');
const statusDot = $('status-dot');
const statusText = $('status-text');
const typingIndicator = $('typing-indicator');
const sidebarToggle = $('sidebar-toggle');
const sidebar = $('sidebar');
const tempSlider = $('temperature');
const tempValue = $('temp-value');

// ──── Initialize ────
document.addEventListener('DOMContentLoaded', () => {
    connectWebSocket();
    loadModels();
    loadRecommendedModels();
    loadStatus();
    setupEventListeners();
});

// ──── WebSocket ────
function connectWebSocket() {
    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${location.host}/ws/chat`;

    state.ws = new WebSocket(wsUrl);

    state.ws.onopen = () => {
        state.connected = true;
        console.log('WebSocket connected');
    };

    state.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWSMessage(data);
    };

    state.ws.onclose = () => {
        state.connected = false;
        console.log('WebSocket disconnected, reconnecting in 3s...');
        setTimeout(connectWebSocket, 3000);
    };

    state.ws.onerror = (err) => {
        console.error('WebSocket error:', err);
    };
}

function handleWSMessage(data) {
    switch (data.type) {
        case 'session':
            state.sessionId = data.session_id;
            break;

        case 'text':
            appendAssistantText(data.content);
            break;

        case 'tool_call':
            appendToolCall(data.tool, data.args);
            break;

        case 'tool_result':
            appendToolResult(data.tool, data.result);
            break;

        case 'model_switch':
            appendModelSwitch(data.from, data.to);
            break;

        case 'error':
            appendError(data.message);
            break;

        case 'done':
            state.sending = false;
            btnSend.disabled = false;
            typingIndicator.classList.add('hidden');
            scrollToBottom();
            break;

        case 'cleared':
            clearChat();
            break;
    }
}

function sendMessage(text) {
    if (!state.ws || state.ws.readyState !== WebSocket.OPEN) {
        appendError('Brak polaczenia z serwerem. Odswież strone.');
        return;
    }
    if (!text.trim()) return;

    state.sending = true;
    btnSend.disabled = true;
    typingIndicator.classList.remove('hidden');

    // Remove welcome message
    const welcome = chatMessages.querySelector('.welcome-message');
    if (welcome) welcome.remove();

    // Add user message to UI
    appendUserMessage(text);

    // Send via WebSocket
    state.ws.send(JSON.stringify({ type: 'message', content: text }));

    // Clear input
    chatInput.value = '';
    chatInput.style.height = 'auto';
}

// ──── Message Rendering ────

let currentAssistantEl = null;

function appendUserMessage(text) {
    currentAssistantEl = null;
    const el = document.createElement('div');
    el.className = 'message user';
    el.innerHTML = `
        <div class="message-avatar">U</div>
        <div class="message-content"><p>${escapeHtml(text)}</p></div>
    `;
    chatMessages.appendChild(el);
    scrollToBottom();
}

function appendAssistantText(text) {
    if (!currentAssistantEl) {
        const el = document.createElement('div');
        el.className = 'message assistant';
        el.innerHTML = `
            <div class="message-avatar">AI</div>
            <div class="message-content"></div>
        `;
        chatMessages.appendChild(el);
        currentAssistantEl = el.querySelector('.message-content');
    }

    // Render markdown-like content
    const rendered = renderMarkdown(text);
    const p = document.createElement('div');
    p.innerHTML = rendered;
    currentAssistantEl.appendChild(p);
    scrollToBottom();
}

function appendToolCall(toolName, args) {
    if (!currentAssistantEl) {
        appendAssistantText('');
    }

    const el = document.createElement('div');
    el.className = 'tool-call';

    const argsStr = Object.entries(args || {})
        .map(([k, v]) => `${k}: ${typeof v === 'string' ? v : JSON.stringify(v)}`)
        .join('\n');

    el.innerHTML = `
        <div class="tool-call-header" onclick="this.nextElementSibling.classList.toggle('hidden')">
            &#9881; ${escapeHtml(toolName)}
        </div>
        <div class="tool-call-args">${escapeHtml(argsStr)}</div>
    `;
    currentAssistantEl.appendChild(el);
    scrollToBottom();
}

function appendToolResult(toolName, result) {
    if (!currentAssistantEl) return;

    const el = document.createElement('div');
    el.className = 'tool-result' + (result.success === false ? ' error' : '');

    let content;
    if (result.error) {
        content = `Error: ${result.error}`;
    } else if (typeof result.result === 'string') {
        content = result.result.substring(0, 2000);
    } else {
        content = JSON.stringify(result.result, null, 2).substring(0, 2000);
    }

    el.innerHTML = `<pre>${escapeHtml(content)}</pre>`;
    currentAssistantEl.appendChild(el);
    scrollToBottom();
}

function appendModelSwitch(fromModel, toModel) {
    const el = document.createElement('div');
    el.className = 'model-switch';
    el.textContent = `Model: ${fromModel || 'brak'} → ${toModel || '?'}`;
    chatMessages.appendChild(el);
    scrollToBottom();
}

function appendError(message) {
    if (!currentAssistantEl) {
        appendAssistantText('');
    }
    const el = document.createElement('div');
    el.className = 'tool-result error';
    el.innerHTML = `<pre>${escapeHtml(message)}</pre>`;
    currentAssistantEl.appendChild(el);
    state.sending = false;
    btnSend.disabled = false;
    typingIndicator.classList.add('hidden');
    scrollToBottom();
}

function clearChat() {
    currentAssistantEl = null;
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <h1>&#9881; NeuroForge</h1>
            <p>Lokalne studio AI z pelnym dostepem do Twojego komputera.</p>
            <p class="hint">Zaladuj model i zacznij rozmowe!</p>
        </div>
    `;
}

// ──── Model Management ────

async function loadModels() {
    try {
        const resp = await fetch('/api/models');
        const data = await resp.json();

        modelSelect.innerHTML = '<option value="">-- Wybierz model --</option>';
        for (const m of data.models) {
            const opt = document.createElement('option');
            opt.value = m.filename;
            opt.textContent = `${m.base_name} (${m.quantization}) - ${m.size_display}`;
            modelSelect.appendChild(opt);
        }
    } catch (e) {
        console.error('Failed to load models:', e);
    }
}

async function loadRecommendedModels() {
    try {
        const resp = await fetch('/api/models/recommended');
        const data = await resp.json();
        const container = $('recommended-models');
        container.innerHTML = '';

        for (const m of data.models) {
            const card = document.createElement('div');
            card.className = 'model-card';
            card.innerHTML = `
                <div class="model-card-name">${escapeHtml(m.name)}</div>
                <div class="model-card-desc">${escapeHtml(m.description)}</div>
                <div class="model-card-meta">
                    <span class="model-card-size">${m.size}</span>
                    ${m.downloaded
                        ? '<span class="downloaded">&#10003; Pobrany</span>'
                        : `<button class="btn btn-sm btn-primary" onclick="downloadModel('${m.repo}', '${m.filename}', this)">Pobierz</button>`
                    }
                </div>
            `;
            container.appendChild(card);
        }
    } catch (e) {
        console.error('Failed to load recommended models:', e);
    }
}

async function downloadModel(repo, filename, btn) {
    btn.disabled = true;
    btn.textContent = 'Pobieranie...';

    try {
        const resp = await fetch('/api/models/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ repo, filename }),
        });

        if (resp.ok) {
            btn.textContent = 'Pobrano!';
            btn.className = 'downloaded';
            loadModels(); // Refresh model list
        } else {
            const data = await resp.json();
            btn.textContent = 'Blad!';
            alert('Blad pobierania: ' + (data.detail || 'unknown'));
        }
    } catch (e) {
        btn.textContent = 'Blad!';
        alert('Blad pobierania: ' + e.message);
    }
}

async function loadModel() {
    const filename = modelSelect.value;
    if (!filename) {
        alert('Wybierz model z listy.');
        return;
    }

    setStatus('loading', 'Ladowanie modelu...');
    btnLoadModel.disabled = true;

    try {
        const resp = await fetch('/api/models/load', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                filename,
                gpu_layers: parseInt($('gpu-layers').value),
                context_size: parseInt($('context-size').value),
                threads: parseInt($('cpu-threads').value),
            }),
        });

        if (resp.ok) {
            state.modelLoaded = true;
            setStatus('active', filename);
            btnUnloadModel.disabled = false;
        } else {
            const data = await resp.json();
            setStatus('error', 'Blad ladowania');
            alert('Blad: ' + (data.detail || 'Unknown error'));
        }
    } catch (e) {
        setStatus('error', 'Blad polaczenia');
        alert('Blad: ' + e.message);
    }

    btnLoadModel.disabled = false;
}

async function unloadModel() {
    try {
        await fetch('/api/models/unload', { method: 'POST' });
        state.modelLoaded = false;
        setStatus('inactive', 'Brak modelu');
        btnUnloadModel.disabled = true;
    } catch (e) {
        console.error('Unload error:', e);
    }
}

async function loadStatus() {
    try {
        const resp = await fetch('/api/status');
        const data = await resp.json();

        if (data.engine.running && data.engine.model) {
            state.modelLoaded = true;
            setStatus('active', data.engine.model);
            btnUnloadModel.disabled = false;
        }
    } catch (e) {
        console.error('Status check failed:', e);
    }
}

function setStatus(type, text) {
    statusDot.className = 'status-indicator';
    if (type === 'active') statusDot.classList.add('active');
    else if (type === 'loading') statusDot.classList.add('loading');
    statusText.textContent = text;
}

// ──── Event Listeners ────

function setupEventListeners() {
    // Send message
    btnSend.addEventListener('click', () => {
        sendMessage(chatInput.value);
    });

    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!state.sending) sendMessage(chatInput.value);
        }
    });

    // Auto-resize textarea
    chatInput.addEventListener('input', () => {
        chatInput.style.height = 'auto';
        chatInput.style.height = Math.min(chatInput.scrollHeight, 150) + 'px';
    });

    // New chat
    btnNewChat.addEventListener('click', () => {
        if (state.ws && state.ws.readyState === WebSocket.OPEN) {
            state.ws.send(JSON.stringify({ type: 'clear' }));
        }
        clearChat();
    });

    // Model controls
    btnLoadModel.addEventListener('click', loadModel);
    btnUnloadModel.addEventListener('click', unloadModel);

    // Temperature slider
    tempSlider.addEventListener('input', () => {
        tempValue.textContent = tempSlider.value;
    });

    // Sidebar toggle (mobile)
    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 &&
            sidebar.classList.contains('open') &&
            !sidebar.contains(e.target) &&
            e.target !== sidebarToggle) {
            sidebar.classList.remove('open');
        }
    });

    // Collapsible sections
    document.querySelectorAll('.section-toggle').forEach(toggle => {
        toggle.addEventListener('click', () => {
            const targetId = toggle.dataset.target;
            const content = document.getElementById(targetId);
            if (content) {
                content.classList.toggle('hidden');
                toggle.classList.toggle('collapsed');
            }
        });
    });
}

// ──── Utilities ────

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function renderMarkdown(text) {
    // Simple markdown rendering
    let html = escapeHtml(text);

    // Code blocks ```...```
    html = html.replace(/```(\w*)\n?([\s\S]*?)```/g, (_, lang, code) => {
        return `<pre><code class="lang-${lang}">${code.trim()}</code></pre>`;
    });

    // Inline code `...`
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Bold **...**
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

    // Italic *...*
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Links [text](url)
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

    // Line breaks
    html = html.replace(/\n/g, '<br>');

    return html;
}

function scrollToBottom() {
    requestAnimationFrame(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });
}

// Expose for inline event handlers
window.downloadModel = downloadModel;
