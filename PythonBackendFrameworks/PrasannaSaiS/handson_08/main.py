from math import ceil
from typing import Optional

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Query, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Course, Department, Enrollment, Student, get_db, init_db
from schemas import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
    DepartmentResponse,
    EnrollmentCreate,
    EnrollmentResponse,
    StudentCreate,
    StudentResponse,
)

app = FastAPI(
    title='Course Management API',
    description='RESTful course management APIs for the Digital Nurture 5.0 hands-on exercises.',
    version='1.0',
    contact={'name': 'Prasanna Sai', 'email': 'prasanna@example.com'},
)


# URL versioning is used here for visibility. A header-based alternative would be
# Accept: application/vnd.api+json;version=1, which keeps URLs cleaner but is harder to test in a browser.


@app.on_event('startup')
async def startup_event():
    await init_db()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    if isinstance(detail, dict) and 'error' in detail:
        payload = detail
        code = payload['error'].get('code', 'HTTP_ERROR')
        message = payload['error'].get('message', 'Request failed')
        field = payload['error'].get('field')
    else:
        code = status_code_to_code(exc.status_code)
        message = str(detail) if detail else 'Request failed'
        field = None
        payload = {'error': {'code': code, 'message': message, 'field': field}}
    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={'error': {'code': 'VALIDATION_ERROR', 'message': 'Request validation failed', 'field': None}},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'error': {'code': 'INTERNAL_SERVER_ERROR', 'message': 'Internal server error', 'field': None}},
    )


@app.get('/')
async def root():
    return {'message': 'API running'}


@app.post(
    '/api/v1/courses/',
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Courses'],
    summary='Create a course',
    response_description='The newly created course',
)
async def create_course(course: CourseCreate, response: Response, db: AsyncSession = Depends(get_db)):
    department = await db.get(Department, course.department_id)
    if department is None:
        raise_api_error(status.HTTP_400_BAD_REQUEST, f'Department with id {course.department_id} does not exist', 'BAD_REQUEST', 'department_id')

    db_course = Course(name=course.name, code=course.code, credits=course.credits, department_id=course.department_id)
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)

    response.status_code = status.HTTP_201_CREATED
    response.headers['Location'] = f'/api/v1/courses/{db_course.id}/'
    return db_course


@app.get('/api/v1/courses/{course_id}/', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise_api_error(status.HTTP_404_NOT_FOUND, f'Course with id {course_id} does not exist', 'NOT_FOUND', None)
    return course


@app.get('/api/v1/courses/', response_model=dict, tags=['Courses'])
async def list_courses(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    base_query = select(Course)
    if search:
        search_term = f'%{search.lower()}%'
        base_query = base_query.where(or_(func.lower(Course.name).like(search_term), func.lower(Course.code).like(search_term)))

    count_query = select(func.count()).select_from(base_query.subquery())
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    offset = (page - 1) * page_size
    result = await db.execute(base_query.offset(offset).limit(page_size))
    courses = result.scalars().all()

    base_url = str(request.base_url).rstrip('/') + '/api/v1/courses/'
    next_url = None
    previous_url = None
    if page * page_size < total:
        next_url = build_paginated_url(base_url, page + 1, page_size, search)
    if page > 1:
        previous_url = build_paginated_url(base_url, page - 1, page_size, search)

    return {
        'count': total,
        'next': next_url,
        'previous': previous_url,
        'results': [serialize_course(course) for course in courses],
    }


@app.put('/api/v1/courses/{course_id}/', response_model=CourseResponse, tags=['Courses'])
async def replace_course(course_id: int, course_update: CourseCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise_api_error(status.HTTP_404_NOT_FOUND, f'Course with id {course_id} does not exist', 'NOT_FOUND', None)

    course.name = course_update.name
    course.code = course_update.code
    course.credits = course_update.credits
    course.department_id = course_update.department_id

    await db.commit()
    await db.refresh(course)
    return course


@app.patch('/api/v1/courses/{course_id}/', response_model=CourseResponse, tags=['Courses'])
async def patch_course(course_id: int, course_update: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise_api_error(status.HTTP_404_NOT_FOUND, f'Course with id {course_id} does not exist', 'NOT_FOUND', None)

    if course_update.name is not None:
        course.name = course_update.name
    if course_update.code is not None:
        course.code = course_update.code
    if course_update.credits is not None:
        course.credits = course_update.credits
    if course_update.department_id is not None:
        course.department_id = course_update.department_id

    await db.commit()
    await db.refresh(course)
    return course


@app.delete('/api/v1/courses/{course_id}/', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise_api_error(status.HTTP_404_NOT_FOUND, f'Course with id {course_id} does not exist', 'NOT_FOUND', None)

    await db.delete(course)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get('/api/v1/courses/{course_id}/students/', response_model=list[StudentResponse], tags=['Courses'])
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if course is None:
        raise_api_error(status.HTTP_404_NOT_FOUND, f'Course with id {course_id} does not exist', 'NOT_FOUND', None)

    result = await db.execute(
        select(Student).join(Enrollment, Enrollment.student_id == Student.id).where(Enrollment.course_id == course_id)
    )
    return result.scalars().all()


@app.get('/api/v1/students/', response_model=list[StudentResponse], tags=['Students'])
async def list_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return result.scalars().all()


@app.post('/api/v1/students/', response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=['Students'])
async def create_student(student: StudentCreate, response: Response, db: AsyncSession = Depends(get_db)):
    db_student = Student(name=student.name, email=student.email)
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)

    response.status_code = status.HTTP_201_CREATED
    response.headers['Location'] = f'/api/v1/students/{db_student.id}/'
    return db_student


@app.post('/api/v1/enrollments/', response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED, tags=['Enrollments'])
async def create_enrollment(
    enrollment: EnrollmentCreate,
    response: Response,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    student = await db.get(Student, enrollment.student_id)
    course = await db.get(Course, enrollment.course_id)
    if student is None:
        raise_api_error(status.HTTP_400_BAD_REQUEST, f'Student with id {enrollment.student_id} does not exist', 'BAD_REQUEST', 'student_id')
    if course is None:
        raise_api_error(status.HTTP_400_BAD_REQUEST, f'Course with id {enrollment.course_id} does not exist', 'BAD_REQUEST', 'course_id')

    db_enrollment = Enrollment(student_id=enrollment.student_id, course_id=enrollment.course_id)
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)

    response.status_code = status.HTTP_201_CREATED
    response.headers['Location'] = f'/api/v1/enrollments/{db_enrollment.id}/'
    background_tasks.add_task(send_confirmation_email, student.email)
    return db_enrollment


@app.get('/api/v1/departments/{department_id}/', response_model=DepartmentResponse, tags=['Departments'])
async def get_department(department_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department).where(Department.id == department_id))
    department = result.scalar_one_or_none()
    if department is None:
        raise_api_error(status.HTTP_404_NOT_FOUND, f'Department with id {department_id} does not exist', 'NOT_FOUND', None)
    return DepartmentResponse(id=department.id, name=department.name, courses=[])


def build_paginated_url(base_url: str, page: int, page_size: int, search: Optional[str]) -> str:
    params = [f'page={page}', f'page_size={page_size}']
    if search:
        params.append(f'search={search}')
    return f'{base_url}?{"&".join(params)}'


def serialize_course(course: Course) -> dict:
    return {'id': course.id, 'name': course.name, 'code': course.code, 'credits': course.credits, 'department_id': course.department_id}


def raise_api_error(status_code: int, message: str, code: str, field: Optional[str]):
    raise HTTPException(
        status_code=status_code,
        detail={'error': {'code': code, 'message': message, 'field': field}},
    )


def status_code_to_code(status_code: int) -> str:
    mapping = {
        400: 'BAD_REQUEST',
        401: 'UNAUTHORIZED',
        404: 'NOT_FOUND',
        422: 'VALIDATION_ERROR',
        500: 'INTERNAL_SERVER_ERROR',
    }
    return mapping.get(status_code, 'HTTP_ERROR')


def send_confirmation_email(student_email: str):
    print(f'Sending confirmation to {student_email}')
