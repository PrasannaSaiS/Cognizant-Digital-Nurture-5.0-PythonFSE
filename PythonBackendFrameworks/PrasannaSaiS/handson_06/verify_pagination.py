import asyncio
import main
from database import init_db
from fastapi.testclient import TestClient


async def seed_and_check():
    await init_db()
    client = TestClient(main.app)
    # create departments and courses via the API
    department_payloads = [
        {'name': 'Computer Science'},
        {'name': 'Physics'},
    ]
    # departments are not implemented in the API, so seed directly
    from database import Department
    from sqlalchemy.ext.asyncio import AsyncSession
    from database import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        session.add_all([Department(name='Computer Science'), Department(name='Physics')])
        await session.commit()

    payloads = [
        {'name': 'Python Basics', 'code': 'PY101', 'credits': 3, 'department_id': 1},
        {'name': 'Data Science', 'code': 'DS101', 'credits': 4, 'department_id': 1},
        {'name': 'Physics 101', 'code': 'PH101', 'credits': 3, 'department_id': 2},
        {'name': 'Chemistry 101', 'code': 'CH101', 'credits': 3, 'department_id': 2},
    ]
    for payload in payloads:
        client.post('/api/courses/', json=payload)

    print('page1', client.get('/api/courses/?skip=0&limit=2').json())
    print('page2', client.get('/api/courses/?skip=2&limit=2').json())
    print('filtered', client.get('/api/courses/?skip=0&limit=2&department_id=1').json())


asyncio.run(seed_and_check())
