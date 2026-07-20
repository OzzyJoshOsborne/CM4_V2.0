import json
import pytest
import datetime 
from unittest.mock import MagicMock, patch

from lib.rabbit import rabbitMQ
from lib.rabbit.rabbitMQController import RabbitMQController


#Bootup Rabbit
def test_bootupRabbit_success():
    
    mockConnection = MagicMock()
    mockConnection.return_value = True

    rabbitMQController = RabbitMQController()
    rabbitMQController.rabbit.connected = mockConnection()
    rabbitMQController.bootupRabbit()

    assert rabbitMQController.rabbitStatus == True

def test_bootupRabbit_fail():

    mockConnection = MagicMock()
    mockConnection.return_value = False

    rabbitMQController = RabbitMQController()
    rabbitMQController.rabbit.connected = mockConnection()
    rabbitMQController.bootupRabbit()

    assert rabbitMQController.rabbitStatus == False


#Create Json Msg
def test_createJsonMsg_success():
    rabbitMQController = RabbitMQController()

    command = 0
    data = "test Data"

    rabbitJson = rabbitMQController.createJsonMsg(command, data)

    assert rabbitJson["uuid"] == "macAddress"
    assert rabbitJson["Type"] == 0
    assert rabbitJson["timestamp"] == pytest.approx(datetime.datetime.now().timestamp())
    assert rabbitJson["data"] == "test Data"

def test_createJsonMsg_emptyData():
    rabbitMQController = RabbitMQController()

    command = None
    data = None

    rabbitJson = rabbitMQController.createJsonMsg(command, data)

    assert rabbitJson["uuid"] == "macAddress"
    assert rabbitJson["Type"] == None
    assert rabbitJson["timestamp"] == pytest.approx(datetime.datetime.now().timestamp())
    assert rabbitJson["data"] == None

#Send Data
def test_sendData_success():
    rabbitMQController = RabbitMQController()
    
    rabbitMQController.sendData(0, "test Data")

    rabbitJson = json.loads(rabbitMQController.sendQueue.get())

    assert rabbitJson["uuid"] == "macAddress"
    assert rabbitJson["Type"] == 0
    assert rabbitJson["timestamp"] == pytest.approx(datetime.datetime.now().timestamp())
    assert rabbitJson["data"] == "test Data"

def test_sendData_QueFull():
    rabbitMQController = RabbitMQController()

    rabbitMQController.sendQueue.empty()

    for i in range(50):
        rabbitMQController.sendQueue.put(i)

    assert rabbitMQController.sendData(0, "test Data") == False




