from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from decouple import config

# connecting db with sqlalchemy orm
DATABASE_URL = config("DATABASE_URL", cast=str, default=None)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


# dependency check
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
