import { getKus } from './api.js';

export async function loadKus() {
  try {
    const kus = await getKus();
    const list = document.getElementById('kus');
    if (!list) return;
    list.innerHTML = '';
    for (const ku of kus) {
      const li = document.createElement('li');
      li.textContent = ku;
      list.appendChild(li);
    }
  } catch (err) {
    console.error('Failed to load KUs', err);
  }
}

document.addEventListener('DOMContentLoaded', loadKus);
