from fastapi import FastAPI, File, UploadFile
from shapely.geometry import shape
from pydantic import BaseModel
from app.models.file import GeoJSONData

app = FastAPI()

@app.get("/")
def read_root():
    return "Welcome to the eia assistant API :)"

class ShapefileData(BaseModel):
    name: str
    geometry_type: str


@app.post("/upload_shapefile/")
async def upload_shapefile(file: UploadFile):
    if file.content_type != "application/octet-stream":
        return {"error": "Invalid file format. Please upload a shapefile (SHP)."}
    
    with open(file.filename, 'wb') as shp_file:
        shp_file.write(file.file.read())
        
    import geopandas as gpd

    data = gpd.read_file(file.filename)
    feature = data.iloc[0]  # Get the first feature
    geometry_type = shape(feature['geometry']).geom_type

    return {"name": file.filename, "geometry_type": geometry_type} #response body json


@app.post("/upload-geojson/")
# async def upload_geojson(file: UploadFile, geojson_data: GeoJSONData):
async def upload_geojson(file: UploadFile):
    # Check the uploaded .geojson data against the GeoJSONData model
    # if not geojson_data:
    #     return {"error": "Invalid .geojson data."}

    # If the .geojson data is valid, you can access it using geojson_data
    # features = geojson_data.features

    # Your file-saving and processing logic here
    # ...

    return {"message": "GeoJSON file uploaded successfully."}