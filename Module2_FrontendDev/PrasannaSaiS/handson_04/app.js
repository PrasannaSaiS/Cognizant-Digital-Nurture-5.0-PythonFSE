import { courses as courseData } from '../handson_03/data.js';

const courseGrid = document.querySelector('.course-grid');
const loadingCoursesEl = document.getElementById('loading-courses');
const loadingNotificationsEl = document.getElementById('loading-notifications');
const errorMessageEl = document.getElementById('error-message');
const retryButton = document.getElementById('retry-button');
const notificationsList = document.getElementById('notifications-list');

const axios = window.axios || {
  interceptors: {
    request: {
      use: () => {}
    }
  },
  get: async (url, config = {}) => {
    const baseUrl = 'https://jsonplaceholder.typicode.com';
    const targetUrl = new URL(url.startsWith('http') ? url : `${baseUrl}${url.startsWith('/') ? url : `/${url}`}`);

    if (config.params) {
      Object.entries(config.params).forEach(([key, value]) => targetUrl.searchParams.set(key, value));
    }

    const response = await fetch(targetUrl);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return { data: await response.json() };
  }
};

const BASE_URL = 'https://jsonplaceholder.typicode.com';

// Resolve a relative API path (e.g. '/posts') against the base URL,
// applying any params object as query string.
function resolveUrl(path, params) {
  const url = new URL(path.startsWith('http') ? path : `${BASE_URL}${path.startsWith('/') ? path : `/${path}`}`);
  if (params) {
    Object.entries(params).forEach(([key, value]) => url.searchParams.set(key, value));
  }
  return url;
}

// Task 2 (Step 50): a reusable Fetch-based apiFetch that checks response.ok
// and throws a *descriptive* Error. Fetch only rejects on network failures —
// it resolves normally for HTTP errors like 404/500, so we must check response.ok.
async function apiFetch(url, { params } = {}) {
  const target = resolveUrl(url, params);
  const response = await fetch(target);

  if (!response.ok) {
    // Always check response.ok — HTTP errors are NOT thrown by fetch itself.
    throw new Error(`Request to "${target}" failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

function fetchUser(id) {
  return fetch(`https://jsonplaceholder.typicode.com/users/${id}`)
    .then((response) => response.json())
    .then((user) => console.log('User name:', user.name));
}

async function fetchUserAsync(id) {
  try {
    const response = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
    const user = await response.json();
    console.log('Async user name:', user.name);
  } catch (error) {
    console.error('Failed to fetch user:', error);
  }
}

function fetchAllCourses() {
  return new Promise((resolve) => {
    setTimeout(() => resolve(courseData), 1000);
  });
}

async function loadCourses() {
  loadingCoursesEl.textContent = 'Loading courses...';
  const loadedCourses = await fetchAllCourses();
  courseGrid.innerHTML = '';
  loadedCourses.forEach((course) => {
    const card = document.createElement('article');
    card.className = 'course-card';
    card.innerHTML = `<h3>${course.name}</h3><p>${course.code}</p><p>${course.credits} credits</p>`;
    courseGrid.appendChild(card);
  });
  loadingCoursesEl.textContent = 'Courses loaded successfully.';
}

// Task 3 (Step 56): same idea rewritten with axios. Axios (a) automatically parses
// JSON (so we return response.data), and (b) throws on non-2xx by default — no need
// to check response.ok manually. { params } is passed straight through to axios.
async function apiFetchAxios(url, { params } = {}) {
  // axios.get returns the parsed data in response.data (no manual .json()).
  // Non-2xx responses throw automatically — no response.ok check required.
  const { data } = await axios.get(url, params ? { params } : undefined);
  return data;
}

// Step 53: simulate a 404 by attempting a bad URL once on first load, so the
// user-friendly error message and Retry button are demonstrated.
let shouldAttemptBadUrl = true;

async function loadNotifications() {
  loadingNotificationsEl.style.display = 'block';
  errorMessageEl.textContent = '';
  retryButton.style.display = 'none';
  notificationsList.innerHTML = '';

  try {
    if (shouldAttemptBadUrl) {
      shouldAttemptBadUrl = false;
      // Task 2 (Step 53): use the Fetch-based apiFetch to hit a bad URL and
      // trigger the descriptive error + Retry button flow.
      await apiFetch('/nonexistent');
      return;
    }

    // Task 3 (Step 57): use axios with a params object to fetch posts for user 1.
    const posts = await apiFetchAxios('/posts', { params: { userId: 1 } });
    posts.slice(0, 5).forEach((post) => {
      const card = document.createElement('article');
      card.className = 'notification-card';
      card.innerHTML = `<h3>${post.title}</h3><p>${post.body}</p>`;
      notificationsList.appendChild(card);
    });
  } catch (error) {
    // Never just log to console — show a friendly message in the UI.
    errorMessageEl.textContent = 'Unable to load notifications right now. Please try again.';
    retryButton.style.display = 'inline-block';
  } finally {
    loadingNotificationsEl.style.display = 'none';
  }
}

retryButton.addEventListener('click', loadNotifications);

axios.interceptors.request.use((config) => {
  console.log(`API call started: ${config.url}`);
  return config;
});

// Fetch vs Axios differences:
// 1. fetch uses Response objects and requires manual JSON parsing, while axios returns parsed data directly.
// 2. fetch does not reject on HTTP error statuses by default, while axios rejects on non-2xx responses.
// 3. fetch requires more manual setup for headers and request configuration, while axios provides built-in conveniences.

fetchUser(1);
fetchUserAsync(2);
Promise.all([fetchUser(1), fetchUser(2)]).then(() => console.log('Promise.all completed'));

loadCourses();
loadNotifications();
