# Network Programming Over the MQTT Protocol
![MQTT Logo](https://mqtt.org/assets/img/mqtt-logo-transp.svg)\
Essentially, [MQTT](https://mqtt.org/) is an application layer protocol developed by OASIS which is mostly used in IoT platforms, such as [Azure IoT Hub](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-mqtt-support), [AWS IoT](https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html), and [Google Cloud IoT](https://cloud.google.com/iot/docs/how-tos/mqtt-bridge), etc. Also IoT devices support this protocol for communication (e.g. Arduino, ESP32, Raspberry Pi, etc).

## Architecture
**This is the basic structure of the MQTT protocol:**

![MQTT Architecture](https://mqtt.org/assets/img/mqtt-publish-subscribe.png)

MQTT stands for Message Queue Telemetry Transport. It is a transport protocol which is used to send and receive messages between devices. It is a publish-subscribe protocol, which means that the devices can send messages to the broker and receive messages from the broker. The broker is a central device which is responsible for distributing the messages to the devices (Or queues, to be exact). The broker is also responsible for keeping the devices in sync. So, the devices can receive messages from the broker even if they are not connected to the network.

## Getting started with the project
First of all, you can clone this github repository using the following command in your terminal:
``` bash
git clone https://github.com/RamtinPRG/MQTT_based_protocol.git
```
Then you need to install the Python dependencies in [`requirements.txt`](https://github.com/RamtinPRG/MQTT_based_protocol/blob/master/requirements.txt) file:
``` bash
pip install -r requirements.txt
```
## Details
This project is a smaller test of a hospital network. The hospital network consists of three devices: 
- central device
- patient device 
- doctor device

The central device is used for sending messages to the other devices. The patient device has the resposibility for receiving messages from the central device and sending them to the doctor device. The doctor device receives messages from the patient device and sending them to the central device.

It's programmed in Python 3.9 and uses `paho-mqtt` library and Eclipse MQTT broker by [Eclipse Foundation](https://www.eclipse.org/paho/index.php?page=clients/python/index.php) for the MQTT communication.