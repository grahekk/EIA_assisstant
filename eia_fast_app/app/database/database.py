from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, MetaData, Table
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config.config import database_url
from app.models.models import GeoSpatialData, Base

DATABASE_URL = database_url
engine = create_engine(DATABASE_URL)
metadata_obj = MetaData(schema="data")

natura_habitats = Table("povs", 
                        metadata_obj,
                        Column("geom", Geometry('POLYGON')),
                        autoload_with = engine)

natura_birds = Table("pop", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
