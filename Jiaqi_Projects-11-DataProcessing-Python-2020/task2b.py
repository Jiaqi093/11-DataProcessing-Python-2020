import csv
import pandas as pd
import numpy
from sklearn import neighbors
from sklearn import preprocessing
from sklearn.cluster import KMeans
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt


world = pd.read_csv("world.csv")
life = pd.read_csv("life.csv")  
world = world.dropna()
merged_life = life.merge(world, left_on = "Country Code", right_on = "Country Code")
merged_life = merged_life.replace("..", numpy.nan)
merged_life.sort_values(by=['Country Code'], inplace=True)     
classlabel = merged_life[['Life expectancy at birth (years)']]
data = merged_life.drop(['Country Name', 'Time', 'Country Code', 'Life expectancy at birth (years)', 'Country', 'Year'], axis = 1)          
    

median_dict = {}
for i in data.columns:
    median_dict[i] = data[i].median()   
data1 = data.fillna(value = median_dict)   
data2 = data.fillna(value = median_dict)
for i in range(len(data2.columns)):
    for j in range(i+1, len(data2.columns)):
        data1[f"feature{str(i), str(j)}"] = ((data1.iloc[:,i].astype('float') * data1.iloc[:,j].astype('float')))
   
# last feature
kmeans = KMeans(n_clusters=3, random_state=0).fit(data1)
data1["feature_cluster"] = (kmeans.labels_)

# Knn - 3.
X_train, X_test, y_train, y_test = train_test_split(data1, classlabel, 
train_size=0.7, test_size=0.3, random_state=200)
scaler = preprocessing.StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
best4features = SelectKBest(k=4)
fit = best4features.fit(X_train, y_train.values.ravel())
best_train = fit.transform(X_train)
best_test = fit.transform(X_test)
knn = neighbors.KNeighborsClassifier(n_neighbors=3)
knn.fit(best_train, y_train.values.ravel())
output_3nn = round(knn.score(best_test, y_test), 3)
print("Accuracy of feature engineering: ", output_3nn)
accu_list_1 = []
whole_range_1 = range(1, 80)

for i in whole_range_1:
    knn = neighbors.KNeighborsClassifier(n_neighbors=i)
    knn.fit(best_train, y_train.values.ravel()) 
    y_pred=knn.predict(best_test)
    accu_list_1.append(accuracy_score(y_test, y_pred))
    
plt.plot(whole_range_1, accu_list_1)
plt.xlabel('varing of k')
plt.ylabel('accuracy')
plt.title("best 4 features accuracy vs varing of k neighbors")
plt.savefig('task2bgraph1.png')
plt.show() 


# PCA
X_train, X_test, y_train, y_test = train_test_split(data1, classlabel, 
train_size=0.7, test_size=0.3, random_state=200)
scaler = preprocessing.StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
pca = PCA(n_components=4).fit(X_train)
pca_train = pd.DataFrame(pca.transform(X_train))
pca_test = pd.DataFrame(pca.transform(X_test))
knn_pca = neighbors.KNeighborsClassifier(n_neighbors=3)
knn_pca.fit(pca_train, y_train.values.ravel())
output_pca = round(knn_pca.score(pca_test, y_test), 3)
print("Accuracy of PCA: ", output_pca)
accu_list_2 = []
whole_range_2 = range(1, 80)

for i in whole_range_2:
    knn = neighbors.KNeighborsClassifier(n_neighbors=i)
    knn.fit(pca_train, y_train.values.ravel()) 
    y_pred=knn.predict(pca_test)
    accu_list_2.append(accuracy_score(y_test, y_pred))
    
plt.plot(whole_range_2, accu_list_2)
plt.xlabel('varing of k')
plt.ylabel('accuracy')
plt.title("PCA accuracy vs varing of k neighbors")
plt.savefig('task2bgraph2.png')
plt.show() 


# first 4 features
first_four = data1.iloc[:,0:4]
X_train_2, X_test_2, y_train, y_test = train_test_split(first_four, classlabel, 
train_size=0.7, test_size=0.3, random_state=200)
scaler = preprocessing.StandardScaler().fit(X_train_2)
X_train_4 = scaler.transform(X_train_2)
X_test_4 = scaler.transform(X_test_2)
knn = neighbors.KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train_4, y_train.values.ravel())
output_first_4_3nn = round(knn.score(X_test_4 , y_test), 3)
print("Accuracy of first four features: ", output_first_4_3nn)
accu_list_3 = []
whole_range_3 = range(1, 80)

for i in whole_range_3:
    knn = neighbors.KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train_4, y_train.values.ravel()) 
    y_pred=knn.predict(X_test_4)
    accu_list_3.append(accuracy_score(y_test, y_pred))
    
plt.plot(whole_range_3, accu_list_3)
plt.xlabel('varing of k')
plt.ylabel('accuracy')
plt.title("first 4 features accuracy vs varing of k neighbors")
plt.savefig('task2bgraph3.png')
plt.show()