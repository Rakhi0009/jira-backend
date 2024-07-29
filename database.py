from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import POSTGRESQL_DATABASE_URL

engine = create_engine(POSTGRESQL_DATABASE_URL)
try:
    with engine.connect() as connection:
        print("Database connected!")
except Exception as e:
    print(f"Database connection failed: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


