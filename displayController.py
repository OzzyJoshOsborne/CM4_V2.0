import time
import displayST7735 as Display

class DisplayController:

    def __init__(self):
        
        self.display = Display.DisplayST7735()
        
        self.showMenu = False
        self.mainMenuIndex = 0
        self.maxMainMenuIndex = 4

    
    def showLogo(self):
        self.display.showLogo()

    def showBootStatus(self, data):
        self.display.showBootStatus(data)

    def showLogoSymbol(self):
        self.display.showLogoSymbol()

    def showMainMenu(self):
        self.display.showMainMenu(self.mainMenuIndex)



    def handleUserInput(self, input):
  
        if(input == 1):
            self.mainMenuIndex += 1
        elif(input == 2):
            self.mainMenuIndex -= 1
        elif(input == 3 or self.mainMenuIndex == self.maxMainMenuIndex):
            self.showMenu = not self.showMenu   

        if(self.mainMenuIndex < 0):
            self.mainMenuIndex = self.maxMainMenuIndex

        if(self.mainMenuIndex > self.maxMainMenuIndex):
            self.mainMenuIndex = 0

        if self.showMenu:
            self.showMainMenu()
        else:
            self.showLogoSymbol()



def __init__():
    d1 = DisplayController()

    # #Show logo
    # d1.showLogo()
    # time.sleep(1.0)

    # #"Bootup"
    # exampleBootSeq(d1)
    # time.sleep(.2)

    # #Show Logo 2
    # d1.showLogoSymbol()
    # time.sleep(1.0)

    #Menu
    d1.handleUserInput(0)


    #Wait for user input
    running = True
    while running:
        command = input()

        match command:
            case "1":
                d1.handleUserInput(1)

            case "2":
                d1.handleUserInput(2)

            case '':
                d1.handleUserInput(3)

            case "9":
                running = False


def exampleBootSeq(d1):
    bootStatus = {}

    timeDelay = .1
    
    bootStatus['Check-Network'] = {}
    d1.showBootStatus(bootStatus)
    time.sleep(timeDelay)

    bootStatus['Check-Network']["NO NETOWORK FOUND"] = 2
    d1.showBootStatus(bootStatus)
    time.sleep(timeDelay)


    bootStatus['Create-Message Send'] = {}
    d1.showBootStatus(bootStatus)
    time.sleep(timeDelay)

    bootStatus['Create-Message Send']["Queue Connected"] = 1
    d1.showBootStatus(bootStatus)
    time.sleep(timeDelay)


    bootStatus['Create-Message Receiver'] = {}
    d1.showBootStatus(bootStatus)
    time.sleep(timeDelay)

    bootStatus['Create-Message Receiver']["Queue Failed"] = 2
    d1.showBootStatus(bootStatus)
    time.sleep(timeDelay)


    bootStatus['Check-Camera Presence'] = {}
    d1.showBootStatus(bootStatus)
    time.sleep(timeDelay)

    bootStatus['Check-Camera Presence']["Camera Not Present"] = 2
    d1.showBootStatus(bootStatus)
    time.sleep(timeDelay)


    bootStatus['Check-Device Sensors'] = {}
    d1.showBootStatus(bootStatus)
    time.sleep(timeDelay)

    bootStatus['Check-Device Sensors']["IMU Sensor Not Found"] = 2
    d1.showBootStatus(bootStatus)
    time.sleep(timeDelay)

    bootStatus['Check-Device Sensors']["ACQ Sensor Present"] = 1
    d1.showBootStatus(bootStatus)
    time.sleep(timeDelay)

    bootStatus['Check-Device Sensors']["AVS Sensor Present"] = 1
    d1.showBootStatus(bootStatus)
    time.sleep(timeDelay)

if __name__ == "__main__":
    __init__() 