from app.database import SessionLocal
from app.models.models import GeoSpatialData

class GeoSpatialService:
    def create_geospatial_data(self, name: str, geometry: str):
        db = SessionLocal()
        data = GeoSpatialData(name=name, geometry=geometry)
        db.add(data)
        db.commit()
        db.close()
        return data

    def get_geospatial_data(self, id: int):
        db = SessionLocal()
        data = db.query(GeoSpatialData).filter(GeoSpatialData.id == id).first()
        db.close()
        return data
