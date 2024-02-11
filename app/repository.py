from app import db
import geopandas as gpd, fiona
from shapely.geometry import Point
import pyproj
from docx import Document

fiona.drvsupport.supported_drivers['kml'] = 'rw' 
fiona.drvsupport.supported_drivers['KML'] = 'rw' 
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'
fiona.drvsupport.supported_drivers['libkml'] = 'rw'
fiona.drvsupport.supported_drivers['GPKG'] = 'rw'


def transform_coordinates(lat, lon, from_epsg=4326, to_epsg=3765):
    transformer = pyproj.Transformer.from_crs(from_epsg, to_epsg, always_xy=True)
    x, y = transformer.transform(lon, lat)
    return x, y

def check_intersection(lat, lon):
    x, y = transform_coordinates(lat, lon)

    geo_file = "3_parcijalni_ispit\pop.shp"
    geo_file = "pop.shp"
    # Read the CSV file into a GeoDataFrame
    gdf = gpd.read_file(geo_file)
    gdf = gdf.set_crs(3765, allow_override=True)

    # Create a Point geometry for the given lat, lon
    point = Point(x, y)

    # Check for intersection
    intersection = gdf.geometry.contains(point)

    # If there is an intersection, extract information
    if intersection.any():
        intersected_data = gdf[intersection]
        sitecode = intersected_data["sitecode"].iloc[0]
        print(sitecode)
        return sitecode
    else:
        return None


def natura_impact_assessment(lat, lon, project_title, project_type):
#     bird_data = "birds.csv"
#     bird_data = query_points_within_polygon(lat, lon)
    text = f"""<p>{project_title} is situated at the location {lat}, {lon}.</p>
           <p> As a {project_type} development project, it is crucial to consider the potential environmental impacts.</p>
           <br> 
           <p> The project could have significant effects on the local ecosystem, including wildlife and bird populations. Some of the potential impacts are:
            
            1. **Habitat Destruction:** The development may lead to the destruction of natural habitats, affecting the local flora and fauna.
            
            2. **Disruption of Wildlife Migration:** If the project is located along migration routes, it could disrupt the natural migration patterns of birds and other animals.
            
            3. **Noise Pollution:** Construction activities can contribute to noise pollution, which may disturb bird species that rely on acoustic signals for communication and navigation.
            
            4. **Air and Water Pollution:** Depending on the nature of the project, there might be emissions and runoff that can contaminate the air and water, impacting both terrestrial and aquatic bird species.
            
            5. **Collision Risks:** Tall structures such as towers or wind turbines pose a collision risk for birds. It's essential to assess and mitigate these risks to protect bird populations.
            
            6. **Introduction of Invasive Species:** Construction activities may introduce invasive species that could outcompete or prey on local bird species.
            
            It's crucial to refer to available environmental impact assessments and conduct thorough studies to minimize negative consequences. The following bird species have been identified in the wider area of the project location based on available data in:

            [List of bird species and relevant data from the CSV file]

            Consideration of these factors is vital for sustainable development, ensuring that the project minimizes its ecological footprint and preserves biodiversity."""
            
    return text

def create_report(proj_name, text, output_path):
    # Create a new Word document
    doc = Document()

    # Add a title with the project name
    doc.add_heading(proj_name, level=1)

    # Add the text content to the document
    doc.add_paragraph(text)

    # Save the document to the specified output path
    doc.save(output_path)


if __name__ == "__main__":
    check_intersection(45.61, 15.70)