from fastapi import FastAPI, File, UploadFile
from shapely.geometry import shape
from pydantic import BaseModel
# from app.models.file import GeoJSONData
from starlette.responses import JSONResponse
import geopandas as gpd
import tempfile
import os


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


# Define a temporary directory to store uploaded files
temp_dir = tempfile.TemporaryDirectory()

@app.post("/upload-geo-file/")
async def upload_geo_file(file: UploadFile):
    # Ensure that the uploaded file is a valid geospatial format (GeoJSON, GPKG, or SHP)
    valid_extensions = {'.json', '.geojson', '.gpkg', '.shp'}
    ext = os.path.splitext(file.filename)[1]
    if ext not in valid_extensions:
        return JSONResponse(content={"error": "Invalid file format"}, status_code=400)

    # Save the uploaded file to the temporary directory
    file_path = os.path.join(temp_dir.name, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Read the uploaded geospatial file using GeoPandas
    try:
        gdf = gpd.read_file(file_path)
        # Perform any geospatial operations you need on the `gdf` here
        # For example, you can access the geometries using gdf.geometry

        return JSONResponse(content={"message": "File uploaded and processed successfully"})
    except Exception as e:
        return JSONResponse(content={"error": f"Error processing geospatial data: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)