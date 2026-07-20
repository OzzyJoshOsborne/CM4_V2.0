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

    def createJsonMsg(self, data):
        #TODO: Add check data type and create obj accordingly - If dict use json.dumps
        return {
            "uuid": "macAddress",
            "Type": 1,
            "timestamp": datetime.datetime.now().timestamp(),
            "data": data
        }

    def sendData(self, data):
        jsonMsg = json.dumps(self.createJsonMsg(data))
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

    time.sleep(2)

    r1.sendData("Test")

    while True:
        pass
