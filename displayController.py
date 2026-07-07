import time
from enum import Enum, auto
from turtle import Screen
import displayST7735 as Display

class Screens(Enum):
    VIEW = 0
    POS = auto()
    SENSORS = auto()
    SETTINGS = auto()
    SPLASH = auto()
    MAIN = auto()

class UserInput(Enum):
    UP = 1
    DOWN = auto()
    ENTER = auto()
    BACK = auto()

class DisplayController:

    def __init__(self, systemData):
        self.data = systemData
        
        self.display = Display.DisplayST7735()
        
        self.showMenu = False
        self.mainMenuIndex = 0
        self.maxMainMenuIndex = 4
        self.screen = Screens.SPLASH

        self.displayOn = True

    def showLogo(self):
        self.display.showLogo()

    def showBootStatus(self, data):
        self.display.showBootStatus(data)

    def showLogoSymbol(self):
        self.display.showLogoSymbol()

    def showMainMenu(self):
        self.display.showMainMenu(self.mainMenuIndex)

    def showSensor(self):
        self.display.showSensors(self.data)


    def setScreenView(self):
        self.screen = Screen.VIEW
    
    def setScreenPos(self):
        self.screen = Screen.POS

    def setScreenSensor(self):
        self.screen = Screen.SENSORS

    def setScreenSettings(self):
        self.screen = Screen.SETTINGS

    def setScreenSplash(self):
        self.screen = Screen.SPLASH

    def setScreenMain(self):
        self.screen = Screen.MAIN


    def startScreenLoop(self):
        while self.displayOn:
            try:
                self._showScreen()
            except NotImplementedError as e:
                print(f"Error - {e}")
                self.screen = Screens.MAIN  

    def _updateScreenIndex(self, menuIndexChange):
        if(not self.showMenu):
            return

        self.mainMenuIndex += menuIndexChange

        if(self.mainMenuIndex < 0):
            self.mainMenuIndex = self.maxMainMenuIndex

        if(self.mainMenuIndex > self.maxMainMenuIndex):
            self.mainMenuIndex = 0

    def _updateScreen(self):
        if(not self.showMenu):
            self.showMenu = True
            self.screen = Screens.MAIN
            return

        self.screen = Screens(self.mainMenuIndex)


    def _prevScreen(self):
        if(self.screen == Screens.MAIN):
            self.screen = Screens.SPLASH
            return

        self.screen = Screens.MAIN

    def _showScreen(self):
        match(self.screen):
            case Screens.SPLASH:
                self.showMenu = False  
                self.mainMenuIndex = 0
                self.showLogoSymbol()

            case Screens.MAIN:
                self.showMainMenu()

            case Screens.VIEW:
                raise NotImplementedError("View not implemented")

            case Screens.POS:
                raise NotImplementedError("Pos not implemented")

            case Screens.SENSORS:
                self.showSensor()

            case Screens.SETTINGS:
                raise NotImplementedError("Settings not implemented")

    def handleUserInput(self, input):
        userInput = UserInput(input)

        match(userInput):
            case UserInput.UP:
                self._updateScreenIndex(-1)

            case UserInput.DOWN:
                self._updateScreenIndex(1)

            case UserInput.ENTER:
                self._updateScreen()

            case UserInput.BACK:
                self._prevScreen()


if __name__ == "__main__":
    __init__() 