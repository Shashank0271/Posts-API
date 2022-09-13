from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.user_name}:{settings.password}@{settings.host_name}:{settings.port_number}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    # everytime we get a request , we create a session
    # we execute the sql statements for that session , after which session is closed
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()