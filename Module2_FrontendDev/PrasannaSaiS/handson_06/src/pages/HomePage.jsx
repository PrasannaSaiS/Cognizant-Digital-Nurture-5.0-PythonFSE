import React from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

function HomePage() {
  const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);
  const totalCredits = enrolledCourses.reduce((sum, course) => sum + course.credits, 0);

  return (
    <div className="page-container">
      <section className="hero">
        <h1>Welcome to your Student Dashboard</h1>
        <p>Manage your academic journey, track course enrollments, and update your information.</p>
      </section>

      <div className="home-dashboard">
        <div className="stat-card glass">
          <h3>Enrolled Courses</h3>
          <p className="stat-val">{enrolledCourses.length}</p>
          <p style={{ color: 'var(--text-secondary)' }}>Currently active courses</p>
          <Link to="/profile" className="btn btn-primary" style={{ marginTop: '1.5rem', textDecoration: 'none' }}>
            View Enrolled List
          </Link>
        </div>

        <div className="stat-card glass">
          <h3>Total Credits</h3>
          <p className="stat-val">{totalCredits}</p>
          <p style={{ color: 'var(--text-secondary)' }}>Earned towards graduation</p>
          <Link to="/courses" className="btn btn-primary" style={{ marginTop: '1.5rem', textDecoration: 'none' }}>
            Explore Courses
          </Link>
        </div>

        <div className="stat-card glass">
          <h3>Profile Status</h3>
          <p className="stat-val" style={{ fontSize: '1.75rem', margin: '1.1rem 0' }}>Verified</p>
          <p style={{ color: 'var(--text-secondary)' }}>Semester 4 Student</p>
          <Link to="/profile" className="btn btn-primary" style={{ marginTop: '1.5rem', textDecoration: 'none' }}>
            Edit Profile
          </Link>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
