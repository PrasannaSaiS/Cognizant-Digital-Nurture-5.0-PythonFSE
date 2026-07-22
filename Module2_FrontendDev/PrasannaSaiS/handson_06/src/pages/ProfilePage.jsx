import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Link } from 'react-router-dom';
import StudentProfile from '../components/StudentProfile';
import { unenroll } from '../redux/enrollmentSlice';

function ProfilePage() {
  const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);
  const dispatch = useDispatch();

  const handleRemove = (id) => {
    dispatch(unenroll(id));
  };

  return (
    <div className="page-container" style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem' }}>
      <StudentProfile />

      <section className="profile-card glass" style={{ maxWidth: '800px' }}>
        <h2 className="section-title">My Enrolled Courses</h2>
        
        {enrolledCourses.length === 0 ? (
          <div className="state-message" style={{ borderStyle: 'solid' }}>
            <p style={{ color: 'var(--text-secondary)' }}>You are not enrolled in any courses yet.</p>
            <Link to="/courses" className="btn btn-primary" style={{ marginTop: '1.5rem', width: 'auto', display: 'inline-flex', textDecoration: 'none' }}>
              Browse & Enroll in Courses
            </Link>
          </div>
        ) : (
          <div className="course-grid">
            {enrolledCourses.map(course => (
              <article key={course.id} className="course-card glass" style={{ border: '1px solid rgba(255,255,255,0.05)' }}>
                <div className="course-header">
                  <h3 className="course-title">{course.name}</h3>
                  <span className="course-code">{course.code}</span>
                </div>
                
                <div className="course-details">
                  <div className="course-detail-item">
                    Credits: <strong>{course.credits}</strong>
                  </div>
                  <div className="course-detail-item">
                    Grade: <strong className="grade-badge">{course.grade}</strong>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
                  <Link 
                    to={`/courses/${course.id}`} 
                    className="btn" 
                    style={{ flex: 1, backgroundColor: 'rgba(99, 102, 241, 0.1)', color: 'var(--accent-primary)', textDecoration: 'none', border: '1px solid rgba(99,102,241,0.2)' }}
                  >
                    Details
                  </Link>
                  <button 
                    className="btn btn-danger" 
                    style={{ flex: 1 }}
                    onClick={() => handleRemove(course.id)}
                  >
                    Remove
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default ProfilePage;
