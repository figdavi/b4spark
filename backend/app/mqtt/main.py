from paho.mqtt import client as mqtt
from typing import Any, Literal
import json
import random

# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python#paho-mqtt-python-client-usage

# TODO: add broker and topics to .env, share with backend and sensors
# TODO: Update to MQTTv5 (If possible)


broker = "broker.hivemq.com"
port = 1883
topic = "mqtt_iot_123321/busuff"
client_id = f"subscribe-{random.randint(0, 1000)}"
transport = "tcp"  # or "websocket"
protocol = mqtt.MQTTv311


def connect_mqtt() -> mqtt.Client:
    def on_connect(client: mqtt.Client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client(
        client_id=client_id,
        transport=transport,
        protocol=protocol,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION1,
    )  # type: ignore
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt.Client):
    def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        print(f"From topic: '{msg.topic}', message: ")
        try:
            data = json.loads(msg.payload.decode())
            print(json.dumps(data, indent=4))
        except Exception as e:
            print(e)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    run()
