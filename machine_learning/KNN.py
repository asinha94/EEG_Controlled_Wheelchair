X = [[0,1], [1,1], [2,2], [3,2], [1,2],[3,4]] #training data
y = ['a', 'a', 'a', 'b','b','c'] #corresponding mode
from sklearn.neighbors import KNeighborsClassifier
neigh = KNeighborsClassifier()
neigh.fit(X, y)
print(neigh.predict([[2,2]]))#predicts with real-time data
print(neigh.predict_proba([[0,2]]))
