import time
import sys
from random import randint

import paho.mqtt.client as mqtt
import keyboard
from SharedLibs import *

logging.basicConfig(level=logging.info)

brokerAddr = "mqtt.eclipseprojects.io"
DataManager.Add(brokerAddr, Buffers.B_BrokerAddrress)

clientID = f"Client{time.time()}{randint(0, 10)}"
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
QoS, isRetain = SetFlags.Publish(PatientStatus.PS_Emergency)
logging.info("Connecting to Broker...")
client.connect(brokerAddr, 1883)

client.loop_start()

while not client.connected_flag and not client.bad_connection_flag:
    print(".", end='', flush=True)
    time.sleep(0.1)
if client.bad_connection_flag:
    client.disconnect()
    client.loop_stop()
    sys.exit()

topic = "BodyTemperature"
DataManager.Add(topic, Buffers.B_Topic)

client.subscribe(topic, QoS)

while not keyboard.is_pressed('q'):
    pass

client.disconnect()
client.loop_stop()
