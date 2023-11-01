from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GeoSpatialData(Base):
    __tablename__ = "input_geospatial_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    crs = 3765
    geometry = Column(Geometry(srid=crs))
