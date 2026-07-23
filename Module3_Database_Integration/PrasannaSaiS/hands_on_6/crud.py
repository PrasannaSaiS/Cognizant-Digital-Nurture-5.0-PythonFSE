# =============================================================================
# Task 2: CRUD Operations via ORM & Task 3: Eager Loading [cite: 438, 451]
# =============================================================================

from sqlalchemy.orm import sessionmaker, joinedload
from datetime import date
from Module3_Database_Integration.PrasannaSaiS.hands_on_6.models import engine, Department, Student, Course, Enrollment, Professor

# Step 80: Open a Session [cite: 439]
Session = sessionmaker(bind=engine)
session = Session()

# -----------------------------------------------------------------------------
# Task 2: CRUD Operations
# -----------------------------------------------------------------------------

# Step 81: INSERT 3 Departments and 5 Students [cite: 440]
d1 = Department(dept_name='Computer Science', hod_name='Dr. Ramesh', budget=850000)
d2 = Department(dept_name='Electronics', hod_name='Dr. Priya', budget=620000)
d3 = Department(dept_name='Mechanical', hod_name='Dr. Suresh', budget=540000)
session.add_all([d1, d2, d3])
session.commit()

s1 = Student(first_name='Arjun', last_name='Mehta', email='arjun@college.edu', date_of_birth=date(2003, 4, 12), department_id=d1.department_id, enrollment_year=2022)
s2 = Student(first_name='Priya', last_name='Suresh', email='priya@college.edu', date_of_birth=date(2003, 7, 25), department_id=d1.department_id, enrollment_year=2022)
s3 = Student(first_name='Rohan', last_name='Verma', email='rohan@college.edu', date_of_birth=date(2002, 11, 8), department_id=d2.department_id, enrollment_year=2021)
s4 = Student(first_name='Sneha', last_name='Patel', email='sneha@college.edu', date_of_birth=date(2004, 1, 30), department_id=d3.department_id, enrollment_year=2023)
s5 = Student(first_name='Vikram', last_name='Das', email='vikram@college.edu', date_of_birth=date(2003, 9, 14), department_id=d1.department_id, enrollment_year=2022)
session.add_all([s1, s2, s3, s4, s5])
session.commit()

# Step 82: INSERT 3 Courses and 4 Enrollments [cite: 441]
c1 = Course(course_name='Data Structures', course_code='CS101', credits=4, department_id=d1.department_id)
c2 = Course(course_name='Circuit Theory', course_code='EC101', credits=3, department_id=d2.department_id)
c3 = Course(course_name='Thermodynamics', course_code='ME101', credits=3, department_id=d3.department_id)
session.add_all([c1, c2, c3])
session.commit()

e1 = Enrollment(student_id=s1.student_id, course_id=c1.course_id, enrollment_date=date(2022, 7, 1), grade='A')
e2 = Enrollment(student_id=s2.student_id, course_id=c1.course_id, enrollment_date=date(2022, 7, 1), grade='B')
e3 = Enrollment(student_id=s3.student_id, course_id=c2.course_id, enrollment_date=date(2021, 7, 1), grade='A')
e4 = Enrollment(student_id=s4.student_id, course_id=c3.course_id, enrollment_date=date(2023, 7, 1), grade=None)
session.add_all([e1, e2, e3, e4])
session.commit()

# Step 83: READ - Query all students in department 'Computer Science' [cite: 442]
cs_students = session.query(Student).join(Department).filter(Department.dept_name == 'Computer Science').all()

# Step 84: READ - Query all enrollments and print names (Demonstrates N+1 Anti-Pattern) [cite: 443]
# With echo=True, this loop will log 1 initial query + multiple isolated relationship fetches [cite: 444]
enrollments_lazy = session.query(Enrollment).all()
for e in enrollments_lazy:
    print(f"Student: {e.student.first_name}, Course: {e.course.course_name}")

# Step 85: UPDATE - Find specific student by email and update enrollment_year [cite: 445]
student_to_update = session.query(Student).filter_by(email='arjun@college.edu').first()
if student_to_update:
    student_to_update.enrollment_year = 2024
    session.commit()

# Step 86: DELETE - Remove an enrollment record where grade is NULL [cite: 446]
enrollment_to_delete = session.query(Enrollment).filter_by(grade=None).first()
if enrollment_to_delete:
    session.delete(enrollment_to_delete)
    session.commit()


# -----------------------------------------------------------------------------
# Task 3: Eager Loading to Fix N+1
# -----------------------------------------------------------------------------

"""
Steps 87, 89, 90: N+1 Comparison Documentation [cite: 452, 453, 454]
- Lazy Loading (Step 84): Executed 1 query for Enrollments, plus 1 additional query 
  per accessed Student and Course relation, resulting in 9 total queries for 4 records.
- Eager Loading (Step 88): Executes exactly 1 SQL statement using a LEFT OUTER JOIN 
  to fetch all relations simultaneously, eliminating the N+1 problem.
"""

# Step 88: Rewrite the query using joinedload [cite: 453]
enrollments_eager = session.query(Enrollment).options(
    joinedload(Enrollment.student),
    joinedload(Enrollment.course)
).all()

for e in enrollments_eager:
    print(f"Student: {e.student.first_name}, Course: {e.course.course_name}")

session.close()