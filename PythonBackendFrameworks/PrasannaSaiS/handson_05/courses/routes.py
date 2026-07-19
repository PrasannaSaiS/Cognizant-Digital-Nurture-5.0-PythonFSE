from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from courses.models import Course, Department, Student, Enrollment, db

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


def make_response_json(data, status_code=200):
    status_label = 'success' if status_code < 400 else 'error'
    return jsonify({'status': status_label, 'data': data}), status_code


@courses_bp.route('/', methods=['GET'])
def list_courses():
    courses = Course.query.all()
    return make_response_json([course.to_dict() for course in courses])


@courses_bp.route('/', methods=['POST'])
def create_course():
    payload = request.get_json(silent=True)
    if not payload:
        return make_response_json({'error': 'Request body must be JSON'}, 400)

    name = payload.get('name')
    code = payload.get('code')
    credits = payload.get('credits')
    department_id = payload.get('department_id')

    if not name or not code or credits is None or department_id is None:
        return make_response_json({'error': 'name, code, credits, and department_id are required'}, 400)

    course = Course(name=name, code=code, credits=credits, department_id=department_id)
    db.session.add(course)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return make_response_json({'error': 'A course with this code already exists'}, 400)
    return make_response_json(course.to_dict(), 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return make_response_json(course.to_dict())


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    payload = request.get_json(silent=True)
    if not payload:
        return make_response_json({'error': 'Request body must be JSON'}, 400)

    course = Course.query.get_or_404(course_id)
    if 'name' in payload:
        course.name = payload['name']
    if 'code' in payload:
        course.code = payload['code']
    if 'credits' in payload:
        course.credits = payload['credits']
    if 'department_id' in payload:
        course.department_id = payload['department_id']

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return make_response_json({'error': 'A course with this code already exists'}, 400)
    return make_response_json(course.to_dict())


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return make_response_json({'deleted': True})


@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def get_course_students(course_id):
    course = Course.query.get_or_404(course_id)
    students = (
        db.session.query(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .filter(Enrollment.course_id == course.id)
        .all()
    )
    return make_response_json([student.to_dict() for student in students])
