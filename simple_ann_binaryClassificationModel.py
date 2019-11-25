# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 22:57:38 2018

@author: Sanmoy
"""
import os
import pandas as pd
import numpy as np
import seaborn as sb

path="C:/F/NMIMS/DataScience/Sem-3/DL/data"
os.chdir(path)

##Read CSV
churn_data = pd.read_csv("Churn_Modelling.csv")
churn_data.info()
churn_data.describe()
churn_data.head(3)
churn_data.tail(3)
churn_data.isnull().sum()

geo = pd.get_dummies(churn_data['Geography'], drop_first=True)
geo.head()

gender = pd.get_dummies(churn_data['Gender'], drop_first=True)
gender.head()

churn_data.drop(['RowNumber', 'CustomerId', 'Surname', 'Geography', 'Gender'], 1, inplace=True)
churn_data_dmmy = pd.concat([geo, gender,churn_data], axis=1)
churn_data_dmmy.info()
churn_data_dmmy.head()

X=churn_data_dmmy.iloc[:, 0:11].values
y=churn_data_dmmy.iloc[:, 11].values

#Splitting into train and test
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Standardising
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)


import keras
from keras.models import Sequential
from keras.layers import Dense

classifier = Sequential()

#Adding first hidden layer
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu', input_dim=11))

#Adding second hidden layer
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))

#Adding output layer
classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))

#Compile,
#adam is stochastic gradient algorithm
classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#Fit the model on traiing set
classifier.fit(X_train, y_train, batch_size=10, epochs=100)


# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)


