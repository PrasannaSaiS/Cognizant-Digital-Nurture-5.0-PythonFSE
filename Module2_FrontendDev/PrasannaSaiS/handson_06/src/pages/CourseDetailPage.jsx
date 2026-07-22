import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { courses as fallbackCourses } from '../data';

function CourseDetailPage() {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const numericId = parseInt(courseId, 10);
    // Find in local data first
    const foundLocal = fallbackCourses.find(c => c.id === numericId);
    
    if (foundLocal) {
      setCourse({
        ...foundLocal,
        description: `This course covers foundational principles of ${foundLocal.name} (${foundLocal.code}), with an emphasis on practical implementation, standard paradigms, and industry applications. Students will learn through hands-on design, analysis, and execution.`
      });
      setLoading(false);
    } else {
      // Fetch from API to see if it exists there
      fetch(`https://jsonplaceholder.typicode.com/posts/${courseId}`)
        .then(res => {
          if (!res.ok) throw new Error('Not found');
          return res.json();
        })
        .then(post => {
          const grades = ['A', 'B+', 'A-', 'B', 'A'];
          setCourse({
            id: post.id,
            name: post.title.split(' ').slice(0, 2).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
            code: `CS10${post.id}`,
            credits: (post.id % 3) + 2,
            grade: grades[post.id % grades.length],
            description: post.body
          });
          setLoading(false);
        })
        .catch(() => {
          setLoading(false);
        });
    }
  }, [courseId]);

  if (loading) {
    return (
      <div className="state-message">
        <div className="loading-spinner"></div>
        <p>Loading course details...</p>
      </div>
    );
  }

  if (!course) {
    return (
      <div className="state-message">
        <p className="error-text">Course with ID {courseId} not found.</p>
        <Link to="/courses" className="btn btn-primary" style={{ marginTop: '1.5rem', width: 'auto', display: 'inline-flex', textDecoration: 'none' }}>
          Back to Courses
        </Link>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="course-detail-container glass">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ margin: 0 }}>{course.name}</h2>
          <span className="course-code">{course.code}</span>
        </div>
        
        <div className="detail-row">
          <span>Credits</span>
          <strong>{course.credits} Credits</strong>
        </div>

        <div className="detail-row">
          <span>Expected Grade</span>
          <strong className="grade-badge">{course.grade}</strong>
        </div>

        <div style={{ marginTop: '1rem' }}>
          <h4 style={{ marginBottom: '0.5rem', color: 'var(--accent-secondary)' }}>Course Description</h4>
          <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6' }}>
            {course.description}
          </p>
        </div>

        <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
          <Link to="/courses" className="btn" style={{ flex: 1, backgroundColor: 'rgba(255,255,255,0.05)', color: 'var(--text-primary)', textDecoration: 'none', border: '1px solid var(--border-color)' }}>
            Back to Catalog
          </Link>
        </div>
      </div>
    </div>
  );
}

export default CourseDetailPage;
