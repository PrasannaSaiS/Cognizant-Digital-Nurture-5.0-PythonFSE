import asyncio
import main
from database import init_db
from fastapi.testclient import TestClient


async def run_checks():
    await init_db()
    client = TestClient(main.app)
    print('root', client.get('/').json())
    print('docs', client.get('/docs').status_code)

    create_resp = client.post('/api/courses/', json={'name': 'FastAPI Basics', 'code': 'FA101', 'credits': 3, 'department_id': 1})
    print('create_course', create_resp.status_code, create_resp.json())

    missing = client.get('/api/courses/999')
    print('missing_course', missing.status_code, missing.json())

    delete_resp = client.delete('/api/courses/1')
    print('delete_course', delete_resp.status_code, delete_resp.text)

    student_resp = client.post('/api/students/', json={'name': 'Alice', 'email': 'alice@example.com'})
    print('create_student', student_resp.status_code, student_resp.json())

    enrollment_resp = client.post('/api/enrollments/', json={'student_id': 1, 'course_id': 1})
    print('create_enrollment', enrollment_resp.status_code, enrollment_resp.json())


asyncio.run(run_checks())
