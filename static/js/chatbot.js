// ── Chatbot JS ──────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  const fab = document.getElementById('chatbot-fab');
  const panel = document.getElementById('chatbot-panel');
  const closeBtn = document.getElementById('chatbot-close');
  const sendBtn = document.getElementById('chatbot-send');
  const inputEl = document.getElementById('chatbot-input');
  const messagesEl = document.getElementById('chatbot-messages');
  const subjectId = document.getElementById('chatbot-subject-id')?.value || null;

  if (!fab || !panel) return;

  fab.addEventListener('click', () => {
    panel.classList.toggle('open');
    if (panel.classList.contains('open') && inputEl) inputEl.focus();
  });

  if (closeBtn) closeBtn.addEventListener('click', () => panel.classList.remove('open'));

  function appendMessage(content, role) {
    const msg = document.createElement('div');
    msg.classList.add('chat-msg', role);
    msg.innerHTML = window.marked ? marked.parse(content) : content;
    messagesEl.appendChild(msg);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function showTyping() {
    const typing = document.createElement('div');
    typing.id = 'typing-indicator';
    typing.classList.add('chat-msg', 'assistant');
    typing.innerHTML = '<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>';
    messagesEl.appendChild(typing);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function removeTyping() {
    const typing = document.getElementById('typing-indicator');
    if (typing) typing.remove();
  }

  async function sendMessage() {
    const message = inputEl.value.trim();
    if (!message) return;

    appendMessage(message, 'user');
    inputEl.value = '';
    sendBtn.disabled = true;
    showTyping();

    try {
      const res = await fetch('/chatbot/api/send/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ message, subject_id: subjectId }),
      });
      const data = await res.json();
      removeTyping();
      if (data.response) appendMessage(data.response, 'assistant');
    } catch (err) {
      removeTyping();
      appendMessage('Connection error. Please try again.', 'assistant');
    } finally {
      sendBtn.disabled = false;
      inputEl.focus();
    }
  }

  if (sendBtn) sendBtn.addEventListener('click', sendMessage);
  if (inputEl) {
    inputEl.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });
  }

  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : '';
  }
});
