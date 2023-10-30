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
    import geopandas as gpd
    import fiona
    import zipfile
    import StringIO
    import shapefile
    
    fiona.drvsupport.supported_drivers['kml'] = 'rw' # enable KML support which is disabled by default
    fiona.drvsupport.supported_drivers['KML'] = 'rw' # enable KML support which is disabled by default


    zipshape = zipfile.ZipFile(open(r'C:\GIS\Temp\RoadsShapefileFolder.zip', 'rb'))
    print(zipshape.namelist())
    dbfname, _, shpname, _, shxname = zipshape.namelist()
    r = shapefile.Reader(shp=StringIO.StringIO(zipshape.read(shpname)),
                        shx=StringIO.StringIO(zipshape.read(shxname)),
                        dbf=StringIO.StringIO(zipshape.read(dbfname)))

    print(r.bbox)
    print(r.numRecords)

    data = gpd.read_file(file.filename)
    feature = data.iloc[0]  # Get the first feature
    geometry_type = shape(feature['geometry']).geom_type

    return {"name": file.filename, "geometry_type": geometry_type}