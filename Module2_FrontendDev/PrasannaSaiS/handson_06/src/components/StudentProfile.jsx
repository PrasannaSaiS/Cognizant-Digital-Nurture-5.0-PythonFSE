import React, { useState } from 'react';

function StudentProfile() {
  const [profile, setProfile] = useState({
    name: 'John Doe',
    email: 'john.doe@example.com',
    semester: '4'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <section className="profile-card glass" id="profile">
      <h2 className="section-title">Student Profile</h2>
      
      <div className="form-group">
        <label htmlFor="name-input">Full Name</label>
        <input
          id="name-input"
          type="text"
          name="name"
          className="form-control"
          value={profile.name}
          onChange={handleChange}
          placeholder="Enter your name"
        />
      </div>

      <div className="form-group">
        <label htmlFor="email-input">Email Address</label>
        <input
          id="email-input"
          type="email"
          name="email"
          className="form-control"
          value={profile.email}
          onChange={handleChange}
          placeholder="Enter your email"
        />
      </div>

      <div className="form-group">
        <label htmlFor="semester-input">Current Semester</label>
        <select
          id="semester-input"
          name="semester"
          className="form-control"
          value={profile.semester}
          onChange={handleChange}
        >
          <option value="1">Semester 1</option>
          <option value="2">Semester 2</option>
          <option value="3">Semester 3</option>
          <option value="4">Semester 4</option>
          <option value="5">Semester 5</option>
          <option value="6">Semester 6</option>
          <option value="7">Semester 7</option>
          <option value="8">Semester 8</option>
        </select>
      </div>

      <div className="profile-summary">
        <h3>Live Profile View</h3>
        <p>Name: <strong>{profile.name || 'N/A'}</strong></p>
        <p>Email: <strong>{profile.email || 'N/A'}</strong></p>
        <p>Semester: <strong>Semester {profile.semester}</strong></p>
      </div>
    </section>
  );
}

export default StudentProfile;
