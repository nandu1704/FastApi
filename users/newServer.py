from fastapi import FastAPI, Request
import uvicorn
import psycopg2
import json
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import URL, Column, Integer, String, Text
from sqlalchemy import create_engine



app = FastAPI()
conn = psycopg2.connect(
    host="localhost",
    database="SQLDemo",
    user="postgres",
    password="Teja@1704",
    port="5432",
)

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Teja@1704",
    host="localhost",
    port=5432,
    database="SQLDemo",
)
# DATABASE_URL = "postgresql://postgres:Teja%401704@localhost:5432/SQLDemo"
# engine = create_engine(DATABASE_URL)
engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class BaseModel(Base):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(Text)
    updated_at = Column(Text)


class Users(BaseModel):
    __tablename__ = "users"
    # id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(Text)
    # created_at = Column(Text)
    # updated_at = Column(Text)


class Products(BaseModel):
    __tablename__ = "products"
    # id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(Text)
    # created_at = Column(Text)
    # updated_at = Column(Text)


# Base.metadata.create_all(bind=engine)


@app.get("/hello")
def root():
    return {"message": "Hello World"}


@app.get("/users")
def get_users():
    # users = []
    # cur = conn.cursor()
    # cur.execute("select * from users")
    # rows = cur.fetchall()
    # users = rows
    # print(users)
    # return users
    db = SessionLocal()
    rows = db.query(Users).all()
    users = []
    for row in rows:
        print(row.id, row.name, row.email, row.password)
        users.append({"id": row.id, "name": row.name})
    db.close()
    return users


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    cur = conn.cursor()
    query = "select * from users where id=%s"
    cur.execute(query, (str(user_id)))
    row = cur.fetchone()
    users = row
    return users


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    # cur = conn.cursor()
    # query = "delete from users where id=%s RETURNING name, email, password"
    # cur.execute(query, (str(user_id)))
    # users = cur.fetchone()
    # conn.commit()
    db = SessionLocal()
    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()
    db.close()
    return "Deleted Successfully"


@app.post("/users")
async def post_users(request: Request):
    db = SessionLocal()
    body = await request.body()
    data = json.loads(body)
    email = data.get("email")
    name = data.get("name")
    password = data.get("password")
    # cur = conn.cursor()
    # query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING name, email, password"
    # cur.execute(query, (name, email, password))
    # users = cur.fetchone()
    # conn.commit()
    row = Users(name=name, email=email, password=password)
    db.add(row)
    db.commit()
    db.refresh(row)
    db.close()
    print(row)
    return row


@app.post("/users/{user_id}")
async def update_user(user_id: int, request: Request):
    # cur = conn.cursor()
    db = SessionLocal()
    body = await request.body()
    data = json.loads(body)
    email = data.get("email")
    # query = "Update users set email=%s where id=%s RETURNING name, email, password"
    # cur.execute(query, (email, str(user_id)))
    # row = cur.fetchone()
    # conn.commit()
    row = db.query(Users).filter(Users.id == user_id).first()
    row.email = email
    db.commit()
    db.refresh(row)
    db.close()
    return {row.id, row.name, row.email}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000, workers=1)
