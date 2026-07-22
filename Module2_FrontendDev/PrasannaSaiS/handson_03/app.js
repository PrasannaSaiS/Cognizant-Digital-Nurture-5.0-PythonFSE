import { courses as courseData } from './data.js';

const courseGrid = document.querySelector('.course-grid');
const totalCreditsEl = document.getElementById('total-credits');
const searchInput = document.getElementById('search-courses');
const sortButton = document.getElementById('sort-button');
const selectedCourseEl = document.getElementById('selected-course');

// Step 30: Loop through courses and use destructuring to extract name and credits.
courseData.forEach((course) => {
  const { name, credits } = course; // destructuring — cleaner than course.name / course.credits
  console.log(`Destructured -> name: ${name}, credits: ${credits}`);
});

// Step 31: Array.map() -> formatted strings like 'CS101 — Data Structures (4 credits)'.
const formattedCourses = courseData.map(
  ({ code, name, credits }) => `${code} — ${name} (${credits} credits)`
);
console.log('Formatted courses:', formattedCourses);

// Step 32: Array.filter() -> only courses with credits >= 4.
const highCreditCourses = courseData.filter(({ credits }) => credits >= 4);
console.log('Courses with 4+ credits:', highCreditCourses.length);

// Step 33: Array.reduce() -> total credits enrolled.
const totalCredits = courseData.reduce((sum, { credits }) => sum + credits, 0);
console.log('Total credits:', totalCredits);

// Step 34: Rewriting a traditional for loop as an arrow function with a template literal.
// The equivalent traditional loop would be:
//   for (let i = 0; i < courseData.length; i++) {
//     console.log(courseData[i].code + ' - ' + courseData[i].name);
//   }
// Arrow function + template literal version:
const summaryLines = courseData.map(
  ({ code, name }) => `Summary: ${code} - ${name}`
);
summaryLines.forEach((line) => console.log(line));

const renderCourses = (items) => {
  courseGrid.innerHTML = '';

  if (items.length === 0) {
    courseGrid.innerHTML = '<p>No matching courses found.</p>';
    totalCreditsEl.textContent = 'Total Credits: 0';
    return;
  }

  const fragment = document.createDocumentFragment();

  items.forEach((course) => {
    const card = document.createElement('article');
    card.className = 'course-card';
    card.dataset.id = course.id;
    card.innerHTML = `
      <h3>${course.name}</h3>
      <p><strong>Code:</strong> ${course.code}</p>
      <p><strong>Credits:</strong> ${course.credits}</p>
      <p><strong>Grade:</strong> ${course.grade}</p>
    `;
    fragment.appendChild(card);
  });

  courseGrid.appendChild(fragment);
  totalCreditsEl.textContent = `Total Credits: ${items.reduce((sum, course) => sum + course.credits, 0)}`;
};

let visibleCourses = [...courseData];
renderCourses(visibleCourses);

searchInput.addEventListener('input', (event) => {
  const query = event.target.value.trim().toLowerCase();
  const filtered = visibleCourses.filter(({ name }) => name.toLowerCase().includes(query));
  renderCourses(filtered);
});

sortButton.addEventListener('click', () => {
  visibleCourses = [...visibleCourses].sort((a, b) => b.credits - a.credits);
  renderCourses(visibleCourses);
});

courseGrid.addEventListener('click', (event) => {
  const card = event.target.closest('.course-card');
  if (!card) return;

  const course = visibleCourses.find((item) => item.id === Number(card.dataset.id));
  if (course) {
    selectedCourseEl.textContent = `Selected course: ${course.name} — Grade ${course.grade}`;
  }
});
