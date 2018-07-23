# Documentation at: https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/html/index.html

import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Thing information
THING_ID = "Testing_Thing_1"
CLIENT_ID = "myClientID" 
CERTIFICATE_PATH = "./certificates"
ENDPOINT = "a221a6r4ojicsi.iot.ap-southeast-1.amazonaws.com"
DEVICE1 = 'device1.1'
DEVICE2 = 'device1.2'
DEVICE3 = 'device2.1'

# Change to your topics here
UPDATE_TOPIC = "$aws/things/thing" + THING_ID + "/shadow/update"
DELTA_TOPIC = "$aws/things/thing" + THING_ID + "/shadow/update/delta"

ROOT_CA = CERTIFICATE_PATH + "/rootCA.pem"
PRIVATE_KEY = CERTIFICATE_PATH + "/private.key.pem"
CERTIFICATE_CRT = CERTIFICATE_PATH + "/certificate.crt.pem"


# Configuration for AWS IoT
myMQTTClient = AWSIoTMQTTClient(CLIENT_ID)
myMQTTClient.configureEndpoint(ENDPOINT, 8883)
myMQTTClient.configureCredentials(ROOT_CA, PRIVATE_KEY, CERTIFICATE_CRT)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myMQTTClient.enableMetricsCollection()


# Connect to MQTT broker
connected = myMQTTClient.connect()
print("Connected: ", connected)


# Generate a JSON message for publishing
def generate_msg_to_publish():
    publish_dict = {'state': {'reported': {DEVICE1: 29, DEVICE2: 12, DEVICE3: 'Hello World!'}}}
    publish_message = json.dumps(publish_dict)
    print("Message to publish: ", publish_message)
    return publish_message

# Subcribe function callback
def subscribeCallback(client, userdata, message):
    print("Subscribe callback: ", message.payload)



# Listen for state change
myMQTTClient.subscribe(DELTA_TOPIC, 1, subscribeCallback)
time.sleep(2)

# Update device shadow
while True:
    published = myMQTTClient.publish(UPDATE_TOPIC, generate_msg_to_publish(), 0)
    print("Published: ", published)
    time.sleep(5)
