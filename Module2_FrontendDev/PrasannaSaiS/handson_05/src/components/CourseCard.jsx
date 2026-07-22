import React from 'react';
import PropTypes from 'prop-types';

function CourseCard({ id, name, code, credits, grade, isEnrolled, onEnroll }) {
  return (
    <article className="course-card glass">
      <div className="course-header">
        <h3 className="course-title">{name}</h3>
        <span className="course-code">{code}</span>
      </div>
      
      <div className="course-details">
        <div className="course-detail-item">
          Credits: <strong>{credits}</strong>
        </div>
        <div className="course-detail-item">
          Grade: <strong className="grade-badge">{grade}</strong>
        </div>
      </div>
      
      <button 
        className="btn btn-primary" 
        onClick={() => onEnroll({ id, name, code, credits, grade })}
        disabled={isEnrolled}
      >
        {isEnrolled ? 'Enrolled' : 'Enroll'}
      </button>
    </article>
  );
}

CourseCard.propTypes = {
  id: PropTypes.number.isRequired,
  name: PropTypes.string.isRequired,
  code: PropTypes.string.isRequired,
  credits: PropTypes.number.isRequired,
  grade: PropTypes.string.isRequired,
  isEnrolled: PropTypes.bool.isRequired,
  onEnroll: PropTypes.func.isRequired
};

export default CourseCard;
