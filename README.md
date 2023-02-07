# 11-DataProcessing-Python-2020

This project is about implementing and evaluating a data linkage system and a classification system using data science principles. 

For task 1, there are two datasets, and my task is to use my data processing skill to match the related data from two datasets. What I have done is, I get rid of the punctuations, extracted the useful information (in this case, is the suffix and prefix) and made string comparison. As a result, task 1a has achieved 0.85 for recall and precision (recall = tp/(tp+fn), precision = tp/(tp+fp)) and my task 1b achieved 0.96 for pair completeness, 0.97 for reduction radio, which is a surprisingly good outcome.

For task 2a, I still have two datasets, and my task is to split the dataset to 70% training set and 30% testing set, in order to test the accuracy of different classification method Knn(k=3), decision tree, Knn(k=7). As a result, accuracy of decision tree is 0.709, k-nn(k=3) is 0.691 and k-nn(k=7) is 0.727. So k-nn(k=7) has the greatest prediction accuracy.

Task 2b is based on Knn (k=3), but I need to use feature engineering (i.e. given a pair of features f1 and f2, create a new feature f12 = f1 x f2) and selection to achieve higher accuracy. I firstly made the data cleaning, and then I applied three different methods on feature engineering, which are “first 4 features”, “best 4 features” and “PCA”(reduce the dimensionality of datasets, increase interpretability and minimize information loss) respectively. As a result, PCA gives the accuracy 0.764 which is the highest accuracy among three methods, and higher than the accuracy in task 2a.

Note: please look at the task 1c report and task 2c report for detail explainations.
