#main fastapi file
from fastapi import FastAPI, HTTPException, Depends
from app.database import SessionLocal


#importing the api router objects from the route files
from routes.students import router as students_router
from routes.courses import router as courses_router
from routes.enrollment import router as enrollment_router

from pydantic import BaseModel
from app import routes, database, models
from typing import List, Annotated
from sqlalchemy.orm import Session

#creating FastAPI instance
app = FastAPI()
app.include_router(students_router, prefix= "/students", tags=["Students"])
app.include_router(courses_router, prefix= "/courses", tags= ["Courses"])
app.include_router(enrollment_router, prefix= "/enrollments", tags= ["Enrollments"])
