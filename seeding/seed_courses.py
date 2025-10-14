from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Course

faker = Faker()

course_list=  ["Math 101", "English 201", "Physics 202", "History 101"]

descriptions = [
    "An introductory course in algebra, calculus, and other foundational math concepts.",
    "A study of literature, grammar, and writing skills in English language.",
    "An overview of classical and modern physics, including mechanics and thermodynamics.",
    "A survey of world history, from ancient civilizations to modern times."
]


def seed_courses(num_courses = 10):
    db: Session = SessionLocal()

    try:
        for name, desc in zip(course_list, descriptions):
            
            existing = db.query(Course).filter(Course.name == name).first()
            if existing:
                continue

            course = Course(name = name, description= desc)
            db.add(Course)

        db.commit()
        print(f"Seeded {len(course_list)} courses successfully")
    except Exception as e:
        db.rollback()
        print("Error seeding courses")
    finally:
        db.close()

if __name__ == "__main__":
    seed_courses()
