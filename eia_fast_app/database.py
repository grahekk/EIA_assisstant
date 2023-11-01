from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.config import settings

DATABASE_URL = settings.database_url

Base = declarative_base()

class GeoSpatialData(Base):
    __tablename__ = "geospatial_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    geometry = Column(Geometry("GEOMETRY", srid=4326))

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
