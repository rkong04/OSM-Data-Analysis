# CMPT353-Project
# 1. Defining the Problem


Part B: Pictures and Geodata
When traveling through the city, there could be a lot of attractions or sites  that you miss since you did not see them or they were nearby unbeknownst to you. You also probably do not remember exactly what streets you were walking and only have some pictures to remember the  trip. It would be nice if you could see all the stuff you might have missed or were supposed to see and how you might have traveled from picture to picture.

# 2. Instructions
pip3 install fuzzywuzzy

Part B: Pictures and Geodata 

Most imported libraries are standard Python libraries, but not all. Some need to be installed.

- pip install Requests
- pip install gpxpy
- pip install polyline
- pip install folium
- pip install pillow

The program itself is all contained in analyzeGeotagPics.py

example cmd line:

python analyzeGeotagPics.py geotaggedEx

python analyzeGeotagPics.py any_folder_name


# 3. Data

Part B: Pictures and Geodata

There is a provided folder of arbitrary example pictures with geotags, but the idea is that you can use any pictures you want if they are geotagged. Only png, jpg, and jpeg files accepted. For this project, geoimgr.com was used to artificially geotag pictures, but in theory, a user should have photos that are already geotagged on their phone hopefully. 

The program takes a folder of pictures,  even if it is just one picture,  so you can have multiple folders of pictures for your own organization in the same directory as the Python file, but you can only run one folder.

The folder input also technically takes a path, but for your own sanity and the program's effectiveness, just keep all picture folders in the same directory as the Python file.

# 4. Output

Part B: Pictures and Geodata
- straightPath.gpx, the gpx file, draws a straight line from point to point
- optimizedPath.gpx, uses Directions API to form a realistic street route
- gpx_display_map.html, runs once for each of the above GPXs to display the GPX in web format, but for tech savvy people you should probably just use a GPX viewer to colour the routes
- unique_attractions.txt, simple list of the attractions passed on the trip
- cmd terminal print outputs, says in detail where exactly among the trip the attractions were detected (e.g. Path A -> B contained [1, 2] and Point C had [3, 4])
