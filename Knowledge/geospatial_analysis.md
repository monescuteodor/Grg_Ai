Geospatial Analysis & Remote Sensing Complete Reference
CHAPTER 1: GETTING STARTED WITH GEOSPATIAL ANALYSIS
Remarks
Geospatial analysis involves the collection, display, and manipulation of imagery, GPS, survey photography, and GIS data. Remote sensing is the acquisition of information about an object or phenomenon without making physical contact, typically via satellites or aircraft. Key concepts: Coordinate Reference Systems (CRS), Projections, Raster vs. Vector data, Spectral Indices, Image Classification. Applications: Urban planning, agriculture, disaster management, environmental monitoring, navigation.
Tools: Python (GeoPandas, Rasterio, Shapely, Folium), QGIS (desktop GIS), GDAL (data translation), Sentinel Hub, Google Earth Engine.
Hello Geospatial
# hello_geo.py
"""
First geospatial program: Calculate distance between two points using Haversine formula.
"""
import math

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on Earth."""
    R = 6371  # Earth's radius in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat/2)**2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)
    
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

# Coordinates: Bucharest, Romania to Paris, France
bucharest = (44.4268, 26.1025)
paris = (48.8566, 2.3522)

dist_km = haversine(*bucharest, *paris)
print(f"Distance: {dist_km:.2f} km")

Coordinate Reference Systems (CRS)
# Geographic CRS: Uses latitude/longitude (e.g., WGS84 / EPSG:4326).
# Projected CRS: Uses linear units (meters/feet) on a flat surface (e.g., UTM, Web Mercator / EPSG:3857).
# Reprojection: Converting data from one CRS to another.

import geopandas as gpd
from shapely.geometry import Point

# Create a GeoDataFrame with WGS84 coordinates
gdf = gpd.GeoDataFrame(
    {'city': ['Bucharest', 'Paris']},
    geometry=[Point(26.1025, 44.4268), Point(2.3522, 48.8566)],
    crs="EPSG:4326"  # WGS84
)

# Reproject to Web Mercator (used by most web maps)
gdf_mercator = gdf.to_crs("EPSG:3857")
print(gdf_mercator.crs)

CHAPTER 2: VECTOR DATA ANALYSIS
Working with Shapefiles and GeoJSON
# Vector data represents features as points, lines, and polygons.
# Formats: Shapefile (.shp), GeoJSON, KML, GPKG.

import geopandas as gpd
import matplotlib.pyplot as plt

# Load a sample dataset (world borders)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Filter for Europe
europe = world[world['continent'] == 'Europe']

# Plot
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
europe.plot(ax=ax, color='lightblue', edgecolor='black')
plt.title("Europe Map")
plt.show()

Spatial Operations
# Buffer: Create a zone around a feature.
# Intersection: Find overlapping areas.
# Union: Combine geometries.
# Distance: Calculate distance between features.

from shapely.geometry import Polygon, Point

# Create two polygons
poly1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
poly2 = Polygon([(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)])

# Intersection
intersection = poly1.intersection(poly2)
print(f"Intersection Area: {intersection.area}")

# Buffer
point = Point(0, 0)
buffered = point.buffer(1.0)  # 1 unit radius
print(f"Buffered Area: {buffered.area}")

Spatial Joins
# Join attributes from one layer to another based on spatial relationship.

# Example: Count points within polygons
points = gpd.GeoDataFrame(
    {'id': [1, 2, 3]},
    geometry=[Point(0.5, 0.5), Point(1.0, 1.0), Point(5, 5)],
    crs="EPSG:4326"
)

polygons = gpd.GeoDataFrame(
    {'name': ['A', 'B']},
    geometry=[Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]), Polygon([(4, 4), (6, 4), (6, 6), (4, 6)])],
    crs="EPSG:4326"
)

result = gpd.sjoin(points, polygons, predicate='within')
print(result)

CHAPTER 3: RASTER DATA ANALYSIS
Working with Satellite Imagery
# Raster data is a grid of pixels (cells), each with a value.
# Formats: GeoTIFF, NetCDF, HDF5.
# Libraries: Rasterio, Xarray.

import rasterio
import numpy as np

# Open a raster file
# src = rasterio.open('image.tif')
# band1 = src.read(1)

# For demo, create a dummy raster
data = np.random.rand(100, 100)
transform = rasterio.transform.from_bounds(0, 0, 10, 10, 100, 100)

with rasterio.open(
    'dummy.tif', 'w',
    driver='GTiff',
    height=100,
    width=100,
    count=1,
    dtype=data.dtype,
    crs='EPSG:4326',
    transform=transform
) as dst:
    dst.write(data, 1)

print("Dummy raster created.")

Spectral Indices
# NDVI (Normalized Difference Vegetation Index): Measures vegetation health.
# NDVI = (NIR - Red) / (NIR + Red)
# Values range from -1 to 1. Higher values indicate healthier vegetation.

def calculate_ndvi(nir_band, red_band):
    """Calculate NDVI from two bands."""
    nir = nir_band.astype(float)
    red = red_band.astype(float)
    
    # Avoid division by zero
    denominator = nir + red
    denominator[denominator == 0] = 1e-6
    
    ndvi = (nir - red) / denominator
    return ndvi

# Example usage with dummy data
nir = np.random.rand(10, 10) * 0.5 + 0.5  # High reflectance
red = np.random.rand(10, 10) * 0.2        # Low reflectance
ndvi = calculate_ndvi(nir, red)
print(f"Mean NDVI: {np.mean(ndvi):.3f}")

Image Classification
# Supervised Classification: Train a model on labeled pixels.
# Unsupervised Classification: Cluster pixels based on spectral similarity (e.g., K-Means).

from sklearn.cluster import KMeans

# Flatten image for clustering
image_3d = np.random.rand(100, 100, 3)  # RGB image
pixels = image_3d.reshape(-1, 3)

# K-Means clustering
kmeans = KMeans(n_clusters=5, random_state=42)
labels = kmeans.fit_predict(pixels)

# Reshape back to image dimensions
classified_image = labels.reshape(100, 100)
print(f"Classified into {len(np.unique(labels))} classes.")

CHAPTER 4: REMOTE SENSING PLATFORMS
Sentinel and Landsat Data
# Sentinel-2: High-resolution optical imagery (10m-60m). Free access via Copernicus Open Access Hub.
# Landsat 8/9: Medium-resolution optical imagery (30m). Long historical record.
# MODIS: Low-resolution, high-frequency global coverage.

# Accessing data programmatically
# import sentinelsat
# api = sentinelsat.SentinelAPI('user', 'password', 'https://scihub.copernicus.eu/dhus')
# products = api.query(area='POLYGON(...)', date=('NOW-1MONTH', 'NOW'), producttype='S2MSI1C')

Google Earth Engine (GEE)
# Cloud-based platform for planetary-scale geospatial analysis.
# Allows processing of petabytes of satellite imagery.

# Python API example (conceptual)
# import ee
# ee.Initialize()
# image = ee.Image('COPERNICUS/S2_SR/20230101T000000_20230101T000000_T10SGD')
# ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

LiDAR Data Processing
# Light Detection and Ranging: Uses laser pulses to measure distances.
# Produces dense 3D point clouds.
# Applications: Digital Elevation Models (DEMs), forestry, urban modeling.

import laspy

# Read a LAS file
# las = laspy.read('file.las')
# x = las.x
# y = las.y
# z = las.z
# classification = las.classification

# Filter ground points
# ground_points = las.points[las.classification == 2]

CHAPTER 5: WEB MAPPING AND VISUALIZATION
Interactive Maps with Folium
# Create interactive Leaflet maps in Python.

import folium

# Create a map centered on Bucharest
m = folium.Map(location=[44.4268, 26.1025], zoom_start=12)

# Add a marker
folium.Marker(
    [44.4268, 26.1025],
    popup="Bucharest",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# Save to HTML
# m.save("map.html")
print("Map created.")

Choropleth Maps
# Thematic maps where areas are shaded based on a statistical variable.

# Example: Population density by country
# choropleth = folium.Choropleth(
#     geo_data=world_json,
#     name='choropleth',
#     data=df,
#     columns=['country', 'density'],
#     key_on='feature.properties.name',
#     fill_color='YlOrRd',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Population Density'
# ).add_to(m)

Tile Servers and WMS
# Web Map Service (WMS): Standard for serving map images.
# Tile Map Service (TMS): Pre-rendered tiles for fast loading.
# Sources: OpenStreetMap, Stamen, CartoDB.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Machine Learning for Geospatial Data
# Object Detection: Identify buildings, cars, ships in satellite imagery.
# Change Detection: Monitor deforestation, urban expansion over time.
# Super-Resolution: Enhance image resolution using deep learning.

Geostatistics
# Kriging: Interpolation method that accounts for spatial autocorrelation.
# Variogram: Measure of spatial dependence.

Big Data Geospatial
# Apache Sedona: Spatial extension for Spark.
# Dask-GeoPandas: Parallel GeoPandas operations.

Recommended Reading
# - "Geographic Information Systems and Science" by Longley et al.
# - "Python Geospatial Development Essentials" by Erik Westra
# - QGIS Documentation: https://docs.qgis.org/
# - GeoPandas Documentation: https://geopandas.org/
# - Rasterio Documentation: https://rasterio.readthedocs.io/

# End of Geospatial Analysis Reference