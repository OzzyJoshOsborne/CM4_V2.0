import time
import threading
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

        sensorResults = self.sensors.bootup()
        sensorList = ["IMU", "ACQ", "AVS"]
        for idx, sensor in enumerate(sensorResults):
            msg = sensorList[idx]
            if sensor:
                msg += " Sensor Present"
            else:
                msg += " Sensor Not Found"
            bootStatus['Check-Device Sensors'][msg] = 1 if sensor else 2
            self.display.showBootStatus(bootStatus)
            time.sleep(timeDelay)

        self.sensorsThread = threading.Thread(target = self.sensors.runSensors, daemon=True)
        self.sensorsThread.start()

        time.sleep(0.1)

        self.display.showSensor()

    def mainLoop(self):
        running = True
        while running:
            command = input()

            match command:
                case "1":
                    self.display.handleUserInput(1)

                case "2":
                    self.display.handleUserInput(2)

                case '':
                    self.display.handleUserInput(3)

                case "9":
                    running = False


if __name__ == '__main__':
    main = Main()