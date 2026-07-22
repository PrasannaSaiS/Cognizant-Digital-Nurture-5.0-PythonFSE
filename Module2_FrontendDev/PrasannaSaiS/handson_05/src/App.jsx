import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import CourseCard from './components/CourseCard';
import StudentProfile from './components/StudentProfile';
import { courses as fallbackCourses } from './data';

function App() {
  const [courses, setCourses] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch courses from JSONPlaceholder API
  useEffect(() => {
    let active = true;
    const fetchCourses = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch posts from API
        const response = await fetch('https://jsonplaceholder.typicode.com/posts');
        if (!response.ok) {
          throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        
        if (active) {
          // Map first 5 posts to realistic course-like objects
          const grades = ['A', 'B+', 'A-', 'B', 'A'];
          const mappedCourses = data.slice(0, 5).map((post, idx) => ({
            id: post.id,
            name: post.title.split(' ').slice(0, 2).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
            code: `CS10${post.id}`,
            credits: (post.id % 3) + 2, // 2 to 4 credits
            grade: grades[idx % grades.length]
          }));
          setCourses(mappedCourses);
        }
      } catch (err) {
        if (active) {
          console.error('Error fetching courses, using fallback data:', err);
          setError(err.message);
          // Fallback to static courses data so the app remains fully functional
          setCourses(fallbackCourses);
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    fetchCourses();

    return () => {
      active = false;
    };
  }, []);

  // Log courses changes to console
  /*
    Why the dependency array matters:
    1. If the dependency array is `[courses]`, this effect runs ONLY when the `courses` state changes. 
       This avoids running the log on unrelated state updates (like typing in the search input or editing the profile form).
    2. If the array is empty `[]`, it runs exactly once after the initial render (mount) and never again.
    3. If the array is omitted entirely, it runs after EVERY single render of this component.
       If the effect triggers a state change, omitting it would lead to an infinite render loop.
  */
  useEffect(() => {
    console.log('Courses updated');
  }, [courses]);

  // Handle enrollment
  const handleEnroll = (course) => {
    // Prevent duplicate enrollment
    if (!enrolledCourses.some(c => c.id === course.id)) {
      setEnrolledCourses(prev => [...prev, course]);
    }
  };

  // Filter courses based on search term
  const filteredCourses = courses.filter(course =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    course.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />
      
      <main>
        <section className="hero">
          <h1>Welcome to the Student Portal</h1>
          <p>Browse courses, manage enrollment, and keep your student profile up-to-date.</p>
        </section>

        <section id="courses">
          <h2 className="section-title">Available Courses</h2>
          
          <div className="controls-container">
            <input
              type="text"
              className="search-input glass"
              placeholder="Search courses by name or code..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {loading ? (
            <div className="state-message">
              <div className="loading-spinner"></div>
              <p>Loading course information from API...</p>
            </div>
          ) : error ? (
            <div className="state-message">
              <p className="error-text">Failed to fetch courses: {error}</p>
              <p>Showing offline fallback data.</p>
              <div className="course-grid" style={{ marginTop: '1.5rem' }}>
                {filteredCourses.map(course => (
                  <CourseCard
                    key={course.id}
                    {...course}
                    isEnrolled={enrolledCourses.some(c => c.id === course.id)}
                    onEnroll={handleEnroll}
                  />
                ))}
              </div>
            </div>
          ) : (
            <div className="course-grid">
              {filteredCourses.length > 0 ? (
                filteredCourses.map(course => (
                  <CourseCard
                    key={course.id}
                    {...course}
                    isEnrolled={enrolledCourses.some(c => c.id === course.id)}
                    onEnroll={handleEnroll}
                  />
                ))
              ) : (
                <div className="state-message">
                  <p>No courses matched your search criteria.</p>
                </div>
              )}
            </div>
          )}
        </section>

        <StudentProfile />
      </main>

      <Footer />
    </>
  );
}

export default App;
