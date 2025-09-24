#main fastapi file
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from app import routes, database, models
from typing import List, Annotated

#creating a new FastAPI instance
app = FastAPI()
app.include_router(routes.routes)
