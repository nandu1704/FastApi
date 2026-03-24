from database import Base
from sqlalchemy import Column, Integer, String


class Employees(Base):
    __tablename__ = "employees"
    employee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
