from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.models import Student
from app.schemas import StudentRead, StudentCreate, StudentUpdate
from app.database import get_db
from typing import List

#this is the actual CRUD part of the app


#creating router instance
router= APIRouter()

#CREATE operation using the HTTP POST request
@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
     
    """
        Pattern:
        1) make a SQLAlchemy instance from the validated schema
        2) add it to the session
        3) commit the session
        4) refresh the instance so DB-generated fields (id) are populated
        5) return the instance (FastAPI uses StudentRead to serialize)
    """
    # 1) construct SQLAlchemy model object from schema, model_dump() returns a dict of model fields
    db_student = Student(**student.model_dump())

    # 2) add to session
    db.add(db_student)
    try:
        # 3) commit (will perform INSERT)
        db.commit()
    except Exception as e:
        # If something goes wrong (e.g. unique constraint), rollback and raise a proper HTTP error.
        db.rollback()
        # Optionally detect IntegrityError for more specific messages
        raise HTTPException(status_code=400, detail="Could not create student") from e

    # 4) refresh to load DB-generated fields (like id)
    db.refresh(db_student)

    # 5) return the SQLAlchemy object — response_model handles serialization
    return db_student


#READ operation using the HTTP get request
@router.get("/{student_id}", response_model=StudentRead)
def read_student(student_id: int, db:Session = Depends(get_db)):
    
    #query the db
    db_student = db.query(Student).filter(models.Student.id == student_id).first()

    #if not found raise 404
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    return db_student

#UPDATE operation using the HTTP put request
@router.put("/{student_id}", response_model = StudentRead)
def update_student(student_id: int, student_update: StudentUpdate, db:Session = Depends(get_db)):
    
    # Query DB for existing student
    db_student = db.query(Student).filter(Student.id == student_id).first()

    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Student not found")
    
    #Update only fields that are provided
    update_data = student_update.dict(exclude_unset=True) # exclude_unset ensures optional fields only
    for key, value in update_data.items():
        setattr(db_student, key, value) #update the attribute

    #Commit changes
    db.commit()

    #Refresh to get updated DB values
    db.refresh(db_student)
    
    #Return updated student
    return db_student

#delete operation using the Delete HTTP request
@router.delete("/{student_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):

    #first query db
    db_student = db.query(Student).filter(Student.id == student_id).first()

    if not db_student:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Student not found")
    
    #delete student
    db.delete(db_student)
    db.commit()

    #no content found
    return None

#created a list all students function as get all students end point
@router.get("/", response_model= List[StudentRead])
def list_students(db:Session = Depends(get_db)):
    return db.query(Student).all()

    