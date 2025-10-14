from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Student

#this script is basically going to automatically populate (ie seed) the students table, but will only work if i run the script

fake = Faker()

def seed_students(num_students=50):
    #SessionLocal is a direct session, outside of the FastAPI dependency system which needs get_db
    db: Session = SessionLocal()
    
    try:
        for _ in range(num_students):
            name = fake.name()
            email = fake.unique.email() #make sure all emails are unique like in the tables
            age = fake.random_int(min= 16, max= 27)
            year = fake.random_int(min=1, max= 5)

            #check if student alrady exists by the unqiue email
            existing = db.query(Student).filter(Student.email == email).first()
            if existing:
                continue

            student = Student(name=name, email=email, age=age, year=year)
            db.add(student)

        db.commit()
        print(f"Seeded {num_students} students successfully")
    except Exception as e:
        db.rollback()
        print("Error seeding students:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_students()




