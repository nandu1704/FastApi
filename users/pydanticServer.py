from typing import List
from datetime import datetime
from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import URL, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from utils import hash_password
import hashlib


app = FastAPI()
url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Teja@1704",
    host="localhost",
    port=5432,
    database="SQLDemo",
)
engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(Text)
    created_at = Column(DateTime, default=func.now())


class UserCreateRequest(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


# Base.metadata.create_all(bind=engine)


@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    rows = db.query(Users).all()
    return rows


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    row = db.query(Users).filter(Users.id == user_id).first()
    return row


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()
    return "Deleted Successfully"


# @app.post("/users", response_model=UserResponse)
# async def post_users(user: UserCreatedRequest, db: Session = Depends(get_db)):
#     # This will create pydantic model to dict, because sqlalchemy needed python type structure
#     # using the sqlalchemy orm we have created Users as the orm model for user table
#     hashed_password = password_context.hash(user.password)
#     user.password = hashed_password
#     row = Users(**user.model_dump())
#     db.add(row)
#     db.commit()
#     return row


@app.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreateRequest, db: Session = Depends(get_db)
) -> UserResponse:
    hashed_password = hash_password(user_data.password)
    user_data.password = hashed_password
    user_obj = Users(**user_data.model_dump())
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


@app.post("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, user=UserCreateRequest, db: Session = Depends(get_db)
):
    updated_row = user.model_dump()
    db.query(Users).filter(Users.id == user_id).update(updated_row)
    db.commit()
    return updated_row
