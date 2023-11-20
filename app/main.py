from fastapi import FastAPI
import uvicorn
import os
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List

app = FastAPI()

# MQTT Configuration
MQTT_HOST = os.environ.get('MQTT_HOST', 'localhost')
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
MQTT_TOPIC = os.environ.get('MQTT_TOPIC', 'guy/test')

# MongoDB Configuration
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
mongo_client = MongoClient(MONGO_URL)
db = mongo_client.mydatabase  # Data Base Name

# MQTT Client setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected successfully.")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    db.mqtt_messages.insert_one({"topic": msg.topic, "message": msg.payload.decode()})

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_start()

# Pydantic model for message
class Message(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"Guy": "Server On TESA"}


@app.get("/get-mqtt-messages")
def get_mqtt_messages():
    messages = list(db.mqtt_messages.find({}, {'_id': 0}))
    return messages

@app.post("/publish/")
def publish_message(message_data: Message):
    message = message_data.message
    result = client.publish(MQTT_TOPIC, message)
    
    return {"message": "Sent successfully", "payload": message}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
