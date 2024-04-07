import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

chain = pd.read_csv('chain_restaurants.csv')
indep = pd.read_csv('independent_restaurant.csv')

model1 = KMeans(n_clusters = 20)
model2 = KMeans(n_clusters = 20)
chain_cluster = model1.fit_predict(chain[['lat','lon']])
indep_cluster = model2.fit_predict(indep[['lat','lon']])


chain['cluster'] = chain_cluster
indep['cluster'] = indep_cluster


plt.figure(figsize=(10, 8))

# Plot data points colored by their assigned clusters
for cluster_label in chain['cluster'].unique():
    cluster_data = chain[chain['cluster'] == cluster_label]
    plt.scatter(cluster_data['lon'], cluster_data['lat'], label=f'Cluster {cluster_label}')

plt.title('KMeans Clustering of Chain Restaurants')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.grid(True)
# plt.show()
plt.savefig('kmeans_chain.png')





plt.figure(figsize=(10, 8))

# Plot data points colored by their assigned clusters
for cluster_label in indep['cluster'].unique():
    cluster_data = indep[indep['cluster'] == cluster_label]
    plt.scatter(cluster_data['lon'], cluster_data['lat'], label=f'Cluster {cluster_label}')

plt.title('KMeans Clustering of indep Restaurants')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.grid(True)
# plt.show()
plt.savefig('kmeans_indep.png')