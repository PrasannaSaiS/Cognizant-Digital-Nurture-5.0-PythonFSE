import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')

import django

django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from courses.models import Department, Course, Student, Enrollment

user_model = get_user_model()
user = user_model.objects.get(username='admin')
user.set_password('Admin@123')
user.save()

client = Client(HTTP_HOST='127.0.0.1')
client.force_login(user)

cs, _ = Department.objects.get_or_create(name='Computer Science', defaults={'head_of_dept': 'Dr. Rao', 'budget': 250000.00})
maths, _ = Department.objects.get_or_create(name='Mathematics', defaults={'head_of_dept': 'Prof. Kumar', 'budget': 180000.00})
physics, _ = Department.objects.get_or_create(name='Physics', defaults={'head_of_dept': 'Dr. Singh', 'budget': 200000.00})

course_payloads = [
    {'name': 'Algorithms', 'code': 'CS401', 'credits': 4, 'department': cs.id},
    {'name': 'Database Systems', 'code': 'CS402', 'credits': 3, 'department': cs.id},
    {'name': 'Quantum Mechanics', 'code': 'PHY301', 'credits': 4, 'department': physics.id},
]
created_courses = []
for payload in course_payloads:
    course, created = Course.objects.get_or_create(code=payload['code'], defaults={
        'name': payload['name'],
        'credits': payload['credits'],
        'department_id': payload['department'],
    })
    created_courses.append(course)

student_payloads = [
    {'first_name': 'Alice', 'last_name': 'Brown', 'email': 'alice@example.com', 'department': cs.id, 'enrollment_year': 2024},
    {'first_name': 'Bob', 'last_name': 'Green', 'email': 'bob@example.com', 'department': cs.id, 'enrollment_year': 2023},
    {'first_name': 'Carol', 'last_name': 'White', 'email': 'carol@example.com', 'department': maths.id, 'enrollment_year': 2022},
    {'first_name': 'Diana', 'last_name': 'Miller', 'email': 'diana@example.com', 'department': physics.id, 'enrollment_year': 2024},
    {'first_name': 'Evan', 'last_name': 'Clark', 'email': 'evan@example.com', 'department': cs.id, 'enrollment_year': 2021},
]
created_students = []
for payload in student_payloads:
    student, created = Student.objects.get_or_create(email=payload['email'], defaults={
        'first_name': payload['first_name'],
        'last_name': payload['last_name'],
        'department_id': payload['department'],
        'enrollment_year': payload['enrollment_year'],
    })
    created_students.append(student)

# Create enrollments via the admin add view
for student, course in [
    (created_students[0], created_courses[0]),
    (created_students[1], created_courses[1]),
    (created_students[2], created_courses[0]),
    (created_students[3], created_courses[2]),
]:
    response = client.post(reverse('admin:courses_enrollment_add'), {'student': student.id, 'course': course.id})
    if response.status_code not in {302, 200}:
        raise RuntimeError(f'Enrollment creation failed with status {response.status_code}')

# Validate duplicate enrollment in the admin form
response = client.post(reverse('admin:courses_enrollment_add'), {'student': created_students[0].id, 'course': created_courses[0].id})
print('Duplicate enrollment status:', response.status_code)
print('Duplicate enrollment errors:', response.context['adminform'].form.errors if response.context and 'adminform' in response.context else 'No adminform in context')
print('Course count:', Course.objects.count())
print('Student count:', Student.objects.count())
print('Enrollment count:', Enrollment.objects.count())
