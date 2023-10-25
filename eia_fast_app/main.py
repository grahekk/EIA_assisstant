from fastapi import FastAPI, File, UploadFile
from shapely.geometry import shape
from pydantic import BaseModel

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
    
    # Now you can work with the SHP file using libraries like geopandas and shapely.
    
    # Example: Reading shapefile and extracting some data
    # import geopandas as gpd
    # data = gpd.read_file(file.filename)
    # feature = data.iloc[0]  # Get the first feature
    # geometry_type = shape(feature['geometry']).geom_type

    # return {"name": file.filename, "geometry_type": geometry_type}