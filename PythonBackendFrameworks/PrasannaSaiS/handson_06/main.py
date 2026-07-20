from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Course, Department, get_db, init_db
from schemas import CourseCreate, CourseResponse, CourseUpdate, DepartmentResponse

app = FastAPI(title='Course Management API', version='1.0')


@app.on_event('startup')
async def startup_event():
    await init_db()


@app.get('/')
async def root():
    return {'message': 'API running'}


@app.post('/api/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    db_course = Course(name=course.name, code=course.code, credits=course.credits, department_id=course.department_id)
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course


@app.get('/api/courses/{course_id}', response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')
    return course


@app.get('/api/courses/', response_model=list[CourseResponse])
async def list_courses(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1),
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Course)
    if department_id is not None:
        query = query.where(Course.department_id == department_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@app.put('/api/courses/{course_id}', response_model=CourseResponse)
async def update_course(course_id: int, course_update: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')

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


@app.delete('/api/courses/{course_id}', status_code=status.HTTP_200_OK)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')

    await db.delete(course)
    await db.commit()
    return {'deleted': True}


@app.get('/api/departments/{department_id}', response_model=DepartmentResponse)
async def get_department(department_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department).where(Department.id == department_id))
    department = result.scalar_one_or_none()
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Department not found')
    return DepartmentResponse(id=department.id, name=department.name, courses=[])
