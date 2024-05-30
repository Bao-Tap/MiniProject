from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from sqlalchemy.pool import QueuePool

engine = create_engine(DATABASE_URI, pool_recycle=3600,poolclass=QueuePool, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
