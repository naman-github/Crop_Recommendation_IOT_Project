import RPi.GPIO as GPIO
import thingspeak
import paho.mqtt.client as mqtt
#importing the required libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from Adafruit_IO import Client, Feed


#Reading the csv file
data=pd.read_csv('cpdata.csv')
print(data.head(1))

#Creating dummy variable for target i.e label
label= pd.get_dummies(data.label).iloc[: , 1:]
data= pd.concat([data,label],axis=1)
data.drop('label', axis=1,inplace=True)
print('The data present in one row of the dataset is')
print(data.head(1))
train=data.iloc[:, 0:4].values
test=data.iloc[: ,4:].values

#Dividing the data into training and test set
X_train,X_test,y_train,y_test=train_test_split(train,test,test_size=0.3)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#Importing Decision Tree classifier
from sklearn.tree import DecisionTreeRegressor
clf=DecisionTreeRegressor()

#Fitting the classifier into training set
clf.fit(X_train,y_train)
pred=clf.predict(X_test)

from sklearn.metrics import accuracy_score
# Finding the accuracy of the model
a=accuracy_score(y_test,pred)
print("The accuracy of this model is: ", a*100)


#Sending the predicted crop to database
cp=firebase.put('/croppredicted','crop',c)


channel_id=1535009
read_key='9KJ5DKI59C47S0EY'
write_key='DYZX93FXKNVW3MDM'
gateway=thingspeak.Channel(id=channel_id, api_key=write_key)

Adafruit_IO_KEY = 'aio_iHjV63vQn7MGMRCd2k36B8PIwcZ1'
Adafruit_IO_USERNAME = 'naman001'
aio = Client(Adafruit_IO_USERNAME, Adafruit_IO_KEY)

Humidity_feed=aio.feeds('humidity')
Temprature_feed=aio.feeds('temperature')
Moisture_feed=aio.feeds('moisture')

MQTT_ADDRESS = '192.168.150.110'
MQTT_USER = 'naman'
MQTT_PASSWORD = '1234'
MQTT_TOPIC = 'home/livingroom/humidity'
MQTT_TOPIC_1 = 'home/livingroom/temperature'
MQTT_TOPIC_2 = 'home/livingroom/soil'

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)
    client.subscribe(MQTT_TOPIC_1)
    client.subscribe(MQTT_TOPIC_2)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload.decode()))
    if(msg.topic == MQTT_TOPIC):
        Humidity=msg.payload.decode()
        response=gateway.update({'field1':Humidity})
        aio.send(Humidity_feed.key, str(Humidity))
        
    if(msg.topic == MQTT_TOPIC_1):
       Temperature=msg.payload.decode()
       response=gateway.update({'field2':Temperature})
       aio.send(Temprature_feed.key, str(Temperature))
       
    if(msg.topic == MQTT_TOPIC_2):
       Moisture=msg.payload.decode()
       response=gateway.update({'field3':Moisture})
       aio.send(Moisture_feed.key, str(Moisture))


def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()




ah=str(Humidity)
atemp=str(Temperature)
shum=str(Moisture)
pH=6.259086583
rain=57.40847165


l=[]
l.append(ah)
l.append(atemp)
l.append(pH)
l.append(rain)
predictcrop=[l]

# Putting the names of crop in a single list
crops=['wheat','mungbean','Tea','millet','maize','lentil','jute','cofee','cotton','ground nut','peas','rubber','sugarcane','tobacco','kidney beans','moth beans','coconut','blackgram','adzuki beans','pigeon peas','chick peas','banana','grapes','apple','mango','muskmelon','orange','papaya','watermelon','pomegranate']
cr='rice'

#Predicting the crop
predictions = clf.predict(predictcrop)
count=0
for i in range(0,30):
    if(predictions[0][i]==1):
        c=crops[i]
        count=count+1
        break;
    i=i+1
if(count==0):
    print('The predicted crop is %s'%cr)
else:
    print('The predicted crop is %s'%c)

if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
