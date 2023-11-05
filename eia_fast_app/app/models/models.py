from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GeoSpatialData(Base):
    __tablename__ = "input_geospatial_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # crs = 4326
    # geometry_type: str
    # geom = Column(Geometry(srid=crs))
    geom = Column(Geometry())

class NaturaHabitats(Base):
    __tablename__ = 'data.povs'
    id = Column("ogc_fid", Integer, primary_key=True)
    site_code = Column("sitecode",String)
    site_name = Column("sitename",String)
    geom = Column(Geometry('POLYGON'))

class NaturaBirds(Base):
    __tablename__ = 'data.pop'
    id = Column("ogc_fid", Integer, primary_key=True)
    site_code = Column("sitecode",String)
    site_name = Column("sitename",String)
    geom = Column(Geometry('POLYGON'))