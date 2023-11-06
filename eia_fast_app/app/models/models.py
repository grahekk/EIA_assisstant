from sqlalchemy import Column, Integer, String, MetaData, Table
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base

metadata_obj = MetaData(schema="data")
Base = declarative_base()

class GeoSpatialData(Base):
    __tablename__ = "input_geospatial_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    crs = 4326
    # geometry_type: str
    geom = Column(Geometry(srid=crs))
    # geom = Column(Geometry())

class NaturaHabitats(Base):
    __tablename__ = 'povs'
    schema = "data"
    id = Column("ogc_fid", Integer, primary_key=True)
    site_code = Column("sitecode",String)
    site_name = Column("sitename",String)
    geom = Column(Geometry('POLYGON'))

class NaturaBirds(Base):
    __tablename__ = 'pop'
    schema = "data"
    id = Column("ogc_fid", Integer, primary_key=True)
    site_code = Column("sitecode",String)
    site_name = Column("sitename",String)
    geom = Column(Geometry('POLYGON'))

# natura_habitats = Table(
#     "povs",
#     metadata_obj,
#     Column("ogc_fid", Integer, primary_key=True),
#     Column("sitecode",String),
#     Column("sitename",String),
#     Column(Geometry('POLYGON')),
#     schema="data"
# )

# natura_birds = Table(
#     "pop",
#     metadata_obj,
#     Column("ogc_fid", Integer, primary_key=True),
#     Column("sitecode",String),
#     Column("sitename",String),
#     Column(Geometry('POLYGON')),
#     schema="data"
# )