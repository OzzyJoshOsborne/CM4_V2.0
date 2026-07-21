
import os
import sys
import time
import pika
from queue import Queue

class RabbitMQ:

    def __init__(self, receiveQueue, sendQueue, ip="10.0.1.1"):
        
        self.ip = ip
        self.port = 5672

        self.queueName = "hello"

        self.msgQueue = receiveQueue
        self.sendQueue = sendQueue

        self.connected = False
        self.connection = None
        self.channel = None

        self.running = True

    def createQueue(self):
        try:
            credentials = pika.PlainCredentials('firecamera', 'camerafire')
            parameters = pika.ConnectionParameters(
                self.ip, 
                self.port,
                socket_timeout = 5,
                connection_attempts = 1
            )# "/", credentials )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            self.channel.queue_declare(queue = self.queueName, durable = True)

            self.connected = True

            self.receiveData()

            return True
        except Exception as e:
            print(f"Error creating Queue - {e} - {type(e).__name__}")
            self.connected = False
            return False

    def sendData(self):
        try:
            # print(f"Send data - {self.sendQueue.empty()}")
            while not self.sendQueue.empty():
                msg = self.sendQueue.get()

                self.channel.basic_publish(
                    exchange = '',
                    routing_key = self.queueName,
                    body = msg
                )

            return True
        except Exception as e:
            print(f"Failed to send data - {type(e).__name__} - {e}")
            self.connected = False
            return False

    def receiveData(self):
        try:
            if not self.connected or self.channel == None:
                raise Exception("Not Connected") 

            self.channel.basic_qos(prefetch_count = 1)
            self.channel.basic_consume(
                queue = self.queueName, 
                on_message_callback = self.handleReceivedData
            )
            # self.channel.start_consuming()
        except Exception as e:
            print(f"Failed to recieve Data - {e}")
            self.connected = False
            return False

    def handleReceivedData(self, ch, method, properties, body):
        try:
            self.msgQueue.put(body, block = False)
            ch.basic_ack(delivery_tag = method.delivery_tag)
        except Exception as e:
            print(f"Error handling data - {type(e).__name__} - {e}")
            return False

    def processData(self):
        try:
            if not self.connected or self.channel == None:
                raise Exception("Not Connected") 
            
            self.connection.process_data_events(time_limit=1)
        except Exception as e:
            print(f"Failed to recieve Data - {e}")
            self.connected = False
            return False
            
    def reconnect(self):
        if self.createQueue():
            return
        time.sleep(5)

    def run(self):

        self.createQueue()

        while self.running:
            if self.connected is False:
                self.reconnect()
                continue

            self.sendData()

            self.processData()

if __name__ == "__main__":
    msgQueue = Queue(maxsize=50)
    sendQueue = Queue(maxsize=50)
    r1 = RabbitMQ(msgQueue, sendQueue, ip="192.168.89.80")


    # r1.recieveData()
    # try:
    #     r1.recieveData()
    # except KeyboardInterrupt:
    #     print('Interrupted')
    #     try:
    #         sys.exit(0)
    #     except SystemExit:
    #         os._exit(0)