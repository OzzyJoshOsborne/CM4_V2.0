import os
import sys
import time
import pika

def recieve():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue="hello", durable=True, arguments={'x-queue-type': 'quorum'})

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="hello", auto_ack=False, on_message_callback = callback)

    print(' [*] Waiting for message. To exit press CTRL+C')
    channel.start_consuming()

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    time.sleep(body.count(b'.'))
    print(" [X] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)


if __name__ == "__main__":
    try:
        recieve()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
