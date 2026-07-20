import time
import json
import datetime
import threading
from queue import Queue
# from lib.rabbit.rabbitMQ import RabbitMQ
# from lib.rabbit.rabbitCommandHandler import RabbitCommandHandler
from rabbitMQ import RabbitMQ
from rabbitCommandHandler import RabbitCommandHandler


class RabbitMQController:

    def __init__(self):
        
        self.msgQueue = Queue(maxsize=50)
        self.sendQueue = Queue(maxsize=50)

        self.rabbit = RabbitMQ(
            self.msgQueue, 
            self.sendQueue,
            ip="192.168.89.80",
        )

        self.commandHandler = RabbitCommandHandler()

        self.rabbitStatus = False

        self.running = True

    def bootupRabbit(self):
        self.createRabbitThread()
        self.rabbitStatus = self.rabbit.connected

    def createJsonMsg(self, type, data):
        return {
            "uuid": "macAddress",
            "Type": type,
            "timestamp": datetime.datetime.now().timestamp(),
            "data": data
        }

    def sendData(self, type, data):
        jsonMsg = json.dumps(self.createJsonMsg(type, data))
        self.sendQueue.put(jsonMsg)

    def handleCommands(self):
        while self.running:
            newMsg = self.msgQueue.get()
            self.commandHandler.processsMsg(newMsg)

    def createRabbitThread(self):
        self.rabbitReceiveThread = threading.Thread(target = self.rabbit.run, daemon = True)
        self.rabbitReceiveThread.start()

    def createHandlerThread(self):
        self.rabbitHandlerThread = threading.Thread(target = self.handleCommands, daemon = True)
        self.rabbitHandlerThread.start()

    def run(self):
        self.createHandlerThread()


if __name__ == "__main__":
    r1 = RabbitMQController()
    r1.bootupRabbit()
    r1.run()

    time.sleep(1)

    r1.sendData(0, "Test")

    time.sleep(1)

    r1.sendData(1, "heartbeat")

    time.sleep(1)

    testJson = {
            "d1": "Data 1",
            "d2": "Data 2"
        }
    
    r1.sendData(2, testJson)

    while True:
        pass
