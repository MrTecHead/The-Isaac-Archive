import paho.mqtt.client as mqtt
import subprocess

MQTT_HOST = "Your Home Assistant IP"      # Example: "192.168.1.50"
MQTT_PORT = 1883
MQTT_TOPIC = "notify/test"

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    subprocess.run(["notify-send", "Home Assistant", message])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()
