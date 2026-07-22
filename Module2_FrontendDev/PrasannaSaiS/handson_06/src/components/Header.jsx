import React from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

function Header() {
  const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);
  const enrolledCount = enrolledCourses.length;

  return (
    <header className="site-header glass">
      <Link to="/" className="site-title">Student Portal</Link>
      <nav aria-label="Primary navigation">
        <ul className="nav-links">
          <li><Link to="/">Home</Link></li>
          <li>
            <Link to="/courses">
              Courses
              {enrolledCount > 0 && <span className="badge">{enrolledCount}</span>}
            </Link>
          </li>
          <li><Link to="/profile">Profile</Link></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
