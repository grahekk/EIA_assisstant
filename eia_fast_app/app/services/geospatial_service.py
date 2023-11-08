from geoalchemy2 import WKBElement
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
from shapely import to_wkt
from shapely import wkt
import geopandas as gpd
import fiona
from pyproj import CRS, Transformer
from sqlalchemy import Function, func

fiona.drvsupport.supported_drivers['libkml'] = 'rw' # enable KML support which is disabled by default
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

from app.database.database import SessionLocal, natura_habitats, natura_birds, Base
from app.models.models import GeoSpatialData

transformer = Transformer.from_crs("EPSG:4326", "EPSG:3765")
# func = Function()

class GeoSpatialService:
    def create_geospatial_data(self, name: str, file: str):
        db = SessionLocal()
        crs = 4326
        gdf = gpd.read_file(file)
        gdf.to_crs = f"EPSG.{crs}"
        geometry = gdf.to_wkt()['geometry'].values[0]
        # geometry = transformer.transform(geometry)
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
        # return_data = db.query(natura_habitats).filter(natura_habitats.geom.intersects(data.geom)).first()

        # return_data = db.query(natura_habitats)
        return_data = db.query(natura_habitats.c.sitename).filter(natura_habitats.c.geom.intersects(func.ST_transform(data.geom, 3765))).all()
        # return_data = db.query(natura_habitats).filter(natura_habitats.geom.intersects(func.ST_transform(data.geom, 3765))).first()
        # return_data = db.query(NaturaHabitats).filter(NaturaHabitats.geom.intersects(func.ST_transform(data.geom, 4326))).first()
        # print(db.query(func.ST_transform(data.geom, 4326)).first())
        # print(db.query(func.ST_transform(data.geom, 3765)).first())
        print(return_data)
        db.close()
        return return_data