# Documentation at: https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/html/index.html

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json

# Thing information
THING_ID = "thing47"
CLIENT_ID = "myClientID47" 
CERTIFICATE_PATH = "./certificates"
ENDPOINT = "a221a6r4ojicsi.iot.ap-southeast-1.amazonaws.com"
DEVICE1 = 'device74.231'
DEVICE2 = 'device72.227'
DEVICE3 = 'device72.228'

# Change to your topics here
UPDATE_TOPIC = "$aws/things/thing" + THING_ID + "/shadow/update"
DELTA_TOPIC = "$aws/things/thing" + THING_ID + "/shadow/update/delta"

ROOT_CA = CERTIFICATE_PATH + "/rootCA.pem"
PRIVATE_KEY = CERTIFICATE_PATH + "/private.key.pem"
CERTIFICATE_CRT = CERTIFICATE_PATH + "/certificate.crt.pem"

# General message notification callback
def customOnMessage(message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

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

# Subcribe function callback
def subscribeCallback(client, userdata, message):
    print("Subscribe callback: ", message.payload)

# Suback callback
def customSubackCallback(mid, data):
    print("Received SUBACK packet id: ")
    print(mid)
    print("Granted QoS: ")
    print(data)
    print("++++++++++++++\n\n")

# Puback callback
def customPubackCallback(mid):
    print("Received PUBACK packet id: ")
    print(mid)
    print("++++++++++++++\n\n")

# Generate a JSON message for publishing
def generate_msg_to_publish():
    publish_dict = {'state': {'reported': {'DEVICE1': 29, 'DEVICE2': 12, 'DEVICE3': 'Hello World!'}}}
    publish_message = json.dumps(publish_dict)
    print("Message to publish: ", publish_message)
    return publish_message

# Note that we are not putting a message callback here. We are using the general message notification callback.
myMQTTClient.subscribeAsync(DELTA_TOPIC, 1, ackCallback=customSubackCallback,       messageCallback=subscribeCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    myMQTTClient.publishAsync(UPDATE_TOPIC, generate_msg_to_publish(), 1, ackCallback=customPubackCallback)
    time.sleep(5)