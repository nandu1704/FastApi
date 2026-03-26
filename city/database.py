from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# database_url = "postgresql://postgres:Teja%401704@localhost:5432/sakila"
database_url = "sqlite:///sakila"
engine = create_engine(database_url)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
