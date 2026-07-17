import time
import threading
from rabbitMQ import RabbitMQ

class RabbitMQController:

    def __init__(self):
        
        self.rabbit = RabbitMQ(ip="192.168.89.80")
        self.rabbitStatus = False

        self.reconnectTimerSeconds = 5 

        self.running = True

    def bootupRabbit(self):
        self.rabbitStatus = self.rabbit.createQueue()

    def sendData(self):
        pass

    def receiveData(self):
        while self.running:
            if self.rabbitStatus is False:
                self.reconnectRabbit()
                continue

            try:
                self.rabbit.receiveData()

            except Exception as e:
                print(e)
                self.rabbitStatus = False

    def reconnectRabbit(self):
        self.bootupRabbit()
        print(f"Trynig reconnect - {self.rabbitStatus}")
        if self.rabbitStatus:
            return
        else:
            time.sleep(self.reconnectTimerSeconds)

    def run(self):
        self.rabbitReciveThread = threading.Thread(target = self.receiveData, daemon = True)
        self.rabbitReciveThread.start()


if __name__ == "__main__":
    r1 = RabbitMQController()
    r1.bootupRabbit()
    r1.run()

    while True:
        pass
