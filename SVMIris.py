import os

import csv
#import inline as inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import socketio
import json
from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)

sio = socketio.Client()
sio.connect('http://e3c85a63.ngrok.io')



#This is Iris data set, input own dataset
iris = pd.read_csv('iris.csv')

sns.pairplot(data=iris, hue='variety', palette='Set2')
# data is data, hue is different colors, pallete are colors for hue

#plt.show()

with open('iris.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
#print(data)

clf = svm.SVC(gamma='scale', C=1)
# C is classification margin, gamma is radius of influence of model chosen support vectors
x_train = iris.iloc[:, :-1]
y_train = iris.iloc[:, 4]
x_test = [iris.iloc[149, :-1]]
#y_test = [iris.iloc[149, 4]]

#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.6)
#Test Size is the E(out) percentage with regards to E(total)
model=SVC(kernel='rbf', C = 1)
# Use RBF if nonlinear, linear is linear
model.fit(x_train, y_train)

pred = model.predict(x_test)   # Predict

print('Prediction: ' + pred[0])

with open('data.json', 'w') as datajson:
    json.dump({'concentration': pred[0]}, datajson)

with open('user.json', 'r') as useremail:
    emailjson = json.load(useremail)
    print(emailjson)
    sio.emit('pi2database', {'concentration': pred[0], 'email': emailjson['email']})


sio.disconnect()
#print(confusion_matrix(y_test,pred))    # Correctness matrix

#print(classification_report(y_test, pred))  # Display correctness
