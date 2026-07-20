import asyncio
import main
from database import init_db
from fastapi.testclient import TestClient


async def run_checks():
    await init_db()
    client = TestClient(main.app)
    print('root', client.get('/').json())
    print('docs', client.get('/docs').status_code)
    response = client.post('/api/courses/', json={'name': 'Bad', 'code': '', 'credits': 'x', 'department_id': 'a'})
    print('invalid', response.status_code, response.json())


asyncio.run(run_checks())
