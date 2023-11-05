from geoalchemy2 import WKBElement
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
from shapely import to_wkt
from shapely import wkt
import geopandas as gpd
import fiona
fiona.drvsupport.supported_drivers['libkml'] = 'rw' # enable KML support which is disabled by default
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'



from app.database.database import SessionLocal
from app.models.models import GeoSpatialData, NaturaHabitats

class GeoSpatialService:
    def create_geospatial_data(self, name: str, file: str):
        db = SessionLocal()
        crs = 3765
        gdf = gpd.read_file(file)
        gdf.to_crs = f"EPSG.{crs}"
        geometry = gdf.to_wkt()['geometry'].values[0]
        data = GeoSpatialData(name=name, geom=geometry)
        db.add(data)
        db.commit()
        data_id = data.id
        db.close()
        return data_id

    def get_geospatial_data(self, id: int):
        db = SessionLocal()
        data = db.query(GeoSpatialData).filter(GeoSpatialData.id == id).first()
        db.close()
        return data

    def get_overlapping(self, id, layer):
        db = SessionLocal()
        data = db.query(GeoSpatialData).filter(GeoSpatialData.id == id).first()
        return_data = db.query(NaturaHabitats).filter(NaturaHabitats.geom.intersects(data.geom)).first()
        print(return_data)
        db.close()
        return return_data