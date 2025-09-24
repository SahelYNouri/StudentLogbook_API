from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine


#creating table of students using sqlalchemy ORM
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable= False)
    age = Column(Integer, nullable= False)
    year = Column(Integer, nullable= False)

    enrollments = relationship("Enrollment", back_populates= "student")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key= True)
    course_name = Column(String(100), nullable= False)
    description = Column(Text, nullable= False)

    enrollments = relationship("Enrollment", back_populates= "course")

#creating an association table for many-to-many relationship between students and courses
#each row represents student x enrolled in course y
class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key= True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    #need to create the course and student relationships
    #relationship is a func that shows how two objects are related, backpopulates links the corresponding relationship
    student = relationship("Student", back_populates= "enrollments")
    course = relationship("Course", back_populates= "enrollments")


#Base.metadata is object that keeps track of all table definitions u made
#create all tables in db
Base.metadata.create_all(engine)