// Global utility: flash notifications (optional, reserved for future use)
function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.textContent = message;
  toast.style.cssText = `
    position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;
    background:${type === 'success' ? '#166534' : '#991b1b'};color:#fff;
    padding:.65rem 1.1rem;border-radius:8px;font-size:.85rem;
    box-shadow:0 4px 16px rgba(0,0,0,.2);
    animation:fadeIn .2s ease;
  `;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

document.addEventListener('click', async (e) => {
  const btn = e.target.closest('[data-action="delete-exam"]');
  if (!btn) return;

  const id = btn.dataset.id;
  const title = btn.dataset.title;
  if (!confirm(`Delete exam "${title}"? This cannot be undone.`)) return;

  const res = await fetch(`/api/exams/${id}`, { method: 'DELETE' });
  if (res.ok) location.reload();
  else alert('Error deleting exam.');
});
