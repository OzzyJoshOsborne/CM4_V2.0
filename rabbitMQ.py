
import os
import sys
import time
import pika

class RabbitMQ:

    def __init__(self, queue, ip="10.0.1.1"):
        
        self.ip = ip
        self.port = 5672

        self.queueName = "hello"

        self.msgQueue = queue

        self.connected = False
        self.channel = None

    def createQueue(self):
        try:
            credentials = pika.PlainCredentials('firecamera', 'camerafire')
            parameters = pika.ConnectionParameters(self.ip, self.port,)# "/", credentials )
            connection = pika.BlockingConnection(parameters)
            self.channel = connection.channel()

            self.channel.queue_declare(queue = self.queueName, durable = True)

            self.connected = True
            return True
        except Exception as e:
            print(f"Error creating Queue - {e}")
            return False

    def sendData(self, data):
        try:
            if not self.connected or self.channel == None:
                return False
            
            self.channel.basic_publish(
                exchange = '',
                routing_key = 'hello',
                body = data
            )

            return True
        except Exception as e:
            print(f"Failed to send data - {e}")
            return False

    def receiveData(self):
        try:
            if not self.connected or self.channel == None:
                return

            self.channel.basic_qos(prefetch_count = 1)
            self.channel.basic_consume(
                queue = self.queueName, 
                on_message_callback = self.handleReceivedData
            )
            self.channel.start_consuming()
        except Exception as e:
            print(f"Failed to recieve Data - {e}")
            raise e

    def handleReceivedData(self, ch, method, properties, body):
        # print(f" [X] Data Received {body}")
        self.msgQueue.put(body)
        ch.basic_ack(delivery_tag = method.delivery_tag)


if __name__ == "__main__":
    r1 = RabbitMQ(ip="192.168.89.80")

    r1.createQueue()
    r1.sendData("Hello World - 0")
    time.sleep(1)
    msgToSend = 100

    for x in range(msgToSend):

        r1.sendData(f"ID - {x}")
        time.sleep(0.5)


    # r1.recieveData()
    # try:
    #     r1.recieveData()
    # except KeyboardInterrupt:
    #     print('Interrupted')
    #     try:
    #         sys.exit(0)
    #     except SystemExit:
    #         os._exit(0)