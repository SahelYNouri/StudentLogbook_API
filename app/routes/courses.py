from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.models import Course
from app.schemas import CourseRead, CourseCreate, CourseUpdate
from app.database import get_db
from typing import List

router = APIRouter()

#Create operation
@router.post("/", response_model= CourseRead, status_code= status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    
    db_course = Course(**course.model_dump())

    db.add(db_course)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code= 400, detail="Could not create student")
    
    db.refresh(db_course)

    return db_course



#READ operation using get req
@router.get("/{course_id}", response_model= CourseRead)
def read_course(course_id: int, db:Session = Depends(get_db)):

    db_course = db.query(Course).filter(models.Course.id == course_id).first()

    if not db_course:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Course not found")
    
    return db_course



#Update operation
@router.put("/{course_id}", response_model = CourseRead)
def update_course(course_id: int, course_update: CourseUpdate, db: Session = Depends(get_db)):

    db_course= db.query(Course).filter(Course.id == course_id).first()

    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Course not found")
    
    update_data = course_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_course, key, value)

    db.commit()

    db.refresh(db_course)

    return db_course



@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session= Depends(get_db)):

    db_course = db.query(Course).filter(Course.id == course_id).first()

    if not db_course:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Course not found")
    
    db.delete(db_course)
    db.commit()

    return None



@router.get("/", response_model=List[CourseRead])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()
