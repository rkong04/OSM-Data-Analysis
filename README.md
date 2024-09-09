# 1. Defining the Problem
Part A: Restaurants

Vancouver has a lot of restaurant options available wherever you are.There are staple chains known across the world but also restaurants home to only Vancouver. The goal is to analyze restaurant data using various clustering and regression models to visualize the statistics and densities of restaurants across Vancouver. 

Part B: Pictures and Geodata

When traveling through the city, there could be a lot of attractions or sites  that you miss since you did not see them or they were nearby unbeknownst to you. You also probably do not remember exactly what streets you were walking and only have some pictures to remember the  trip. It would be nice if you could see all the stuff you might have missed or were supposed to see and how you might have traveled from picture to picture.

# 2. Run Instructions
Libraries:  
pip3 install fuzzywuzzy pandas numpy matplotlib scikit-learn  
pip3 install Request gpxpy polyline folium pillow  

Order of execution:  

Part A: Restaurants  
python3 clean_osm_data.py  
python3 restaurant_analysis.py  
python3 clusters.py  

Part B: Pictures and Geodata   
The program itself is all contained in analyzeGeotagPics.py  

example cmd line:  
python analyzeGeotagPics.py geotaggedEx  
python analyzeGeotagPics.py any_folder_name  


# 3. Data  
Part A: Restaurants 

files used in restaurant_analysis.py and clusters.py are:  
- datasets/chain_restaurants.csv
- datasets/independent_restaurants.csv
  
These CSV files are produced using clean_osm_data.py 

Part B: Pictures and Geodata

There is a provided folder of arbitrary example pictures with geotags, but the idea is that you can use any pictures you want if they are geotagged. Only png, jpg, and jpeg files accepted. For this project, geoimgr.com was used to artificially geotag pictures, but in theory, a user should have photos that are already geotagged on their phone hopefully. 

The program takes a folder of pictures,  even if it is just one picture,  so you can have multiple folders of pictures for your own organization in the same directory as the Python file, but you can only run one folder.

The folder input also technically takes a path, but for your own sanity and the program's effectiveness, just keep all picture folders in the same directory as the Python file.

# 4. Output
Part A: Restaurants   
restaurant_analysis.py produces:
- datasets/city_population_chain_count.csv, a CSV file with chain count predictions
- Images/plotOfChainCounts.jpg  
- Images/plotOfChainsPerCity.jpg  
- Images/numOfChainsVsPopulation.jpg  

clusters.py produces:  
  
datasets/chain_cluster.csv -updated  
datasets/indep_cluster.csv -updated   
These two datasets can be put in Google My Maps to visual the chain vs independent restaurants 
  
- Images/Affinity.png  
- Images/Agglomerative.png  
- Images/DBSCAN.png  
- Images/KMeans.png  


Part B: Pictures and Geodata
- straightPath.gpx, the gpx file, draws a straight line from point to point
- optimizedPath.gpx, uses Directions API to form a realistic street route
- gpx_display_map.html, runs once for each of the above GPXs to display the GPX in web format, but for tech savvy people you should probably just use a GPX viewer to colour the routes
- unique_attractions.txt, simple list of the attractions passed on the trip
- cmd terminal print outputs, says in detail where exactly among the trip the attractions were detected (e.g. Path A -> B contained [1, 2] and Point C had [3, 4])
