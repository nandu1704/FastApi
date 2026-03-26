import json
from time import time
import greenstalk
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import City, CityModel, CityCreate
from database import get_db, Base, engine

router = APIRouter()

Base.metadata.create_all(bind=engine)

@router.get("/city")
async def get_city(db: Session = Depends(get_db)):
    cities = db.query(City).all()
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")
    return cities


@router.get("/city/{city_id}")
async def get_city_by_id(city_id: int, db: Session = Depends(get_db)):
    row = db.query(City).filter(City.city_id == city_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="City not found")
    return row


@router.post("/city", response_model=CityModel)
async def add_city(city: CityCreate, db: Session = Depends(get_db)):
    try:
        new_city = City(**city.model_dump())
        db.add(new_city)
        db.commit()
        db.refresh(new_city)

        client = greenstalk.Client(("127.0.0.1", 11300))
        job_data = {
            "to_email": "gopalnanda368@gmail.com",
            "subject": "City Created Successfully",
            "body": f"City '{new_city.city}' has been added successfully.",
        }
        client.put(json.dumps(job_data).encode("utf-8"))
        return new_city
    except Exception as e:
        db.rollback()
        raise e


@router.put("/city/{city_id}")
async def update_city(
    city_id: int, city_data: CityCreate, db: Session = Depends(get_db)
):
    updated_data = city_data.model_dump()
    if not updated_data:
        raise HTTPException(status_code=404, detail="City not found")
    db.query(City).filter(City.city_id == city_id).update(updated_data)
    db.commit()
    return updated_data


@router.delete("/city/{city_id}")
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    db.query(City).filter(City.city_id == city_id).delete()
    db.commit()
    return {"message": "Deleted Successfully"}
