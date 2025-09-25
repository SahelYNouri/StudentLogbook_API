#schema layer (validation/serialization) using pydantic
#this layer of the project defines strucutre of the data when it enters or leaves the API
#FastAPI uses pydantic models(classes/schemas)

#scehmas are rules for my API, says what data is valid and how it should be returned

#classes inherit from basemodel, Optional for opitonal fiels
from pydantic import BaseModel
from typing import Optional

#input schema for creating a student
class StudentCreate(BaseModel):
    name: str
    age:int
    email:str
    year: int

#output schema for returning a student
class StudentRead(BaseModel):
    id: int
    name: str
    age: int
    email: str
    year: int

    class Config:
        orm_mode = True  

class StudentUpdate(BaseModel):
    name: Optional[str]= None
    age: Optional[int]= None
    email: Optional[str]= None
    year: Optional[int]= None

class CourseRead(BaseModel):
    id: int
    course_name:str
    description: str
    
    class Config:
        orm_mode = True  

class CourseCreate(BaseModel):
    course_name: str
    description: str

class CourseUpdate(BaseModel):
    course_name: Optional[str]= None
    description: Optional[str]= None

class EnrollmentCreate(BaseModel):

    student_id: int
    course_id: int

class EnrollmentRead(BaseModel):
    id: int
    student_id: int
    course_id: int

    class Config:
        orm_mode = True  

