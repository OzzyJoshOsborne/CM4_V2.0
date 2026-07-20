import sys 
import pika
import json
import random
import datetime

def send(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue="hello", durable=True)#, arguments={'x-queue-type': 'quorum'})

    # message = ' '.join(sys.argv[1:]) or "Hello Workd!" 

    channel.basic_publish(
        exchange='', 
        routing_key='hello', 
        body=msg
    )

    print(f" [X] sent {msg}")
    connection.close()


def sendLoop():
    msgToSend = [1,2,3,4,5,6,7,8,9,10,11,12,13,20,21,23,40,41, 66]

    for x in msgToSend:

        # send(f"ID - {x}", random.randint(1,5))

        msg = json.dumps(
            {
                "uuid": "macAddress",
                "Type": x,
                "timestamp": datetime.datetime.now().timestamp(),
                "data": f"Test data for command - {x}"
            }
        )

        send(msg)
    

if __name__ == "__main__":
    # send()

    sendLoop()