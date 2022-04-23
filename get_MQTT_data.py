import thingspeak
import paho.mqtt.client as mqtt

channel_id=1535009
read_key='9KJ5DKI59C47S0EY'
write_key='DYZX93FXKNVW3MDM'
gateway=thingspeak.Channel(id=channel_id, api_key=write_key)

MQTT_ADDRESS = '192.168.150.110'
MQTT_USER = 'naman'
MQTT_PASSWORD = '1234'
MQTT_TOPIC = 'home/+/+'


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload.decode()))
    response=gateway.update({'field1':msg.payload.decode()})


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