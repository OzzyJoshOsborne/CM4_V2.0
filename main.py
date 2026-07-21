
import time
from datetime import datetime
import threading

import sys
import termios
import tty

import lib.systemData as SystemData
import lib.display.displayController as Display
import lib.sensors.sensorController as Sensors
import lib.camera.cameraController as Camera
import lib.rabbit.rabbitMQController as Rabbit

class Main:
    def __init__(self):
        #Init System Data
        self.systemData = SystemData.SystemData()

        #Core
        self.rabbitController = Rabbit.RabbitMQController()
        self.cameraController = Camera.CameraController(self.systemData)
        self.sensorsController = Sensors.SensorController(self.systemData)

        self.displayController = Display.DisplayController(self.systemData, self.cameraController)

        self.bootup()

        self.startControllers()

        self.mainLoop()


    def bootup(self):
        bootStatus = {}

        self.displayController.showLogo()
        time.sleep(0.1)

        timeDelay = .1

        #Check Network
        bootStatus['Check-Network'] = {}
        bootStatus['Check-Network']["NO NETOWORK FOUND"] = 2
        self.displayController.showBootStatus(bootStatus)
        time.sleep(timeDelay)

        # #Rabbit 1
        # bootStatus['Create-Message Send'] = {}
        # bootStatus['Create-Message Send']["Queue Failed"] = 2
        # self.display.showBootStatus(bootStatus)
        # time.sleep(timeDelay)

        # #Rabbit 2
        # bootStatus['Create-Message Receiver'] = {}
        # bootStatus['Create-Message Receiver']["Queue Failed"] = 2
        # self.display.showBootStatus(bootStatus)
        # time.sleep(timeDelay)

        bootStatus['Create-Message RabbitMQ'] = {}
        self.displayController.showBootStatus(bootStatus)

        self.rabbitController.bootupRabbit()

        msg = ""
        if self.rabbitController.rabbitStatus:
            msg += "Queue Success"
        else:
            msg += "Queue Failed"

        bootStatus['Create-Message RabbitMQ'][msg] = 1 if self.rabbitController.rabbitStatus else 2
        self.displayController.showBootStatus(bootStatus)


        #Camera
        bootStatus['Check-Camera Presence'] = {}
        self.displayController.showBootStatus(bootStatus)

        self.cameraController.bootupCamera()
        msg = ""
        if self.systemData.cameraStatus:
            msg += "Camera Present"
        else:
            msg += "Camera Not Present"

        bootStatus['Check-Camera Presence'][msg] = 1 if self.systemData.cameraStatus else 2
        self.displayController.showBootStatus(bootStatus)


        #Sensors
        bootStatus['Check-Device Sensors'] = {}
        self.displayController.showBootStatus(bootStatus)

        sensorResults = threading.Thread(target = self.sensorsController.bootup, daemon = True)
        sensorResults.start()

        sensorsBooting = True

        while sensorsBooting:
            if self.systemData.BME688Status is not None:
                msg = 'ACQ'
                if self.systemData.BME688Status:
                    msg += " Sensor Present"
                else:
                    msg += " Sensor Not Found"
                bootStatus['Check-Device Sensors'][msg] = 1 if self.systemData.BME688Status else 2
                self.displayController.showBootStatus(bootStatus)

            if self.systemData.FS3000Status is not None:
                msg = 'AVS'
                if self.systemData.FS3000Status:
                    msg += " Sensor Present"
                else:
                    msg += " Sensor Not Found"
                bootStatus['Check-Device Sensors'][msg] = 1 if self.systemData.FS3000Status else 2
                self.displayController.showBootStatus(bootStatus)

            if self.systemData.BNO086Status is not None:
                msg = 'IMU'
                if self.systemData.BNO086Status:
                    msg += " Sensor Present"
                else:
                    msg += " Sensor Not Found"
                bootStatus['Check-Device Sensors'][msg] = 1 if self.systemData.BNO086Status else 2
                self.displayController.showBootStatus(bootStatus)

            if self.systemData.BME688Status is not None and self.systemData.FS3000Status is not None and self.systemData.BNO086Status is not None:
                sensorsBooting = False

        sensorResults.join()

    def startControllers(self):
        self.rabbitController.run()

        self.sensorsController.run()

        self.cameraController.run()

        time.sleep(0.1)

        self.displayThread = threading.Thread(target = self.displayController.startScreenLoop, daemon = True)
        self.displayThread.start()

        self.startHeartbeatThread()

    def sendHeartBeat(self):
        while True:
            heartbeatMsg = {
                "type": "heartbeat",
                "time": datetime.now()
            }

            commandNum = 0

            self.rabbitController.sendData(commandNum, "heartbeatMsg")
            time.sleep(2)

    def startHeartbeatThread(self):
        self.heartBeatThread = threading.Thread(target = self.sendHeartBeat, daemon = True)
        self.heartBeatThread.start()

    def getKeyPress(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)

            if ch == '\x1b':
                # Escape sequence
                next1 = sys.stdin.read(1)
                if next1 == '[':
                    next2 = sys.stdin.read(1)
                    return ch + next1 + next2
                return 'ESC'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if ord(ch) == 3: quit()
        return ch

    def mainLoop(self):
        running = True
        while running:

            # command = input()
            
            key = self.getKeyPress()

            print(key)

            if key == "\x1b[A":# Up
                self.displayController.handleUserInput(1)

            elif key == "\x1b[B": # Down
                self.displayController.handleUserInput(2)

            elif key == "\x1b[C": # Right
                self.displayController.handleUserInput(3)

            elif key == "\x1b[D": # Left
                self.displayController.handleUserInput(4)

            elif key == "\r": # Enter
                self.displayController.handleUserInput(3)

            elif key == "m":
                self.cameraController.toggleIFMode()


if __name__ == '__main__':
    main = Main()