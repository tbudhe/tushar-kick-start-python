from sklearn.cluster import KMeans

data = [[1, 1], [1.5, 2], [3, 4], [5, 7], [3.5, 5], [4.5, 5], [3.5, 4.5]]

model = KMeans(n_clusters=2, random_state=0, n_init=10)
model.fit(data)

print(model.labels_)  # groups it invented itself - no correct answers given