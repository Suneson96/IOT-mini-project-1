import time
from azure.iot.device import IoTHubDeviceClient, Message
import board
import adafruit_dht
import json
from dht import DHTSensor
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
HOSTNAME = os.getenv("IOTHUB_HOSTNAME")
DEVICE_ID = os.getenv("IOTHUB_DEVICE_ID")
SHARED_ACCESS_KEY = os.getenv("IOTHUB_SHARED_ACCESS_KEY")

if not HOSTNAME or not DEVICE_ID or not SHARED_ACCESS_KEY:
    raise ValueError("Missing IoT Hub credentials in .env file.")

# Build the connection string
CONNECTION_STRING = f"HostName={HOSTNAME};DeviceId={DEVICE_ID};SharedAccessKey={SHARED_ACCESS_KEY}"
 
# Intialize the IoT Hub client and the DHT sensor
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
sensor = DHTSensor(board.D4)
 
while True:

    data = sensor.read()

    try:
        print(data)
        message = Message(json.dumps(data))
        message.content_encoding = "utf-8"
        message.content_type = "application/json"
        client.send_message(message)
        print(f"Sent: {data}")
    except Exception as e:
        print(f"Error: {e}")
 
    time.sleep(10)