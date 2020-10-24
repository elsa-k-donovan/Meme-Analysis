import pandas as pd
from sklearn.cluster import KMeans, DBSCAN

# reference: https://benalexkeen.com/k-means-clustering-in-python/

file_loc = "/home/htabesh/scratch/data"

### Initialisation
df_features_norm = pd.read_json (file_loc + '/norm-memes-beta-features-partial.json')
df_features = pd.read_json (file_loc + '/memes-beta-features-partial.json')
output_file_name = file_loc + "/memes-clustered-features.json"
# Testing
# df_features = df_features.head(100)

## norm
# create df with X, Y cordinates <- this will make it easier to handle the cordinates
feature_cordinates_norm = pd.DataFrame(columns=['X','Y','path'])
for index, row in df_features_norm.iterrows():
    new_row = {'X':row[1][0], 'Y':row[1][1], 'path':row[0]}
    feature_cordinates_norm = feature_cordinates_norm.append(new_row, ignore_index=True)

## not norm
feature_cordinates = pd.DataFrame(columns=['X','Y','path'])
for index, row in df_features.iterrows():
    new_row = {'X':row[1][0], 'Y':row[1][1], 'path':row[0]}
    feature_cordinates = feature_cordinates.append(new_row, ignore_index=True)

# now lets figure out the number of cluster we need by using DBSCAN with non-normalized data
clustering = DBSCAN(eps=2, min_samples=4).fit(feature_cordinates[['X', 'Y']])
k = len(set(clustering.labels_))

# now we can use the K to run the k-mean algorithm with that many clusters
kmeans = KMeans(n_clusters=k)
kmeans.fit(feature_cordinates_norm[['X', 'Y']])
labels = kmeans.predict(feature_cordinates_norm[['X', 'Y']])
centroids = kmeans.cluster_centers_

# lets save to a new json
feature_cordinates_norm['cluster'] = labels
feature_cordinates_norm.to_json(output_file_name)


