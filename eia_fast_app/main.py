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
    # from io import StringIO
    # import shapefile
    
    fiona.drvsupport.supported_drivers['kml'] = 'rw' # enable KML support which is disabled by default
    fiona.drvsupport.supported_drivers['KML'] = 'rw' # enable KML support which is disabled by default


    # zipshape = zipfile.ZipFile(open(file.filename, 'rb'))
    # print(zipshape.namelist())
    # dbfname, _, shpname, _, shxname = zipshape.namelist()
    # r = shapefile.Reader(shp=StringIO.StringIO(zipshape.read(shpname)),
    #                     shx=StringIO.StringIO(zipshape.read(shxname)),
    #                     dbf=StringIO.StringIO(zipshape.read(dbfname)))

    # print(r.bbox)
    # print(r.numRecords)

    data = gpd.read_file(file.filename)
    feature = data.iloc[0]  # Get the first feature
    geometry_type = shape(feature['geometry']).geom_type

    return {"name": file.filename, "geometry_type": geometry_type} #response body json

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Binary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

app = FastAPI()

# Step 1: Define a Pydantic model for file validation
class GeoPackageUpload(BaseModel):
    file: UploadFile

# Step 2: Create a SQLAlchemy model for the database table
DATABASE_URL = "sqlite:///./test.db"
Base = declarative_base()

class GeoPackage(Base):
    __tablename__ = "geopackages"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    content = Column(Binary)

# Initialize the database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Step 3: Use Pydantic models for request validation and response serialization
@app.post("/upload/")
async def upload_gpkg(gpkg: GeoPackageUpload):
    file = gpkg.file
    if file.content_type != "application/octet-stream":
        return {"error": "Only GeoPackage files (.gpkg) are allowed."}

    # Read the file content
    file_content = file.file.read()

    # Step 4: Perform database operations using SQLAlchemy
    try:
        db = SessionLocal()
        db.add(GeoPackage(filename=file.filename, content=file_content))
        db.commit()
        db.close()
    except IntegrityError:
        return {"error": "File with the same name already exists in the database."}

    return {"filename": file.filename, "content_type": file.content_type}
