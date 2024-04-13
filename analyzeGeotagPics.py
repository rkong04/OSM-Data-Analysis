import sys
import os
import math
from PIL import Image
from xml.dom.minidom import getDOMImplementation
import requests
import gpxpy
import gpxpy.gpx
import polyline
import webbrowser
import folium
#import osmnx as ox
#import networkx as nx
#import geopandas as gpd

#my personal key
API_KEY = 'AIzaSyAVwJM_meiBw7Qr3TxOgAY5LmOoB8xKUdU'

def get_gps_coordinates(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if not exif_data:
            print(f"No EXIF data found in {image_path}")
            return None
        gps_info = exif_data.get(34853) #this number represents gpsinfo in EXIF data so it's kind of like an ID
        if not gps_info:
            print(f"No GPS data found in {image_path}")
            return None
        def convert_to_degrees(value):
            d, m, s = value
            return d + (m / 60.0) + (s / 3600.0)
        lat = convert_to_degrees(gps_info[2]) if gps_info[1] == 'N' else -convert_to_degrees(gps_info[2])
        lon = convert_to_degrees(gps_info[4]) if gps_info[3] == 'E' else -convert_to_degrees(gps_info[4])
        return lat, lon
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance * 1000

#makes points along a STRAIGHT PATH from point to point, does not follow the "realistic" path
def interpolate_points(p1, p2, interval=1000): #in meters btw
    points = []
    distance = haversine(p1[0], p1[1], p2[0], p2[1])
    num_points = int(distance // interval)
    lat_step = (p2[0] - p1[0]) / (num_points + 1)
    lon_step = (p2[1] - p1[1]) / (num_points + 1)
    for i in range(1, num_points + 1):
        lat = p1[0] + lat_step * i
        lon = p1[1] + lon_step * i
        points.append((lat, lon))
    return points

def fetch_place_details(place_id):
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'user_ratings_total',
        'key': API_KEY
    }
    response = requests.get(details_url, params=params)
    return response.json()

"""def find_nearby_attractions(latitude, longitude):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f'{latitude},{longitude}',
        'radius': 1000,
        'keyword': 'point of interest|historical site|tourist attraction',
        'key': API_KEY
    }
    res = requests.get(endpoint_url, params=params)
    results = res.json()
    attractions = []
    if 'results' in results:
        for place in results['results']:
            if place['name'] not in attractions:
                attractions.append(place['name'])
    return attractions"""

def find_nearby_attractions(latitude, longitude):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f'{latitude},{longitude}',
        'radius': 1000,
        'keyword': 'point of interest|historical site|tourist attraction',
        'key': API_KEY
    }
    res = requests.get(endpoint_url, params=params)
    results = res.json()
    attractions = []
    min_reviews = 50
    if 'results' in results:
        for place in results['results']:
            details = fetch_place_details(place['place_id'])
            if details.get('result', {}).get('user_ratings_total', 0) >= min_reviews:
                if place['name'] not in attractions:
                    attractions.append(place['name'])
    return attractions

def process_images_and_find_attractions(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    attractions_data = {}
    coordinates = []
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        gps_data = get_gps_coordinates(image_path)
        if gps_data:
            coordinates.append((gps_data, image_path))

    for i in range(len(coordinates) - 1):
        start, end = coordinates[i], coordinates[i+1]
        start_attractions = find_nearby_attractions(*start[0])
        attractions_data[f"At {start[1]}:"] = start_attractions
        path_attractions = set()

        all_points = interpolate_points(start[0], end[0])
        for point in all_points:
            path_attractions.update(find_nearby_attractions(*point))

        path_key = f"Path from {start[1]} to {end[1]}"
        attractions_data[path_key] = list(path_attractions)

        if i == len(coordinates) - 2:
            end_attractions = find_nearby_attractions(*end[0])
            attractions_data[f"At {end[1]}:"] = end_attractions

    return attractions_data

def create_gpx_file(coordinates, filename="straightPath.gpx"):
    impl = getDOMImplementation()
    doc = impl.createDocument(None, "gpx", None)
    root = doc.documentElement
    root.setAttribute("version", "1.1")
    root.setAttribute("creator", "Chun Lai")
    root.setAttribute("xmlns", "http://www.topografix.com/GPX/1/1")

    trk = doc.createElement("trk")
    root.appendChild(trk)
    
    trkseg = doc.createElement("trkseg")
    trk.appendChild(trkseg)

    for lat, lon in coordinates: #ORDER MATTERS BTW
        trkpt = doc.createElement("trkpt")
        trkpt.setAttribute("lat", str(lat))
        trkpt.setAttribute("lon", str(lon))
        trkseg.appendChild(trkpt)

    with open(filename, "w") as f:
        f.write(doc.toprettyxml(indent="  "))
    display_gpx_on_map('straightPath.gpx')

def create_gpx(coordinates):
    gpx = gpxpy.gpx.GPX()

    for i in range(len(coordinates) - 1):
        start = coordinates[i]
        end = coordinates[i + 1]

        response = requests.get(
            'https://maps.googleapis.com/maps/api/directions/json?',
            params={
                'origin': f'{start[0]},{start[1]}',
                'destination': f'{end[0]},{end[1]}',
                'key': API_KEY
            }
        )
        data = response.json()
        points = data['routes'][0]['overview_polyline']['points']

        decoded = polyline.decode(points)

        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        for lat, lon in decoded:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=0))

    with open('optimizedPath.gpx', 'w') as file:
        file.write(gpx.to_xml())
    display_gpx_on_map('optimizedPath.gpx')

    

def process_folder(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    coordinates = []

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        gps_data = get_gps_coordinates(image_path)
        if gps_data:
            coordinates.append(gps_data)

    return coordinates

def accumulate_and_print_unique_attractions(attractions_dict):
    all_attractions = set()
    for location, nearby_attractions in attractions_dict.items():
        all_attractions.update(nearby_attractions)
    print('Overall, you were nearby or should have passed:', all_attractions)

def save_unique_attractions_to_file(attractions, filename='unique_attractions.txt'):
    all_attractions = set()
    for nearby_attractions in attractions.values(): 
        all_attractions.update(nearby_attractions)
    
    with open(filename, 'w') as file:
        for attraction in sorted(all_attractions):
            file.write(f"{attraction}\n")

def display_gpx_on_map(gpx_path):
    with open(gpx_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    start_lat = gpx.tracks[0].segments[0].points[0].latitude
    start_lon = gpx.tracks[0].segments[0].points[0].longitude

    my_map = folium.Map(location=[start_lat, start_lon], zoom_start=14)

    for track in gpx.tracks:
        for segment in track.segments:
            points = [(point.latitude, point.longitude) for point in segment.points]
            folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(my_map)

    my_map.save('gpx_display_map.html')

    
    webbrowser.open('gpx_display_map.html', new=2)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Failed input, please try: python analyzeGeotagPics.py folderName")
        sys.exit(1)
    folder_path = sys.argv[1]
    attractions = process_images_and_find_attractions(folder_path)
    save_unique_attractions_to_file(attractions)
    coordinates = process_folder(folder_path)

    for location, nearby_attractions in attractions.items():
        print(f"{location} {nearby_attractions} \n")

    accumulate_and_print_unique_attractions(attractions)
    print("\n")

    if coordinates:
        create_gpx_file(coordinates)
        create_gpx(coordinates)
        print(f"2 GPX files created using {len(coordinates)} input coordinates.")
    else:
        print("No geotagged images found or no images in folder.")

    
