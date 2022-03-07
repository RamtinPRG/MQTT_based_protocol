import paho.mqtt.client as mqtt
import time
from random import uniform
from SharedLibs import *
import sys

logging.basicConfig(level=logging.info)

brokerAddr = "mqtt.eclipseprojects.io"
DataManager.Add(brokerAddr, Buffers.B_BrokerAddrress)

clientID = "Client" + str(time.time()) + str(uniform(0.0, 10.0))
DataManager.Add(clientID, Buffers.B_ClientID)
client = mqtt.Client(clientID, False)

DataManager.CheckoutBuffer(Buffers.B_ClientID)
DataManager.CheckoutBuffer(Buffers.B_BrokerAddrress)

# call back binding
client.on_log = CallBacks.on_log
client.on_connect = CallBacks.on_connect
client.on_disconnect = CallBacks.on_disconnect
client.on_publish = CallBacks.on_publish
client.on_subscribe = CallBacks.on_subscribe
client.on_message = CallBacks.on_message

SetFlags.Connection(client)
QOS, isRetain = SetFlags.Publish(PatientStatus.PS_Emergency)
logging.info("Connecting to Broker...")
client.connect(brokerAddr)

client.loop_start()

while not client.connected_flag and not client.bad_connection_flag:
    print(".", end='', flush=True)
    time.sleep(0.1)
if client.bad_connection_flag:
    client.disconnect()
    client.loop_stop()
    sys.exit()

topic = "BloodPressure"
DataManager.Add(topic, Buffers.B_Topic)
msg = uniform(0, 100)
logging.info("Message: " + str(msg))
client.publish(topic, str(msg), QOS, isRetain)
time.sleep(3)

client.subscribe(topic, QOS)
time.sleep(3)

client.disconnect()
client.loop_stop()
