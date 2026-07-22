import React from 'react';

function Header({ siteName, enrolledCount }) {
  return (
    <header className="site-header glass">
      <a href="#" className="site-title">{siteName}</a>
      <nav aria-label="Primary navigation">
        <ul className="nav-links">
          <li><a href="#home">Home</a></li>
          <li>
            <a href="#courses">
              Courses
              {enrolledCount > 0 && <span className="badge">{enrolledCount}</span>}
            </a>
          </li>
          <li><a href="#profile">Profile</a></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
