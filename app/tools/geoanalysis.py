import pyproj
from shapely.geometry import Point
from shapely.ops import transform
import geopandas as gpd

def create_point(lat, lon):
    """
    Create a Point object with the given latitude and longitude using shapely.
    Also transform point to wanted epsg.
    """
    point = Point(lon, lat)

    target_crs = pyproj.CRS.from_epsg(4326)
    source_crs = pyproj.CRS.from_epsg(4326)

    transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)
    transformed_point = transform(transformer.transform, point)

    return transformed_point

def get_geodataframe_for_point(lat, lon, table, session):
    # Define the query to retrieve data within 5 kilometers of the given point
    if table == 'pop':
        query = f"""
            SELECT ST_GeometryN(geom, generate_series(1, ST_NumGeometries(geom))) AS geom_polygon
            FROM data.{table}
            WHERE ST_DWithin(
                geom,
                ST_Transform(ST_SetSRID(ST_MakePoint({lon}, {lat}), 4326),3765),
                5000
            )
            LIMIT 1;
        """

        # Use geopandas to read the data from the database into a GeoDataFrame
        gdf = gpd.read_postgis(query, session.bind, geom_col='geom_polygon', crs = 3765)
        return gdf
    elif table == None:
        return

