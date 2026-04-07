// ── Main JS — AI Personal Tutor ────────────────────────────

document.addEventListener('DOMContentLoaded', () => {

  // Auto-dismiss alerts
  const alerts = document.querySelectorAll('.alert[data-auto-dismiss]');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(20px)';
      setTimeout(() => alert.remove(), 300);
    }, 4000);
  });

  // Tab switcher (Paste Text / Upload PDF)
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(p => p.style.display = 'none');
      btn.classList.add('active');
      const target = btn.dataset.tab;
      const pane = document.getElementById(target);
      if (pane) pane.style.display = 'block';
    });
  });

  // Drag & drop PDF upload zone
  const dropZone = document.querySelector('.file-drop-zone');
  const fileInput = document.querySelector('.file-input');

  if (dropZone && fileInput) {
    dropZone.addEventListener('click', (e) => {
      if (e.target !== fileInput) fileInput.click();
    });
    dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
    dropZone.addEventListener('drop', e => {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        fileInput.files = files;
        const nameEl = dropZone.querySelector('.file-name');
        if (nameEl) nameEl.textContent = files[0].name;
      }
    });

    fileInput.addEventListener('change', () => {
      if (fileInput.files.length > 0) {
        const nameEl = dropZone.querySelector('.file-name');
        if (nameEl) nameEl.textContent = fileInput.files[0].name;
      }
    });
  }

  // Animate progress bars on load
  const fills = document.querySelectorAll('.progress-bar-fill[data-pct]');
  fills.forEach(fill => {
    const pct = parseFloat(fill.dataset.pct) || 0;
    setTimeout(() => { fill.style.width = Math.min(pct, 100) + '%'; }, 100);
  });

  // Option selection for quiz
  document.querySelectorAll('.option-label').forEach(label => {
    label.addEventListener('click', () => {
      const name = label.dataset.name;
      document.querySelectorAll(`.option-label[data-name="${name}"]`).forEach(l => l.classList.remove('selected'));
      label.classList.add('selected');
      const radio = label.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;
    });
  });

  // Confirm delete dialogs
  document.querySelectorAll('.confirm-delete-form').forEach(form => {
    form.addEventListener('submit', e => {
      if (!confirm('Are you sure? This action cannot be undone.')) {
        e.preventDefault();
      }
    });
  });

});
