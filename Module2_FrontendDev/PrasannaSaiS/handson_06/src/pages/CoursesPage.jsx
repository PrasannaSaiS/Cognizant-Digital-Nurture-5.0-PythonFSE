import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import CourseCard from '../components/CourseCard';
import { enroll } from '../redux/enrollmentSlice';
import { courses as fallbackCourses } from '../data';

function CoursesPage() {
  const [courses, setCourses] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const dispatch = useDispatch();
  const navigate = useNavigate();
  const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);

  // Fetch courses from JSONPlaceholder API
  useEffect(() => {
    let active = true;
    const fetchCourses = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch('https://jsonplaceholder.typicode.com/posts');
        if (!response.ok) {
          throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        
        if (active) {
          const grades = ['A', 'B+', 'A-', 'B', 'A'];
          const mappedCourses = data.slice(0, 5).map((post, idx) => ({
            id: post.id,
            name: post.title.split(' ').slice(0, 2).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
            code: `CS10${post.id}`,
            credits: (post.id % 3) + 2,
            grade: grades[idx % grades.length]
          }));
          setCourses(mappedCourses);
        }
      } catch (err) {
        if (active) {
          console.error('Error fetching courses, using fallback data:', err);
          setError(err.message);
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

  // Log courses update
  useEffect(() => {
    console.log('Courses updated');
  }, [courses]);

  const handleEnroll = (course) => {
    dispatch(enroll(course));
    navigate('/profile');
  };

  const filteredCourses = courses.filter(course =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    course.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="page-container">
      <h2 className="section-title">Course Catalog</h2>
      
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
    </div>
  );
}

export default CoursesPage;
