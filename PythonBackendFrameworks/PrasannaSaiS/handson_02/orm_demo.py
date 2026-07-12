import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
django.setup()

from django.db import connection
from django.db.models import Count, F
from courses.models import Department, Course, Student

cs, _ = Department.objects.get_or_create(
    name='Computer Science',
    defaults={'head_of_dept': 'Dr. Ada', 'budget': 100000.00},
)
maths, _ = Department.objects.get_or_create(
    name='Mathematics',
    defaults={'head_of_dept': 'Prof. Lin', 'budget': 80000.00},
)

Course.objects.get_or_create(name='Python Programming', defaults={'code': 'CS101', 'credits': 3, 'department': cs})
Course.objects.get_or_create(name='Data Structures', defaults={'code': 'CS102', 'credits': 4, 'department': cs})
Course.objects.get_or_create(name='Calculus I', defaults={'code': 'MATH101', 'credits': 3, 'department': maths})
Course.objects.get_or_create(name='Linear Algebra', defaults={'code': 'MATH102', 'credits': 3, 'department': maths})

Student.objects.get_or_create(email='alice@example.com', defaults={'first_name': 'Alice', 'last_name': 'Ng', 'department': cs, 'enrollment_year': 2024})
Student.objects.get_or_create(email='bob@example.com', defaults={'first_name': 'Bob', 'last_name': 'Kumar', 'department': cs, 'enrollment_year': 2023})
Student.objects.get_or_create(email='carol@example.com', defaults={'first_name': 'Carol', 'last_name': 'Davis', 'department': maths, 'enrollment_year': 2022})
Student.objects.get_or_create(email='david@example.com', defaults={'first_name': 'David', 'last_name': 'Singh', 'department': maths, 'enrollment_year': 2024})
Student.objects.get_or_create(email='eva@example.com', defaults={'first_name': 'Eva', 'last_name': 'Lee', 'department': cs, 'enrollment_year': 2021})

print('Courses in Computer Science:')
print(list(Course.objects.filter(department__name='Computer Science').values('name', 'code')))

print('Course counts per department:')
print(list(Department.objects.annotate(course_count=Count('courses')).values('name', 'course_count')))

connection.queries_log.clear()
students = list(Student.objects.select_related('department').all())
print('Selected students with department info:')
for student in students:
    print(student.first_name, student.department.name)
print('SQL queries used:', len(connection.queries))

Department.objects.update(budget=F('budget') * 1.1)
print('Updated department budgets:')
print(list(Department.objects.values('name', 'budget')))
