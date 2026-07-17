import sys 
import pika
import random

def send(msg, time):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue="hello", durable=True)#, arguments={'x-queue-type': 'quorum'})

    # message = ' '.join(sys.argv[1:]) or "Hello Workd!" 
    message = msg
    for x in range(time):
        message += "."

    channel.basic_publish(
        exchange='', 
        routing_key='hello', 
        body=message
    )

    print(f" [X] sent {message}")
    connection.close()


def sendLoop():
    msgToSend = 12

    for x in range(msgToSend):

        send(f"ID - {x}", random.randint(1,5))
    

if __name__ == "__main__":
    # send()

    sendLoop()