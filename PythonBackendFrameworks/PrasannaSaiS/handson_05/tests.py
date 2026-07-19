import unittest

from app import create_app
from courses.models import db, Course, Department, Student, Enrollment


class CourseApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            dept = Department(name='Computer Science')
            db.session.add(dept)
            db.session.commit()
            course = Course(name='Python Basics', code='PY101', credits=3, department_id=dept.id)
            db.session.add(course)
            db.session.commit()
            student = Student(name='Alice', email='alice@example.com')
            db.session.add(student)
            db.session.commit()
            enrollment = Enrollment(student_id=student.id, course_id=course.id)
            db.session.add(enrollment)
            db.session.commit()

    def test_list_courses(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload['status'], 'success')
        self.assertEqual(len(payload['data']), 1)

    def test_create_course(self):
        response = self.client.post('/api/courses/', json={
            'name': 'Django Basics',
            'code': 'DJ102',
            'credits': 4,
            'department_id': 1,
        })
        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertEqual(payload['data']['code'], 'DJ102')

    def test_students_route(self):
        response = self.client.get('/api/courses/1/students/')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload['data'][0]['name'], 'Alice')


if __name__ == '__main__':
    unittest.main()
