import React from 'react';

function Footer() {
  const currentYear = new Date().getFullYear();
  return (
    <footer className="site-footer">
      <p>&copy; {currentYear} Student Portal. All rights reserved.</p>
    </footer>
  );
}

export default Footer;
