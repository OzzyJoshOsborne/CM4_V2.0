import time
import threading

import sys
import termios
import tty

import systemData as SystemData
import displayController as Display
import sensorController as Sensors

class Main:
    def __init__(self):
        #Init System Data
        self.systemData = SystemData.SystemData()

        self.display = Display.DisplayController(self.systemData)
        #Core
        #Rabbit
        #Camera
        self.sensors = Sensors.SensorController(self.systemData)

        self.bootup()

        self.mainLoop()


    def bootup(self):
        bootStatus = {}

        self.display.showLogo()
        time.sleep(0.1)

        timeDelay = .1

        #Check Network
        bootStatus['Check-Network'] = {}
        bootStatus['Check-Network']["NO NETOWORK FOUND"] = 2
        self.display.showBootStatus(bootStatus)
        time.sleep(timeDelay)

        #Rabbit 1
        bootStatus['Create-Message Send'] = {}
        bootStatus['Create-Message Send']["Queue Failed"] = 2
        self.display.showBootStatus(bootStatus)
        time.sleep(timeDelay)

        #Rabbit 2
        bootStatus['Create-Message Receiver'] = {}
        bootStatus['Create-Message Receiver']["Queue Failed"] = 2
        self.display.showBootStatus(bootStatus)
        time.sleep(timeDelay)

        #Camera
        bootStatus['Check-Camera Presence'] = {}
        bootStatus['Check-Camera Presence']["Camera Not Present"] = 2
        self.display.showBootStatus(bootStatus)
        time.sleep(timeDelay)

        #Sensors
        bootStatus['Check-Device Sensors'] = {}
        self.display.showBootStatus(bootStatus)

        sensorResults = threading.Thread(target = self.sensors.bootup, daemon = True)
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
                self.display.showBootStatus(bootStatus)

            if self.systemData.FS3000Status is not None:
                msg = 'AVS'
                if self.systemData.FS3000Status:
                    msg += " Sensor Present"
                else:
                    msg += " Sensor Not Found"
                bootStatus['Check-Device Sensors'][msg] = 1 if self.systemData.FS3000Status else 2
                self.display.showBootStatus(bootStatus)

            if self.systemData.BNO086Status is not None:
                msg = 'IMU'
                if self.systemData.BNO086Status:
                    msg += " Sensor Present"
                else:
                    msg += " Sensor Not Found"
                bootStatus['Check-Device Sensors'][msg] = 1 if self.systemData.BNO086Status else 2
                self.display.showBootStatus(bootStatus)

            if self.systemData.BME688Status is not None and self.systemData.FS3000Status is not None and self.systemData.BNO086Status is not None:
                sensorsBooting = False


        self.sensorsThread = threading.Thread(target = self.sensors.runSensors, daemon = True)
        self.sensorsThread.start()

        time.sleep(0.1)

        self.displayThread = threading.Thread(target = self.display.startScreenLoop, daemon = True)
        self.displayThread.start()

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

            if key == "\x1b[A":# Up
                self.display.handleUserInput(1)

            elif key == "\x1b[B": # Down
                self.display.handleUserInput(2)

            elif key == "\x1b[C": # Right
                self.display.handleUserInput(3)

            elif key == "\x1b[D": # Left
                self.display.handleUserInput(4)

            elif key == "\r": # Enter
                self.display.handleUserInput(3)


if __name__ == '__main__':
    main = Main()