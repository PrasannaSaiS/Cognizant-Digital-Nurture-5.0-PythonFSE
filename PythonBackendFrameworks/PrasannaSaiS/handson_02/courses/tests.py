from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Course, Department, Enrollment, Student


class EnrollmentModelTests(TestCase):
    def setUp(self):
        department = Department.objects.create(name='Computer Science', head_of_dept='Dr. Rao', budget=100000.00)
        self.course = Course.objects.create(name='Algorithms', code='CS401', credits=4, department=department)
        self.student = Student.objects.create(first_name='Alice', last_name='Brown', email='alice@example.com', department=department, enrollment_year=2024)

    def test_duplicate_enrollment_is_rejected(self):
        Enrollment.objects.create(student=self.student, course=self.course)

        with self.assertRaises(ValidationError):
            Enrollment.objects.create(student=self.student, course=self.course)
