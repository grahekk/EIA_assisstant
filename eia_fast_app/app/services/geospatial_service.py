from geoalchemy2 import WKBElement
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
import geopandas as gpd

from app.database.database import SessionLocal
from app.models.models import GeoSpatialData

class GeoSpatialService:
    def create_geospatial_data(self, name: str, geometry: str):
        db = SessionLocal()
        geometry = from_shape(shape(geometry)) # put ewkt
        print("this is geometry from service ",geometry)
        data = GeoSpatialData(name=name, geom=geometry)
        db.add(data)
        db.commit()
        db.close()
        return data

    def get_geospatial_data(self, id: int):
        db = SessionLocal()
        data = db.query(GeoSpatialData).filter(GeoSpatialData.id == id).first()
        db.close()
        return data
