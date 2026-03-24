from database import Base
from sqlalchemy import Column, Integer, VARCHAR
from pydantic import BaseModel


class City(Base):
    __tablename__ = "city"
    city_id = Column(Integer, primary_key=True, index=True)
    city = Column(VARCHAR(50), nullable=False)
    country_id = Column(Integer, nullable=False, default=1)


class CityCreate(BaseModel):
    city_id: int
    city: str
    country_id: int


class CityModel(BaseModel):
    city_id: int
    city: str
    country_id: int
