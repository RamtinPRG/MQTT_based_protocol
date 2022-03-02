from enum import Enum
import logging
from queue import Queue

logging.basicConfig(level=logging.INFO)

class PatientStatus(Enum):
    PS_Emergency = 0    # needs detailed and exact information
    PS_Normal = 1

class Buffers(Enum):
    B_BrokerAddrress = 0
    B_ClientID = 1
    B_ClientAddrres = 2
    B_Topic = 3

class DataManager():
    brokerAddr = []
    clientIDs = []
    clientAddrs = []
    topics = []
    q = Queue()

    @classmethod
    def Add(cls, data, Buffer):
        match Buffer:
            case Buffers.B_BrokerAddrress:
                cls.brokerAddr.append(data)
            case Buffers.B_ClientID:
                cls.clientIDs.append(data)
            case Buffers.B_ClientAddrres:
                cls.clientAddrs.append(data)
            case Buffers.B_Topic:
                cls.topics.append(data)

    @classmethod
    def GetBufferAt(cls, Buffer):
        match Buffer:
            case Buffers.B_BrokerAddrress:
                return cls.brokerAddr
            case Buffers.B_ClientID:
                return cls.clientIDs
            case Buffers.B_ClientAddrres:
                return cls.clientAddrs
            case Buffers.B_Topic:
                return cls.topics

    @classmethod
    def CheckoutBuffer(cls, Buffer):
        buf = cls.GetBufferAt(cls, Buffer)
        for i in buf:
            print(i, end=', ')
        print()

# 0: Connection successful
# 1: Connection refused – incorrect protocol version
# 2: Connection refused – invalid client identifier
# 3: Connection refused – server unavailable
# 4: Connection refused – bad username or password
# 5: Connection refused – not authorised
# 6-255: Currently unused.
class CallBacks():
    def on_connect(client, userdate, flags, rc):        
        if rc == 0:
            client.connected_flag = True
            logging.info("Successfully connected")
        elif rc == 1:
            client.bad_connection_flag = True
            logging.info("Connection refused - incorrect protocol version; Return code: ", str(rc))
        elif rc == 2:
            client.bad_connection_flag = True
            logging.info("Connection refused - invalid client identifier; Return code: ", str(rc))
        elif rc == 3:
            client.bad_connection_flag = True
            logging.info("Connection refused - server unavailable; Return code: ", str(rc))
        elif rc == 4:
            client.bad_connection_flag = True
            logging.info("Connection refused - bad username or password; Return code: ", str(rc))
        elif rc == 5:
            client.bad_connection_flag = True
            logging.info("Connection refused - not authorised; Return code: : ", str(rc))
        else:
            client.bad_connection_flag = True
            logging.info("Currently unused; Return code: ", str(rc))
    
    def on_disconnect(client, userdata, rc):
        if rc == 0:
            logging.info("Disconected gracefully")
        else:
            logging.info("Disconnected - Return code: " + str(rc))
        client.connected_flag = False
        client.disconnect_flag = True

    def on_publish(client, userdata, mid):
        logging.info("on_publish: mid: " + str(mid))
    
    def on_subscribe(client, userdata, mid, granted_qos):
        logging.info("on_subscribe: mid: " + str(mid))
        logging.info("on_subscribe: granted_qos: " + str(granted_qos))

    def on_message(client, userdate, message):
        DataManager.q.put(message.topic + ": ", message.payload.decode("utf-8"))
        logging.info("message: " + message.topic + '> ' + message.payload.decode("utf-8"))

    def on_log(client, userdata, level, buf):
        logging.info("on_log: " + buf)
        
class SetFlags:
    def Connection(client):
        client.connected_flag = False
        client.bad_connection_flag = False
        client.disconnect_flag = False
    
    def Publish(patientStatus):
        match(patientStatus):
            case PatientStatus.PS_Emergency:
                return (1, True)    # TODO: handle the message duplication on the server-side
            case PatientStatus.PS_Normal:
                return (0, False)