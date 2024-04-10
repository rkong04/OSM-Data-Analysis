import sys
import os
from PIL import Image
from xml.dom.minidom import getDOMImplementation

#extract GPS coordinates from an image's EXIF data
def get_gps_coordinates(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()

        if not exif_data:
            print(f"No EXIF data found in {image_path}")
            return None

        gps_info = exif_data.get(34853)
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

#create a GPX file from a list of coordinates
def create_gpx_file(coordinates, filename="path_through_city.gpx"):
    impl = getDOMImplementation()
    doc = impl.createDocument(None, "gpx", None)
    root = doc.documentElement
    root.setAttribute("version", "1.1")
    root.setAttribute("creator", "Your Name")
    root.setAttribute("xmlns", "http://www.topografix.com/GPX/1/1")

    trk = doc.createElement("trk")
    root.appendChild(trk)
    
    trkseg = doc.createElement("trkseg")
    trk.appendChild(trkseg)

    for lat, lon in coordinates: #ORDER MATTERS HERE
        trkpt = doc.createElement("trkpt")
        trkpt.setAttribute("lat", str(lat))
        trkpt.setAttribute("lon", str(lon))
        trkseg.appendChild(trkpt)

    with open(filename, "w") as f:
        f.write(doc.toprettyxml(indent="  "))


#process all images in the given folder and extract coordinates
def process_folder(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    coordinates = []

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        gps_data = get_gps_coordinates(image_path)
        if gps_data:
            coordinates.append(gps_data)  #append coordinates as a tuple (lat, lon) THE ORDER MATTERS 

    return coordinates

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("failed; the cmd line input looks like this: python createPath.py folderName")
        sys.exit(1)

    folder_path = sys.argv[1]
    coordinates = process_folder(folder_path)

    if coordinates:
        create_gpx_file(coordinates)
        print(f"GPX file created with {len(coordinates)} points.")
    else:
        print("No geotagged images found or no images in folder.")
