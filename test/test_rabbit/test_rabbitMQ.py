import pika.exceptions
import pytest
import pika
from queue import Queue
from unittest.mock import MagicMock, patch

from lib.rabbit.rabbitMQ import RabbitMQ

recieveQueue = Queue(maxsize=50)
sendQueue = Queue(maxsize=50)
ip = "192.168.89.80"

#Create Que
def test_createQueue_success():

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)

    assert rabbitMQ.createQueue() == True

@patch("lib.rabbit.rabbitMQ.pika")
def test_createQueue_rabbitOffline(mockPika):
    mockPika.BlockingConnection.side_effect = pika.exceptions.AMQPChannelError()

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)

    assert rabbitMQ.createQueue() == False

@patch("lib.rabbit.rabbitMQ.pika")
def test_createQueue_wrongIpPort(mockPika):
    mockPika.BlockingConnection.side_effect = pika.exceptions.AMQPChannelError()

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)
    rabbitMQ.ip = "192.168.89.85"

    assert rabbitMQ.createQueue() == False

    mockPika.BlockingConnection.side_effect = pika.exceptions.AMQPConnectionError()

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)
    rabbitMQ.ip = "192.168.89.80"
    rabbitMQ.port = 5673
    
    assert rabbitMQ.createQueue() == False

#Send Data
def test_sendData_ValidData():
    mockChannel = MagicMock()
    mockChannel.basic_publish.return_value = True

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)
    sendQueue.put("Msg")
    rabbitMQ.channel = mockChannel

    assert rabbitMQ.sendData() == True

def test_sendData_NoData():
    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)
    sendQueue.put(None)

    assert rabbitMQ.sendData() == False

def test_sendData_Disconnect():
    mockChannel = MagicMock()
    mockChannel.basic_publish.side_effect = AttributeError()

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)
    rabbitMQ.sendQueue.put("Test")

    assert rabbitMQ.sendData() == False

def test_sendData_QueueDeleted():
    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)
    rabbitMQ.sendQueue = None

    assert rabbitMQ.sendData() == False

def test_sendData_LargeData():
    mockChannel = MagicMock()

    sendQueueFill = Queue(maxsize=50)
    rabbitMQ = RabbitMQ(recieveQueue, sendQueueFill, ip=ip)
    rabbitMQ.channel = mockChannel

    for i in range(50):
        sendQueueFill.put(i)

    assert rabbitMQ.sendData() == True


#Receive Data
def test_receiveData_Success():
    mockChannel = MagicMock()
    mockChannel.basic_consume.return_value = True

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)
    rabbitMQ.connected = True
    rabbitMQ.channel = mockChannel
    
    rabbitMQ.receiveData()
    mockChannel.basic_consume.assert_called_once()

def test_receiveData_Error():
    mockChannel = MagicMock()
    mockChannel.basic_consume.side_effect = Exception

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)
    rabbitMQ.connected = True
    rabbitMQ.channel = mockChannel

    assert rabbitMQ.receiveData() == False

def test_receiveData_NotConnected():
    mockChannel = MagicMock()
    mockChannel.basic_consume.side_effect = Exception

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)
    rabbitMQ.connected = False

    assert rabbitMQ.receiveData() == False


#Handle Recieved Data
def test_handleReceiveData_Success():
    mockChannel = MagicMock()
    mockChannel.basic_ack.return_value = True

    mockMethod = MagicMock()
    mockMethod.delivery_tag.return_value = 0

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)

    rabbitMQ.handleReceivedData(mockChannel, mockMethod, "properties", "New Data")

    # print(recieveQueue.get())
    assert recieveQueue.get() == "New Data" 

def test_handleReceiveData_fullQueue():
    mockChannel = MagicMock()
    mockChannel.basic_ack.return_value = True

    mockMethod = MagicMock()
    mockMethod.delivery_tag.return_value = 0

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)

    recieveQueue.empty()
    for i in range(50):
        recieveQueue.put(i)

    rabbitMQ.handleReceivedData(mockChannel, mockMethod, "properties", "New Data")

    # print(recieveQueue.get())
    assert rabbitMQ.handleReceivedData(mockChannel, mockMethod, "properties", "New Data") == False
    recieveQueue.empty()

def test_handleReceiveData_basicAckFail():
    mockChannel = MagicMock()
    mockChannel.basic_ack.side_effect = Exception()

    mockMethod = MagicMock()
    mockMethod.delivery_tag.return_value = 0

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)

    assert rabbitMQ.handleReceivedData(mockChannel, mockMethod, "properties", "New Data") == False


#Process Data
def test_processData_success():
    mockConnection = MagicMock()
    mockConnection.process_data_events.return_value = True

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)
    rabbitMQ.connected = True
    rabbitMQ.channel = True
    rabbitMQ.connection = mockConnection

    rabbitMQ.processData()

    mockConnection.process_data_events.assert_called_once()


def test_processData_error():
    mockConnection = MagicMock()
    mockConnection.process_data_events.side_effect = Exception()

    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)
    rabbitMQ.connected = True
    rabbitMQ.channel = True
    rabbitMQ.connection = mockConnection

    return rabbitMQ.processData() == False

def test_processData_notConnected():
    rabbitMQ = RabbitMQ(recieveQueue, sendQueue, ip=ip)

    return rabbitMQ.processData() == False