from fastapi import FastAPI, Request
import uvicorn
import psycopg2
import json

app = FastAPI()
conn = psycopg2.connect(
    host="localhost",
    database="SQLDemo",
    user="postgres",
    password="Teja@1704",
    port="5432",
)


@app.get("/hello")
def root():
    return {"message": "Hello World"}


@app.get("/users")
def get_users():
    users = []
    cur = conn.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()
    users = rows
    print(users)
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
    cur= conn.cursor()
    query= "delete from users where id=%s RETURNING name, email, password"
    cur.execute(query, (str(user_id)))
    users= cur.fetchone()
    conn.commit()
    return users
    


@app.post("/users")
async def post_users(request: Request):
    body = await request.body()
    data = json.loads(body)
    email = data.get("email")
    name = data.get("name")
    password = data.get("password")
    cur = conn.cursor()
    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING name, email, password"
    cur.execute(query, (name, email, password))
    users = cur.fetchone()
    conn.commit()
    return users


@app.post("/users/{user_id}")
async def update_user(user_id: int, request: Request):
    cur = conn.cursor()
    body = await request.body()
    data = json.loads(body)
    email = data.get("email")
    query = "Update users set email=%s where id=%s RETURNING name, email, password"
    cur.execute(query, (email, str(user_id)))
    row = cur.fetchone()
    conn.commit()
    users = row
    return users


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, workers=1)
