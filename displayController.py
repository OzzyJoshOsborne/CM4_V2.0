import time
from enum import Enum, auto
import displayST7735 as Display

class Screens(Enum):
    MAIN = 0
    VIEW = auto()
    POS = auto()
    SENSORS = auto()
    SETTINGS = auto()
    SPLASH = auto()



class DisplayController:

    def __init__(self):
        
        self.display = Display.DisplayST7735()
        
        self.showMenu = False
        self.mainMenuIndex = 0
        self.maxMainMenuIndex = 4
        self.screen = Screens.SPLASH

    def showLogo(self):
        self.display.showLogo()

    def showBootStatus(self, data):
        self.display.showBootStatus(data)

    def showLogoSymbol(self):
        self.display.showLogoSymbol()

    def showMainMenu(self):
        self.display.showMainMenu(self.mainMenuIndex)


    def showScreen(self):
        match(self.screen):
            case Screens.MAIN:
                pass

            case Screens.VIEW:
                pass

            case Screens.POS:
                pass


    def _updateScreenIndex(self, menuIndexChange):
        if(not self.showMenu):
            return

        self.mainMenuIndex += menuIndexChange

        if(self.mainMenuIndex < 0):
            self.mainMenuIndex = self.maxMainMenuIndex

        if(self.mainMenuIndex > self.maxMainMenuIndex):
            self.mainMenuIndex = 0

    def _updateScreen(self):
        #If on main screen, show main menu
        if(not self.showMenu):
            self.showMenu = True
            return

        # print(self.screen)
        # print("---")
        # for sc in Screens:
        #     print(sc)
        #     print(sc.name)
        #     print(sc.value)

        print(Screens(self.mainMenuIndex).name)
        
        match(self.mainMenuIndex):
            case 0:
                print("To Implement - View Image")
            case 1:
                print("To Implement - Camera Pos")
            case 2:
                print("To Implement - Sensors")
            case 3: 
                print("To Implement - Settings")
            case 4:
              self.showMenu = False  
              self.mainMenuIndex = 0


        #If on index X do Y 

    def handleUserInput(self, input):
        print(input)

        if(input == 1):
            self._updateScreenIndex(1)

        elif(input == 2):
            self._updateScreenIndex(-1)

        elif(input == 3):
            self._updateScreen()

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