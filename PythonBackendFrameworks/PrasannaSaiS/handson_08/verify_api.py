import asyncio
import os

import main
from database import AsyncSessionLocal, Department, init_db
from fastapi.testclient import TestClient


async def run_checks():
    if os.path.exists('courses.db'):
        os.remove('courses.db')
    await init_db()

    async with AsyncSessionLocal() as session:
        session.add(Department(name='Computer Science'))
        await session.commit()

    client = TestClient(main.app)
    print('root', client.get('/').json())
    print('docs', client.get('/docs').status_code)

    create_resp = client.post(
        '/api/v1/courses/',
        json={'name': 'FastAPI Basics', 'code': 'FA101', 'credits': 3, 'department_id': 1},
    )
    print('create_course', create_resp.status_code, create_resp.headers.get('location'), create_resp.json())

    second_resp = client.post(
        '/api/v1/courses/',
        json={'name': 'Advanced FastAPI', 'code': 'FA102', 'credits': 4, 'department_id': 1},
    )
    print('create_second_course', second_resp.status_code, second_resp.json())

    paginated = client.get('/api/v1/courses/?page=1&page_size=1')
    print('paginated', paginated.status_code, paginated.json())

    search = client.get('/api/v1/courses/?search=fastapi')
    print('search', search.status_code, search.json())

    patch_resp = client.patch('/api/v1/courses/1/', json={'credits': 5})
    print('patch_course', patch_resp.status_code, patch_resp.json())

    invalid = client.post(
        '/api/v1/courses/',
        json={'name': 'Broken Course', 'code': 'BC999', 'credits': 2, 'department_id': 999},
    )
    print('invalid_department', invalid.status_code, invalid.json())

    missing = client.get('/api/v1/courses/999/')
    print('missing_course', missing.status_code, missing.json())

    delete_resp = client.delete('/api/v1/courses/1/')
    print('delete_course', delete_resp.status_code, delete_resp.text)

    student_resp = client.post('/api/v1/students/', json={'name': 'Alice', 'email': 'alice@example.com'})
    print('create_student', student_resp.status_code, student_resp.headers.get('location'), student_resp.json())

    enrollment_resp = client.post('/api/v1/enrollments/', json={'student_id': 1, 'course_id': 2})
    print('create_enrollment', enrollment_resp.status_code, enrollment_resp.headers.get('location'), enrollment_resp.json())


asyncio.run(run_checks())
