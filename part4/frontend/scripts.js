// === HBnB Part 4 - Frontend Script ===
// Works with Flask mock API at http://127.0.0.1:5000/api/v1
// Endpoints used: POST /login, GET /places, GET /places/:id, POST /reviews

const API_BASE = 'http://127.0.0.1:5000/api/v1';

// ---------- Cookie helpers ----------
function setCookie(name, value, days = 1) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}
function getCookie(name) {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith(`${encodeURIComponent(name)}=`))
    ?.split('=')[1]
    ? decodeURIComponent(document.cookie.split('; ').find(row => row.startsWith(`${encodeURIComponent(name)}=`)).split('=')[1])
    : null;
}
function deleteCookie(name) {
  document.cookie = `${encodeURIComponent(name)}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
}

// ---------- Auth helpers ----------
function getToken() {
  return getCookie('token');
}
function isAuthenticated() {
  return Boolean(getToken());
}
function authHeaders() {
  const t = getToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}

// ---------- URL helpers ----------
function getQueryParam(key) {
  return new URLSearchParams(window.location.search).get(key);
}

// ---------- Common UI helpers ----------
function toggleLoginLink() {
  const loginLink = document.getElementById('login-link');
  if (!loginLink) return;
  loginLink.style.display = isAuthenticated() ? 'none' : 'block';
}
function ensurePriceFilterOptions() {
  const sel = document.getElementById('price-filter');
  if (!sel) return;
  // Required options: 10, 50, 100, All
  const needed = ['10', '50', '100', 'All'];
  if (sel.options.length === 0) {
    needed.forEach(v => {
      const opt = document.createElement('option');
      opt.value = v;
      opt.textContent = v;
      sel.appendChild(opt);
    });
  }
}

// ---------- Render helpers ----------
function createPlaceCard(place) {
  const col = document.createElement('div');
  col.className = 'col-12 col-sm-6 col-lg-4 col-xl-3';

  const img = (place.images && place.images[0]) || 'images/sample1.jpg';

  col.innerHTML = `
    <div class="place-card position-relative text-white" style="background-image: url('${img}')">
      

      <div class="place-info position-relative d-flex flex-column justify-content-between h-100 p-3">
        <div>
          <h5 class="fw-bold">${place.title}</h5>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-auto">
          <a href="place.html?id=${place.id}" class="text-white fw-semibold text-decoration-none">Book now</a>
        </div>
      </div>

      <div class="visually-hidden host-name">${place.host || 'Unknown Host'}</div>
    </div>
  `;
  return col;
}


function renderPlaces(listEl, places) {
  listEl.innerHTML = '';
  places.forEach(p => listEl.appendChild(createPlaceCard(p)));
}

function renderPlaceDetails(container, place) {
  container.innerHTML = `
    <div class="place-details">
      <div class="pd-hero">
        <img class="pd-image" src="${(place.images && place.images[0]) || 'images/sample1.jpg'}" alt="${place.title}">
        <div class="pd-main">
          <h2 class="pd-title">${place.title}</h2>
          <p class="pd-meta"><strong>Host:</strong> ${place.host ?? 'Unknown'}</p>
          <p class="pd-meta"><strong>Price:</strong> $${place.price} / night</p>
          <p class="pd-desc">${place.description ?? ''}</p>
          ${place.latitude && place.longitude ? `<p class="pd-coords">(${place.latitude}, ${place.longitude})</p>` : ''}
        </div>
      </div>

      <div class="pd-amenities">
        <h3>Amenities</h3>
        ${
          (place.amenities && place.amenities.length)
            ? `<ul class="pd-amenities-list">${place.amenities.map(a => `<li>${a}</li>`).join('')}</ul>`
            : `<p class="pd-muted">No amenities listed.</p>`
        }
      </div>

      <div class="pd-reviews">
        <h3>Reviews</h3>
        <div class="pd-reviews-grid">
          ${
            (place.reviews && place.reviews.length)
              ? place.reviews.map(r => `
                  <div class="review-card">
                    <p class="review-user"><strong>${r.user ?? 'User'}</strong></p>
                    <p class="review-rating">Rating: ${r.rating ?? 5}</p>
                    <p class="review-text">${r.comment ?? ''}</p>
                  </div>
                `).join('')
              : `<p class="pd-muted">No reviews yet.</p>`
          }
        </div>
      </div>

      ${isAuthenticated()
        ? `<div class="pd-cta"><a class="details-button" href="add_review.html?id=${encodeURIComponent(place.id)}">Add a review</a></div>`
        : ''
      }
    </div>
  `;
}

// ---------- API calls ----------
async function apiLogin(email, password) {
  const res = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) throw new Error('Login failed');
  return res.json();
}

async function apiGetPlaces() {
  const res = await fetch(`${API_BASE}/places`, { headers: { ...authHeaders() } });
  if (!res.ok) throw new Error('Failed to fetch places');
  return res.json();
}

async function apiGetPlace(id) {
  const res = await fetch(`${API_BASE}/places/${encodeURIComponent(id)}`, { headers: { ...authHeaders() } });
  if (!res.ok) throw new Error('Failed to fetch place details');
  return res.json();
}

async function apiPostReview(placeId, comment, rating = 5) {
  const res = await fetch(`${API_BASE}/reviews`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify({ place_id: placeId, comment, rating })
  });
  if (res.status === 401) throw new Error('Unauthorized');
  if (!res.ok) throw new Error('Failed to submit review');
  return res.json();
}

// ---------- Page bootstraps ----------
async function initLoginPage() {
  toggleLoginLink();
  const form = document.getElementById('login-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = (document.getElementById('email') || {}).value || '';
    const password = (document.getElementById('password') || {}).value || '';
    try {
      const data = await apiLogin(email.trim(), password);
      // Store token in cookie for session management
      setCookie('token', data.access_token, 1);
      window.location.href = 'index.html';
    } catch (err) {
      alert('Login failed. Check your email/password.');
    }
  });
}

async function initIndexPage() {
  toggleLoginLink();
  ensurePriceFilterOptions();

  const listEl = document.getElementById('places-list');
  if (!listEl) return;

  try {
    const places = await apiGetPlaces();
    renderPlaces(listEl, places);

    // Client-side price filter
    const sel = document.getElementById('price-filter');
    if (sel) {
      sel.addEventListener('change', () => {
        const val = sel.value;
        if (val === 'All') {
          renderPlaces(listEl, places);
        } else {
          const max = Number(val);
          const filtered = places.filter(p => Number(p.price) <= max);
          renderPlaces(listEl, filtered);
        }
      });
    }
  } catch (err) {
    listEl.innerHTML = '<p>Failed to load places.</p>';
  }
}

async function initPlacePage() {
  toggleLoginLink();
  const id = getQueryParam('id');
  const container = document.getElementById('place-details');
  if (!container) return;

  if (!id) {
    container.innerHTML = '<p>Missing place id.</p>';
    return;
  }

  try {
    const place = await apiGetPlace(id);
    renderPlaceDetails(container, place);
  } catch (err) {
    container.innerHTML = '<p>Failed to load place details.</p>';
  }
}

async function initAddReviewPage() {
  // Only authenticated users can access this page; otherwise redirect to index
  if (!isAuthenticated()) {
    window.location.href = 'index.html';
    return;
  }
  toggleLoginLink();

  const placeId = getQueryParam('id');
  const form = document.getElementById('review-form');
  const textEl = document.getElementById('review-text');
  const ratingEl = document.getElementById('rating');

  if (!placeId || !form) {
    alert('Missing place id or form not found.');
    window.location.href = 'index.html';
    return;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const comment = (textEl && textEl.value.trim()) || '';
    const rating = ratingEl ? Number(ratingEl.value) || 5 : 5;

    if (!comment) {
      alert('Please enter your review.');
      return;
    }

    try {
      await apiPostReview(placeId, comment, rating);
      alert('Review submitted successfully!');
      form.reset();
      // Optionally, go back to place details
      window.location.href = `place.html?id=${encodeURIComponent(placeId)}`;
    } catch (err) {
      if (String(err.message).includes('Unauthorized')) {
        alert('Session expired. Please log in again.');
        deleteCookie('token');
        window.location.href = 'login.html';
      } else {
        alert('Failed to submit review.');
      }
    }
  });
}

// ---------- Router ----------
document.addEventListener('DOMContentLoaded', () => {
  // Determine which page we're on via pathname
  const path = window.location.pathname.toLowerCase();

  if (path.endsWith('/login.html')) {
    initLoginPage();
  } else if (path.endsWith('/index.html') || path.endsWith('/')) {
    initIndexPage();
  } else if (path.endsWith('/place.html')) {
    initPlacePage();
  } else if (path.endsWith('/add_review.html')) {
    initAddReviewPage();
  } else {
    // Fallback: still toggle the login link if present
    toggleLoginLink();
  }
});
