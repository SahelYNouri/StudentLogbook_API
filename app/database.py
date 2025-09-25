import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

#all tables are created using the base class (just python classes that extend Base)
from sqlalchemy.orm import declarative_base, sessionmaker

#So in this project, instead of using psycopg2, ill use SQLAlchemy which is an ORM (object Relational Mapper)
#An ORM allows us to interact with the databse using python objects instead of writing raw SQL queries like in psycopg2


#engine is an object that manages the db connection and connection pooling
#note that SQLAlchemy uses the psycopg2 driver to connect to the postgres db

load_dotenv()
host= os.getenv("HOST")
dbname= os.getenv("DB_NAME")
user= os.getenv("USER")
password= os.getenv("PASSWORD") 
port = os.getenv("PORT")

Base = declarative_base()
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")


#use session to interact with db and commit, query, etc
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine) #links session to db engine






