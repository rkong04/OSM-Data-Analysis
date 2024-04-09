import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import AffinityPropagation


chain = pd.read_csv('chain_restaurants.csv')
indep = pd.read_csv('independent_restaurant.csv')


#creates a png with a side by side of the clusterings of restaurants for chain vs independent
def showClustering(chain,indep,clusterType):

  fig, ax = plt.subplots(1, 2, figsize=(20, 8)) 

# Plot data points for chain restaurants
  for cluster_label in chain['cluster'].unique():
      cluster_data = chain[chain['cluster'] == cluster_label]
      ax[0].scatter(cluster_data['lon'], cluster_data['lat'], label=f'Cluster {cluster_label}')

  ax[0].set_title('Clustering of Chain Restaurants')
  ax[0].set_xlabel('Longitude')
  ax[0].set_ylabel('Latitude')
  ax[0].grid(True)

# Plot data points for independent restaurants
  for cluster_label in indep['cluster'].unique():
      cluster_data = indep[indep['cluster'] == cluster_label]
      ax[1].scatter(cluster_data['lon'], cluster_data['lat'], label=f'Cluster {cluster_label}')

  ax[1].set_title('Clustering of Independent Restaurants')
  ax[1].set_xlabel('Longitude')
  ax[1].set_ylabel('Latitude')
  ax[1].grid(True)

  name = "Images\\" + clusterType + ".png"
  plt.savefig(name)


#given two models, fit and predict the clustering for indep and chain restaurants
def fit_model(chain_model,indep_model,name):
    chain_cluster = chain_model.fit_predict(chain[['lat','lon']])
    indep_cluster = indep_model.fit_predict(indep[['lat','lon']])
    chain['cluster'] = chain_cluster
    indep['cluster'] = indep_cluster
    showClustering(chain,indep,name)
   
#KMeans
model1 = KMeans(n_clusters = 20)
model2 = KMeans(n_clusters = 20)
fit_model(model1,model2,"KMeans")

#Affinity 
Afmodel1 = AffinityPropagation(random_state=None)
Afmodel2 = AffinityPropagation(random_state=None)
fit_model(Afmodel1,Afmodel2,"Affinity")

#Agglomerative
Agmodel1 = AgglomerativeClustering(n_clusters = 20)
Agmodel2 = AgglomerativeClustering(n_clusters = 20)
fit_model(Agmodel1,Agmodel2,"Agglomerative")

#DBSCAN
chain_coord = chain[['lat','lon']].values
indep_coord = indep[['lat','lon']].values
eps = 1/6371    #1km radius 
db = DBSCAN(eps=eps,min_samples=5, algorithm='ball_tree', metric='haversine').fit_predict(np.radians(chain_coord))  #need to convert to radians to find distances using haversine
db2 = DBSCAN(eps=eps,min_samples=5, algorithm='ball_tree', metric='haversine').fit_predict(np.radians(indep_coord))
chain['cluster'] = db
indep['cluster'] = db2

chain_filtered = chain[chain['cluster'] != -1]
indep_filtered = indep[indep['cluster'] != -1] #remove noise (points where there werent at least min_samples amount of other restuarants within eps(1km))
showClustering(chain_filtered,indep_filtered,"DBSCAN")