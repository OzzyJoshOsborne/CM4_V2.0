
import os
import sys
import time
import pika

class RabbitMQ:

    def __init__(self, ip="10.0.1.1"):
        
        self.ip = ip
        self.port = 5672

        self.queueName = "hello"

    def createQueue(self):
        credentials = pika.PlainCredentials('firecamera', 'camerafire')
        parameters = pika.ConnectionParameters(self.ip, self.port,)# "/", credentials )
        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()

        self.channel.queue_declare(queue = self.queueName, durable = True)

    def sendData(self, data):
        self.channel.basic_publish(
            exchange = '',
            routing_key = 'hello',
            body = data
        )

    def recieveData(self):
        self.channel.basic_qos(prefetch_count = 1)
        self.channel.basic_consume(
            queue = self.queueName, 
            on_message_callback = self.handleRecievedData
        )
        self.channel.start_consuming()

    def handleRecievedData(self, ch, method, properties, body):
        print(f" [X] Data Received {body}")
        ch.basic_ack(delivery_tag = method.delivery_tag)


if __name__ == "__main__":
    r1 = RabbitMQ(ip="192.168.89.80")

    r1.createQueue()
    r1.sendData("Hello World - 0")
    time.sleep(1)
    # r1.recieveData()
    try:
        r1.recieveData()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)