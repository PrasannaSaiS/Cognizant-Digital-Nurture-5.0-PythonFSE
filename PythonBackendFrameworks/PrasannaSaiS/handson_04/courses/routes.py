from flask import Blueprint, jsonify, request

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

courses = []
next_id = 1


def make_response_json(data, status_code=200):
    status_label = 'success' if status_code < 400 else 'error'
    return jsonify({'status': status_label, 'data': data}), status_code


@courses_bp.route('/', methods=['GET'])
def list_courses():
    return make_response_json(courses)


@courses_bp.route('/', methods=['POST'])
def create_course():
    payload = request.get_json(silent=True)
    if not payload:
        return make_response_json({'error': 'Request body must be JSON'}, 400)

    name = payload.get('name')
    code = payload.get('code')
    credits = payload.get('credits')

    if not name or not code or credits is None:
        return make_response_json({'error': 'name, code, and credits are required'}, 400)

    global next_id
    course = {
        'id': next_id,
        'name': name,
        'code': code,
        'credits': credits,
    }
    courses.append(course)
    next_id += 1
    return make_response_json(course, 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = next((item for item in courses if item['id'] == course_id), None)
    if course is None:
        return make_response_json({'error': 'Course not found'}, 404)
    return make_response_json(course)


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    payload = request.get_json(silent=True)
    if not payload:
        return make_response_json({'error': 'Request body must be JSON'}, 400)

    course = next((item for item in courses if item['id'] == course_id), None)
    if course is None:
        return make_response_json({'error': 'Course not found'}, 404)

    if 'name' in payload:
        course['name'] = payload['name']
    if 'code' in payload:
        course['code'] = payload['code']
    if 'credits' in payload:
        course['credits'] = payload['credits']

    return make_response_json(course)


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    global courses
    course = next((item for item in courses if item['id'] == course_id), None)
    if course is None:
        return make_response_json({'error': 'Course not found'}, 404)

    courses = [item for item in courses if item['id'] != course_id]
    return make_response_json({'deleted': True}, 200)
