# Put task2a.py code here
import csv
import pandas as pd
import numpy 
from sklearn import neighbors
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
        
world = pd.read_csv("world.csv")
life = pd.read_csv("life.csv")   
world = world.dropna()


# getting the headers of two csv.
header_world = world.columns.values.tolist()
header_life = life.columns.values.tolist()
merged_life = life.merge(world, left_on = "Country Code", right_on = "Country Code")
merged_life = merged_life.replace("..", numpy.nan)
merged_life.sort_values(by=['Country Code'], inplace=True)


# combining the rwo csv into one csv, where the last column is the life expactancy of birth.
header_world.append(header_life[-1])
classlabel = merged_life[['Life expectancy at birth (years)']]
data = merged_life.drop(['Country Name', 'Time', 'Country Code', 'Life expectancy at birth (years)', 'Country', 'Year'], axis = 1)

# train test split
X_train, X_test, y_train, y_test = train_test_split(data, classlabel, 
train_size=0.7, test_size=0.3, random_state=200)
median_dict = {}
median_list = []

for i in X_train.columns:
    median_dict[i] = round(X_train[i].median(), 3)
    median_list.append(round(X_train[i].median(), 3))    
X_train = X_train.fillna(value = median_dict)    
median_dict_2 = {}

for i in X_test.columns:
    median_dict_2[i] = round(X_test[i].median(), 3)    
X_test = X_test.fillna(value = median_dict_2) 
mean_list = []
var_list = []

for i in X_train.columns:
    X_train[i] = X_train[i].astype(float)
    mean = round(X_train[i].mean(), 3)
    var = numpy.var(X_train[i])
    mean_list.append(mean)
    var_list.append(var)
    
with open('task2a.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(['feature', 'median', 'mean', 'variance'])
    for i in range(20):
        mean_final = mean_list[i]
        median_final = median_list[i]
        variance_final = round(var_list[i], 3)
        writer.writerow([header_world[i+3], median_final, mean_final, 
variance_final])    
              
              
# 0 mean and unit variance.
scaler = preprocessing.StandardScaler().fit(X_train)
X_train=scaler.transform(X_train)
X_test=scaler.transform(X_test)
# make prediction when knn = 7.
knn_7 = neighbors.KNeighborsClassifier(n_neighbors=7)
knn_7.fit(X_train, y_train.values.ravel())
y_pred_7=knn_7.predict(X_test)
# make prediction when knn = 3.
knn_3 = neighbors.KNeighborsClassifier(n_neighbors=3)
knn_3.fit(X_train, y_train.values.ravel())
y_pred_3=knn_3.predict(X_test)
# find the prediction by using decision tree.
dt = DecisionTreeClassifier(random_state=200, max_depth=3)
dt.fit(X_train, y_train)
y_pred_tree=dt.predict(X_test)
        
print("Accuracy of decision tree: ", round(accuracy_score(y_test, y_pred_tree), 3))
print("Accuracy of k-nn, (k=3): ", round(accuracy_score(y_test, y_pred_3), 3))
print("Accuracy of K-nn, (k=7): ", round(accuracy_score(y_test, y_pred_7), 3))