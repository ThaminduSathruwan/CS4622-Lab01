# -*- coding: utf-8 -*-
"""190257C_ML_Lab01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rh5oomnT0IIZUJ4JbGozRtMPxDBv2KnM

# CS4622 - Machine Learning Lab 01 - Feature Engineering

# Loading Data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.decomposition import PCA

# Loading data
train = pd.read_csv('/content/drive/MyDrive/train.csv')
valid = pd.read_csv('/content/drive/MyDrive/valid.csv')
test = pd.read_csv('/content/drive/MyDrive/test.csv')

train.head()

train.describe()

# Looking for missing values in train data set
train.isna().sum()

# Looking for missing values in valid data set
valid.isna().sum()

"""`label_2` contains missing values. Therefore, we need to handle those missing values in label_2 modelling."""

X = train.iloc[:, : -4]

X.head()

# KNN Classification Model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

def knn_classification(k, X_train, y_train, X_valid, y_valid):
  knn_model = KNeighborsClassifier(n_neighbors=k)
  knn_model.fit(X_train, y_train)
  y_pred = knn_model.predict(X_valid)
  accuracy = accuracy_score(y_valid, y_pred)
  return accuracy

# SVM Classification Model
from sklearn import svm
from sklearn import metrics

# clf = svm.SVC(kernel='linear', class_vector="balanced")
# print(metrics.confussion_matrix(y_valid, y_pred))

def svm_classification(X_train, y_train, X_valid, y_valid):
  clf = svm.SVC(kernel='linear')
  clf.fit(X_train, y_train)
  y_pred = clf.predict(X_valid)
  accuracy = accuracy_score(y_valid, y_pred)
  return accuracy

# Function to write to CSV
def create_csv(x, y_before_predict, y_after_predict, label_name):
    output_filename = f"/content/drive/My Drive/190257C_{label_name}.csv"
    combined_data = pd.DataFrame()

    combined_data["Predicted labels before feature engineering"] = y_before_predict
    combined_data["Predicted labels after feature engineering"] = y_after_predict
    combined_data["No of new features"] = [len(x.columns)] * len(combined_data)

    i = 0;
    while i < len(x.columns):
        column_name = x.columns[i]
        combined_data[f"new_feature_{i+1}"] = x[column_name]
        i += 1

    while i < 256:
        combined_data[f"new_feature_{i+1}"] = [None] * len(combined_data)
        i += 1

    combined_data.to_csv(output_filename, index=False)

"""# Modeling `label_1`: Speaker ID"""

# Split X and and label_1
X_label_1 = train.iloc[:, : -4]
y_label_1 = train['label_1']

X_valid_label_1 = valid.iloc[:, : -4]
y_valid_label_1 = valid['label_1']

X_test_label_1 = test.copy()
X_test_label_1 = X_test_label_1.iloc[:, : -4]

X_label_1.head()

y_label_1.head()

plt.figure(figsize=(12, 6))
y_label_1.hist()

"""Check accuracy before any feature selection"""

# KNN Classification Model
k=7
knn_model_label_1 = KNeighborsClassifier(n_neighbors=k)
knn_model_label_1.fit(X_label_1, y_label_1)

y_pred_label_1 = knn_model_label_1.predict(X_valid_label_1)
accuracy = accuracy_score(y_valid_label_1, y_pred_label_1)
print("Accuracy: ", accuracy)

# Predict label 1 before feature engineering for test dataset
y_pred_label_1_before = knn_model_label_1.predict(X_test_label_1)

"""Feature selection"""

# Check for columns with low variance
from sklearn.feature_selection import VarianceThreshold

var_thres = VarianceThreshold(threshold=0.2)
var_thres.fit(X_label_1)

low_variance_columns = [column for column in X_label_1.columns if column not in X_label_1.columns[var_thres.get_support()]]
print(len(low_variance_columns))

"""No low variance columns detected. Check for mutual information."""

# Check Mutual Information
from sklearn.feature_selection import mutual_info_classif, SelectPercentile
mutual_info = mutual_info_classif(X_label_1, y_label_1)
mutual_info

mutual_info = pd.Series(mutual_info)
mutual_info.index = X_label_1.columns
mutual_info.sort_values(ascending=False)

# Plot the ordered mutual_info values per feature
mutual_info.sort_values(ascending=False).plot.bar(figsize=(20, 8))

selected_top_columns = SelectPercentile(mutual_info_classif, percentile=20)
selected_top_columns.fit(X_label_1, y_label_1)
selected_column_names = X_label_1.columns[selected_top_columns.get_support()]
print(selected_column_names)
print(len(selected_column_names))

# Get selected columns from train and valid data sets
X_label_1_new = pd.DataFrame(X_label_1, columns=selected_column_names)
X_valid_label_1_new = pd.DataFrame(X_valid_label_1, columns=selected_column_names)
X_test_label_1_new = pd.DataFrame(X_test_label_1, columns=selected_column_names)

"""Check accuracy after feature selection"""

# Check accuracy again using KNN Classification Model
k=7
knn_model_label_1_new = KNeighborsClassifier(n_neighbors=k)
knn_model_label_1_new.fit(X_label_1_new, y_label_1)

y_pred_label_1_new = knn_model_label_1_new.predict(X_valid_label_1_new)
accuracy_new = accuracy_score(y_valid_label_1, y_pred_label_1_new)
print("New Accuracy: ", accuracy_new)

# Predict label 1 after feature engineering for test dataset
y_pred_label_1_after = knn_model_label_1_new.predict(X_test_label_1_new)

"""write CSV file for label_1"""

create_csv(X_test_label_1_new, y_pred_label_1_before, y_pred_label_1_after, "label_1")

"""# Modeling `label_2`: Speaker Age

Handlig missing values
"""

train

# Remove label_2 missing rows
label_2 = train[train['label_2'].notna()]
label_2_valid = valid[valid['label_2'].notna()]

label_2

# Split X and and label_2
X_label_2 = label_2.iloc[:, : -4]
y_label_2 = label_2['label_2']

X_valid_label_2 = label_2_valid.iloc[:, : -4]
y_valid_label_2 = label_2_valid['label_2']

X_test_label_2 = test.copy()
X_test_label_2 = X_test_label_2.iloc[:, : -4]

# Look y_label_2 after removing the missing values
y_label_2

# Check is there any missing values
y_label_2.isna().sum()

plt.figure(figsize=(12, 6))
y_label_2.hist()

"""Check accuracy before feature selection"""

# KNN Classification Model
k=7
knn_model_label_2 = KNeighborsClassifier(n_neighbors=k)
knn_model_label_2.fit(X_label_2, y_label_2)

y_pred_label_2 = knn_model_label_2.predict(X_valid_label_2)
accuracy = accuracy_score(y_valid_label_2, y_pred_label_2)
print("Accuracy: ", accuracy)

X_test_label_2

# Predict label 2 before feature engineering for test dataset
y_pred_label_2_before = knn_model_label_2.predict(X_test_label_2)

"""Use Principal component analysis"""

pca_label_2 = PCA(n_components=0.90, svd_solver='full')
pca_label_2.fit(X_label_2)
X_train_trf_label_2 = pd.DataFrame(pca_label_2.transform(X_label_2))
X_valid_trf_label_2 = pd.DataFrame(pca_label_2.transform(X_valid_label_2))
X_test_trf_label_2 = pd.DataFrame(pca_label_2.transform(X_test_label_2))
X_train_trf_label_2.shape

"""Check accuracy agian after principle component analysis"""

# Check accuracy again using KNN Classification Model
k=7
knn_model_label_2_new = KNeighborsClassifier(n_neighbors=k)
knn_model_label_2_new.fit(X_train_trf_label_2, y_label_2)

y_pred_label_2_new = knn_model_label_2_new.predict(X_valid_trf_label_2)
accuracy_new = accuracy_score(y_valid_label_2, y_pred_label_2_new)
print("New Accuracy: ", accuracy_new)

# Predict label 2 after feature engineering for test dataset
y_pred_label_2_after = knn_model_label_2_new.predict(X_test_trf_label_2)

"""write CSV file for label_2"""

create_csv(X_test_trf_label_2, y_pred_label_2_before, y_pred_label_2_after, "label_2")

"""# Modeling `label_3`: Speaker Gender"""

# Split X and and label_3
X_label_3 = train.iloc[:, : -4]
y_label_3 = train['label_3']

X_valid_label_3 = valid.iloc[:, : -4]
y_valid_label_3 = valid['label_3']

X_test_label_3 = test.copy()
X_test_label_3 = X_test_label_3.iloc[:, : -4]

y_label_3.value_counts()

class_counts = y_label_3.value_counts()

plt.figure(figsize=(10, 6))
class_counts.plot(kind='bar')
plt.title('Class Distribution')
plt.xlabel('Class')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# Oversampling usign SMOTE

from imblearn.over_sampling import SMOTE
from collections import Counter

# Apply SMOTE for oversampling
smote_label_3 = SMOTE(sampling_strategy='auto', random_state=42)
X_resampled_label_3, y_resampled_label_3 = smote_label_3.fit_resample(X_label_3, y_label_3)

# Visualize the class distribution after oversampling
print("Class distribution before oversampling:", Counter(y_label_3))
print("Class distribution after oversampling:", Counter(y_resampled_label_3))

"""Check accuracy before any feature selection"""

# KNN Classification Model
k=7
knn_model_label_3 = KNeighborsClassifier(n_neighbors=k)
knn_model_label_3.fit(X_resampled_label_3, y_resampled_label_3)

y_pred_label_3 = knn_model_label_3.predict(X_valid_label_3)
accuracy = accuracy_score(y_valid_label_3, y_pred_label_3)
print("Accuracy: ", accuracy)

# Predict label 3 before feature engineering for test dataset
y_pred_label_3_before = knn_model_label_3.predict(X_test_label_3)

"""Use Principal component analysis"""

from sklearn.decomposition import PCA

pca_label_3 = PCA(n_components=0.75, svd_solver='full')
pca_label_3.fit(X_resampled_label_3)
X_train_trf_label_3 = pd.DataFrame(pca_label_3.transform(X_resampled_label_3))
X_valid_trf_label_3 = pd.DataFrame(pca_label_3.transform(X_valid_label_3))
X_test_trf_label_3 = pd.DataFrame(pca_label_3.transform(X_test_label_3))
X_train_trf_label_3.shape

"""Check accuracy after feature selection"""

# Check accuracy again using KNN Classification Model
k=7
knn_model_label_3_new = KNeighborsClassifier(n_neighbors=k)
knn_model_label_3_new.fit(X_train_trf_label_3, y_resampled_label_3)

y_pred_label_3_new = knn_model_label_3_new.predict(X_valid_trf_label_3)
accuracy_new = accuracy_score(y_valid_label_3, y_pred_label_3_new)
print("New Accuracy: ", accuracy_new)

# Predict label 3 after feature engineering for test dataset
y_pred_label_3_after = knn_model_label_3_new.predict(X_test_trf_label_3)

"""write CSV file for label_3"""

create_csv(X_test_trf_label_3, y_pred_label_3_before, y_pred_label_3_after, "label_3")

"""# Modeling `label_4`: Speaker Accent"""

# Split X and and label_3
X_label_4 = train.iloc[:, : -4]
y_label_4 = train['label_4']

X_valid_label_4 = valid.iloc[:, : -4]
y_valid_label_4 = valid['label_4']

X_test_label_4 = test.copy()
X_test_label_4 = X_test_label_4.iloc[:, : -4]

y_label_4.value_counts()

class_counts = y_label_4.value_counts()

plt.figure(figsize=(10, 6))
class_counts.plot(kind='bar')
plt.title('Class Distribution')
plt.xlabel('Class')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

"""The `label_04` is imbalanced beacuse some classes having significantly fewer samples than others. For improve the performance using resampling.

**Applying Resampling:**
"""

# Oversampling usign SMOTE

from imblearn.over_sampling import SMOTE
from collections import Counter

# Apply SMOTE for oversampling
smote = SMOTE(sampling_strategy='auto', random_state=42)
X_resampled_label_4, y_resampled_label_4 = smote.fit_resample(X_label_4, y_label_4)

# Visualize the class distribution after oversampling
print("Class distribution before oversampling:", Counter(y_label_4))
print("Class distribution after oversampling:", Counter(y_resampled_label_4))

"""Check accuracy before any feature selection"""

# KNN Classification Model
k=7
knn_model_label_4 = KNeighborsClassifier(n_neighbors=k)
knn_model_label_4.fit(X_resampled_label_4, y_resampled_label_4)

y_pred_label_4 = knn_model_label_4.predict(X_valid_label_4)
accuracy = accuracy_score(y_valid_label_4, y_pred_label_4)
print("Accuracy: ", accuracy)

# Predict label 4 before feature engineering for test dataset
y_pred_label_4_before = knn_model_label_4.predict(X_test_label_4)

"""Use Principal component analysis"""

from sklearn.decomposition import PCA

pca_label_4 = PCA(n_components=0.90, svd_solver='full')
pca_label_4.fit(X_resampled_label_4)
X_train_trf_label_4 = pd.DataFrame(pca_label_4.transform(X_resampled_label_4))
X_valid_trf_label_4 = pd.DataFrame(pca_label_4.transform(X_valid_label_4))
X_test_trf_label_4 = pd.DataFrame(pca_label_4.transform(X_test_label_4))
X_train_trf_label_4.shape

"""Check accuracy after feature selection"""

# Check accuracy again using KNN Classification Model
k=7
knn_model_label_4_new = KNeighborsClassifier(n_neighbors=k)
knn_model_label_4_new.fit(X_train_trf_label_4, y_resampled_label_4)

y_pred_label_4_new = knn_model_label_4_new.predict(X_valid_trf_label_4)
accuracy_new = accuracy_score(y_valid_label_4, y_pred_label_4_new)
print("New Accuracy: ", accuracy_new)

# Predict label 4 after feature engineering for test dataset
y_pred_label_4_after = knn_model_label_4_new.predict(X_test_trf_label_4)

"""write CSV file for label_4"""

create_csv(X_test_trf_label_4, y_pred_label_4_before, y_pred_label_4_after, "label_4")