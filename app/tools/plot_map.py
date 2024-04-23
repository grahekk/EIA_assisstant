import io
import folium
from folium import plugins, elements
from PIL import Image
import tempfile
from shapely.geometry import box


def export_map_with_shapefile(lat, lon, zoom=15, basemap='OpenStreetMap', file_path='map_image.jpg', gdf=None):
    """
    Generate and export a map image centered at the specified latitude and longitude.

    Parameters:
    - lat (float): Latitude of the center of the map.
    - lon (float): Longitude of the center of the map.
    - zoom (int, optional): Zoom level of the map (default is 15).
    - basemap (str, optional): Basemap layer for the map. Options include:
      'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor',
      'CartoDB positron', 'CartoDB dark_matter', and more (default is 'OpenStreetMap').
    - file_path (str, optional): File path to save the exported JPEG image (default is 'map_image.jpg').

    Returns:
    None

    Example:
    >>> export_map_image(37.7749, -122.4194, zoom=15, basemap='Stamen Terrain', file_path='san_francisco_map.jpg')

    Note:
    - Ensure that the necessary libraries ('folium', 'selenium', 'PIL') are installed.
    - A web driver for Selenium is required; download it from https://sites.google.com/chromium.org/driver/.
    """
    # Create a folium map centered at the given latitude and longitude
    map_center = [lat, lon]
    my_map = folium.Map(location=map_center, control_scale=True, tiles=basemap)

    # Add a marker at the specified location
    folium.Marker(location=map_center, popup=f'({lat}, {lon})').add_to(my_map)
    if not gdf.empty:
        folium.GeoJson(gdf).add_to(my_map)
        gdf_bounds = gdf.total_bounds
        gdf_box = box(gdf_bounds[0], gdf_bounds[1], gdf_bounds[2], gdf_bounds[3])

        # Center the map and set zoom to fit the extent of the shapefile
        my_map.fit_bounds(gdf_box.bounds, max_zoom=18)

    else:
        print("Folium map gdf is empty!")

    # Save the map as an HTML file
    with tempfile.TemporaryDirectory() as tmp:
        html_path = f"temp_map.html"
        my_map.save(html_path)

        # Use selenium to take a screenshot of the HTML map
        img_data = my_map._to_png(1)

        # Use PIL to crop the screenshot and save it as a JPEG
        with Image.open(io.BytesIO(img_data)) as im:
        # im = Image.open(io.BytesIO(img_data))
            cut_left = 1.2
            cut_pixels = int(cut_left * 37.8)  # Convert centimeters to pixels (Assuming 96 DPI)
            im = im.crop((cut_pixels, 0, im.width, im.height - 10)) # Crop the left side and bottom scale
            rgb_im = im.convert('RGB')
            rgb_im.save(file_path, 'JPEG')


# Example usage
# export_map_image(45.80, 16.00, zoom=15, file_path='map_image.jpg')
