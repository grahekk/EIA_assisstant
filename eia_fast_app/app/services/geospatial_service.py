from geoalchemy2 import WKBElement
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
from shapely import to_wkt
from shapely import wkt
import geopandas as gpd

from app.database.database import SessionLocal
from app.models.models import GeoSpatialData

class GeoSpatialService:
    def create_geospatial_data(self, name: str, file: str):
        db = SessionLocal()
        # geometry = to_wkt(geometry)
        gdf = gpd.read_file(file)
        # data = gdf.to_postgis(name="input_geospatial_data", con=db.bind, if_exists="append", index = True)

        # geometry = shape(gdf)
        # geometry = from_shape(geometry) # TODO: put ewkt
        # print("this is geometry from service ", geometry)
        # geometry = gdf.to_wkt()

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
