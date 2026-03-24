import json
from fastapi import APIRouter, Request
from database import sessionLocal
from models import Employees


router = APIRouter()
@router.get("/")
def root():
    return {"status": "server working"}


@router.get("/employee")
async def get_employees():
    try:
        db = sessionLocal()
        rows = db.query(Employees).all()
    finally:
        db.close()
    return rows


@router.get("/employee/{id}")
async def get_employee_by_id(id: int):
    db = sessionLocal()
    row = db.query(Employees).filter(Employees.employee_id == id).all()
    db.close()
    return row


@router.post("/employees")
# async def add_employee(data: dict):
async def add_employee(data: dict, request: Request):
    db = sessionLocal()
    body = await request.body()
    data = json.loads(body)
    rows = Employees(first_name=data.get("first_name"), last_name=data.get("last_name"))
    db.add(rows)
    db.commit()
    db.refresh(rows)
    db.close()
    return rows


@router.post("/employee/{id}")
async def update_employee(id: int, data: dict):
    db = sessionLocal()
    rows = db.query(Employees).filter(Employees.employee_id == id).first()
    rows.first_name = data.get("first_name")
    rows.last_name = data.get("last_name")
    db.commit()
    db.refresh(rows)
    db.close()
    return rows


@router.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int):
    db = sessionLocal()
    row = (
        db.query(Employees)
        .filter(Employees.employee_id == employee_id, Employees.last_name.is_(None))
        .first()
    )
    if row is None:
        db.close()
        return {"message": "Employee not found or last_name is not NULL"}
    db.delete(row)
    db.commit()
    db.close()

    return {"message": "Deleted Successfully"}
