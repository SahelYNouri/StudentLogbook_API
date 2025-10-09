from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models
from app.schemas import EnrollmentCreate, EnrollmentRead
from app.database import get_db
from typing import List

router= APIRouter()

#Create enrollment
@router.post("/", respnse_model= EnrollmentRead, status_code= status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentCreate, db: Session= Depends(get_db)):

    #check if student and course exists
    student = db.query(models.Student).filter(models.Student.id == enrollment.student_id).first()
    course= db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()

    if not student or not course:
        raise HTTPException(status_code= 404, detail= "Student or course not found")
    
    #check if enrollment already exists
    existing= db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.student_id == enrollment.student_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail= "Enrollemnt already exists")
    
    db_enrollment = models.Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment



#Read enrollment by id
@router.get("/{enrollment_id}", response_model= EnrollmentRead)
def read_enrollment(enrollment_id: int, db: Session= Depends(get_db)):

    db_enrollment= db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not db_enrollment:
        raise HTTPException(status_code= 404, detail= "Enrollment not found")
   
    return db_enrollment



#List all enrollments
@router.get("/", response_model= List[EnrollmentRead])
def list_enrollments(db: Session = Depends(get_db)):
    
    return db.query(models.Enrollment).all()

#Not creating an update function as it doesnt make sense to update enrollments, jsut create a new one instead

#delete enrollment
@router.delete("/{enrollment_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):

    db_enrollment = db.query(models.enrollment).filter(models.Enrollment.id == enrollment_id)
    if not db_enrollment:
        raise HTTPException(status_code=404, detail= "Enrollment not found")
    
    db.delete(db_enrollment)
    db.commit()

    return None




    

