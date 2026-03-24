from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

database_url = "postgresql://postgres:Teja%401704@localhost:5432/sakila"
engine = create_engine(database_url)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
