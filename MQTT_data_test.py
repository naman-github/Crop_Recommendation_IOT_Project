import RPi.GPIO as GPIO
import thingspeak
import paho.mqtt.client as mqtt
from Adafruit_IO import Client, Feed

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

MQTT_ADDRESS = '10.33.0.87'
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


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()