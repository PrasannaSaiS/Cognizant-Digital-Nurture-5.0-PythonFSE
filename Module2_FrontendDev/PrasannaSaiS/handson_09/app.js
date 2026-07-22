import { courses as courseData } from './data.js';

const courseGrid = document.querySelector('.course-grid');
const totalCreditsEl = document.getElementById('total-credits');
const searchInput = document.getElementById('search-courses');
const sortButton = document.getElementById('sort-button');
const selectedCourseEl = document.getElementById('selected-course');
const resultsCountEl = document.getElementById('results-count');

// Helper to update selection
const selectCourse = (card) => {
  const course = visibleCourses.find((item) => item.id === Number(card.dataset.id));
  if (course) {
    selectedCourseEl.textContent = `Selected course: ${course.name} — Expected Grade: ${course.grade}`;
    // Focus the selected course region to assist screen readers
    selectedCourseEl.focus();
  }
};

const renderCourses = (items) => {
  courseGrid.innerHTML = '';

  // Update live region announcer for screen readers (Task 2)
  resultsCountEl.textContent = `${items.length} course${items.length === 1 ? '' : 's'} found`;

  if (items.length === 0) {
    courseGrid.innerHTML = '<p class="no-results" role="alert">No matching courses found.</p>';
    totalCreditsEl.textContent = 'Total Enrolled Credits: 0';
    return;
  }

  const fragment = document.createDocumentFragment();

  items.forEach((course) => {
    const card = document.createElement('article');
    card.className = 'course-card';
    card.dataset.id = course.id;
    card.tabIndex = 0; // Make focusable (Task 2)
    card.setAttribute('role', 'button'); // Set appropriate role (Task 2)
    card.setAttribute('aria-label', `${course.name}, code ${course.code}, ${course.credits} credits, expected grade ${course.grade}. Click to view details.`);
    
    card.innerHTML = `
      <h3>${course.name}</h3>
      <p><strong>Code:</strong> ${course.code}</p>
      <p><strong>Credits:</strong> ${course.credits}</p>
      <p><strong>Grade:</strong> ${course.grade}</p>
    `;
    fragment.appendChild(card);
  });

  courseGrid.appendChild(fragment);
  totalCreditsEl.textContent = `Total Enrolled Credits: ${items.reduce((sum, course) => sum + course.credits, 0)}`;
};

let visibleCourses = [...courseData];
renderCourses(visibleCourses);

// Search query input handling
searchInput.addEventListener('input', (event) => {
  const query = event.target.value.trim().toLowerCase();
  const filtered = courseData.filter(({ name, code }) => 
    name.toLowerCase().includes(query) || code.toLowerCase().includes(query)
  );
  renderCourses(filtered);
});

// Sort click listener
sortButton.addEventListener('click', () => {
  visibleCourses = [...visibleCourses].sort((a, b) => b.credits - a.credits);
  renderCourses(visibleCourses);
});

// Mouse Click Event Delegation
courseGrid.addEventListener('click', (event) => {
  const card = event.target.closest('.course-card');
  if (!card) return;
  selectCourse(card);
});

// Keyboard Navigation Event Delegation (Task 2)
courseGrid.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault(); // Prevent scrolling down when space is pressed
    const card = event.target.closest('.course-card');
    if (!card) return;
    selectCourse(card);
  }
});
