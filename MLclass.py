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
import as7262
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(10,GPIO.OUT)
GPIO.output(10, GPIO.HIGH)

simplefilter(action='ignore', category=FutureWarning)

try:
    sio = socketio.Client()
    sio.connect('http://e3c85a63.ngrok.io')
except:
    pass

as7262.soft_reset()
as7262.set_gain(64)
as7262.set_integration_time(17.857)
as7262.set_measurement_mode(2)
as7262.set_illumination_led(0)

totred = 0
totorange = 0
totyellow = 0
totgreen = 0
totblue = 0
totviolet = 0

try:
    for i in range(50):
        values = as7262.get_calibrated_values()
        print("""
Red:    {}
Orange: {}
Yellow: {}
Green:  {}
Blue:   {}
Violet: {}""".format(*values))
        totred += values.red
        totorange += values.orange
        totyellow += values.yellow
        totgreen += values.green
        totblue += values.blue
        totviolet += values.violet

    totred = totred / 50
    totorange = totorange / 50
    totyellow = totyellow / 50
    totgreen = totgreen / 50
    totblue = totblue / 50
    totviolet = totviolet / 50

except KeyboardInterrupt:
    as7262.set_measurement_mode(3)


x_testset = [{'Red': totred, 'Orange': totorange, 'Yellow': totyellow, 'Green':totgreen, 'Blue': totblue, 'Violet': totviolet}]

x_test = pd.DataFrame(x_testset)



#This is Iris data set, input own dataset
iris = pd.read_csv('Data_Final.csv', dtype=object)

sns.pairplot(data=iris,vars=["Red","Orange","Yellow","Green","Blue","Violet"], hue='concentration', palette='Set2')
# data is data, hue is different colors, pallete are colors for hue

#plt.show()

with open('Data_Final.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

print(data)

clf = svm.SVC(gamma='0.0001', C=0.0001)
# C is classification margin, gamma is radius of influence of model chosen support vectors
x_train = iris.iloc[:, :-1]
y_train = iris.iloc[:, 6]
#x_test = [iris.iloc[149, :-1]]
#y_test = [iris.iloc[149, 4]]

#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
#Test Size is the E(out) percentage with regards to E(total)
model=SVC(kernel='rbf', C = 0.0001)
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
