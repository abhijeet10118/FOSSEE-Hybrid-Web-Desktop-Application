const API_BASE = '/api';

function getAuthHeaders() {
  const creds = sessionStorage.getItem('auth');
  if (!creds) return {};
  const { username, password } = JSON.parse(creds);
  const encoded = btoa(`${username}:${password}`);
  return { Authorization: `Basic ${encoded}` };
}

export async function login(username, password) {
  const res = await fetch(`${API_BASE}/history/`, {
    headers: { Authorization: `Basic ${btoa(`${username}:${password}`)}` },
  });
  if (!res.ok) throw new Error('Invalid credentials');
  sessionStorage.setItem('auth', JSON.stringify({ username, password }));
  return { username };
}

export function logout() {
  sessionStorage.removeItem('auth');
}

export function isAuthenticated() {
  return !!sessionStorage.getItem('auth');
}

export async function uploadCSV(file) {
  const form = new FormData();
  form.append('file', file);
  const res = await fetch(`${API_BASE}/upload/`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: form,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || res.statusText);
  }
  return res.json();
}

export async function getHistory() {
  const res = await fetch(`${API_BASE}/history/`, { headers: getAuthHeaders() });
  if (!res.ok) throw new Error('Failed to load history');
  return res.json();
}

export async function getDataset(id) {
  const res = await fetch(`${API_BASE}/datasets/${id}/`, { headers: getAuthHeaders() });
  if (!res.ok) throw new Error('Failed to load dataset');
  return res.json();
}

export function getPDFUrl(id) {
  const creds = sessionStorage.getItem('auth');
  if (!creds) return null;
  const { username, password } = JSON.parse(creds);
  return `${API_BASE}/datasets/${id}/pdf/?${new URLSearchParams({})}`;
}

export function downloadPDF(id, filename) {
  const creds = sessionStorage.getItem('auth');
  if (!creds) return;
  const { username, password } = JSON.parse(creds);
  const encoded = btoa(`${username}:${password}`);
  fetch(`/api/datasets/${id}/pdf/`, { headers: { Authorization: `Basic ${encoded}` } })
    .then(r => r.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename || `report_${id}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    });
}
