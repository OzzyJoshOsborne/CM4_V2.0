import os
import time
import math
import digitalio
import board
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7735

BAUDRATE = 24000000

class DisplayST7735:
    
    #Colors
    COLOR_WHITE = (255, 255, 255)
    COLOR_RED = (255, 0 , 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_ORANGE = (255, 127, 0)

    FONT = cv2.FONT_HERSHEY_SIMPLEX


    def __init__(self):

        self.width = self.height = 128
        
        self.bootup()


    def bootup(self):
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = digitalio.DigitalInOut(board.D24)

        xOffset = 2
        yOffset = 3
        rotate = 180

        spi = board.SPI()

        self.disp = st7735.ST7735R(spi, dc_pin, cs_pin, reset_pin, 128, 128, BAUDRATE, x_offset = xOffset, y_offset = yOffset, rotation = rotate)

        self._loadImages()

        self._showBlackScreen()

    def _loadImages(self):
        #Loads all images from display_images into self.images, using the file name as the image key
        self.imageDir = r'display_images'
        self.images = {}
        
        for file in os.listdir(self.imageDir):
            imageName = file.split(".")[0]
            imagePath = os.path.join(self.imageDir, file)

            image = cv2.imread(imagePath,cv2.IMREAD_COLOR)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
            self.images[imageName] = cv2.resize(image, (128, 128))

    def _updateDisplay(self, frame):
        self.disp.image(frame)

    def _addText(self, img, txt, x, y, color):
        cv2.putText(img, txt, (x, y), self.FONT, .3, color, 1)

        return img

    def _getTextSize(self, txt):
        return cv2.getTextSize(txt, self.FONT, .3, 1)

    def _addLogo(self, img):
        offset = 0
        logoSize = 32

        logo = self.images["FCL240"].copy()
        logo = cv2.resize(logo, (logoSize, logoSize))
        img[offset: offset+logoSize, self.width - offset - logoSize: self.width - offset] = logo

    def _addLogoText(self, img):
        offset = 10
        logoSize = 128

        logo = self.images["FCLW"].copy()
        logo_h, logo_w, _ = logo.shape

        #Crop Image
        crop_y = 55
        crop_h = 22
        logo = logo[crop_y:crop_y+crop_h, 0:logo_w]

        #Top Left
        x1 = 0
        y1 = 10

        #Bottom Right
        x2 = x1 + logo_w
        y2 = y1 + crop_h

        # img[offset: offset+logoSize, self.width - offset - logoSize: self.width - offset] = logo
        img[y1: y2, x1: x2] = logo

    def _showBlackScreen(self):
        img = np.zeros((self.width, self.height, 4), dtype=np.uint8)
        newFrame = Image.fromarray(img)
        self._updateDisplay(newFrame)

    def showLogo(self):
        newFrame = Image.fromarray(self.images["FCLW"])
        self._updateDisplay(newFrame)

    def showLogoSymbol(self):
        newFrame = Image.fromarray(self.images["FCL240"])
        self._updateDisplay(newFrame)

    def showBootStatus(self, bootStatus):
        img = np.zeros((self.width, self.height, 3), dtype=np.uint8)
        yPos = 10
        
        for subsystem in bootStatus:
            cv2.putText(img, subsystem, (5, yPos), self.FONT, 0.3, self.COLOR_WHITE, 1)
            yPos += 10

            for system in bootStatus[subsystem]:

                color = self.COLOR_WHITE
                match bootStatus[subsystem][system]:
                    case 1: 
                        color = self.COLOR_GREEN
                    case 2:
                        color = self.COLOR_RED

                cv2.putText(img, system, (15, yPos), self.FONT, 0.3, color, 1)
                yPos += 10

        newFrame = Image.fromarray(img)
        self._updateDisplay(newFrame)

    def showMainMenuAnimation(self):
        pass

    def showMainMenu(self, index):
        img = np.zeros((self.width, self.height, 4), dtype=np.uint8)

        # Logo
        self._addLogo(img)

        # Options
        menuOptions = ["View Image", "Camera Pos", "Sensors", "Settings", "Main Screen"]

        menuStart_y = 35
        offset = 18

        for idx, option in enumerate(menuOptions):
            x = int(self.width / 2) - int(self._getTextSize(option)[0][0] / 2)

            color = self.COLOR_WHITE

            #Selected Option
            if(idx == index):
                color = self.COLOR_ORANGE

            self._addText(img, option, x, menuStart_y + (offset * idx), color)

        newFrame = Image.fromarray(img)
        self._updateDisplay(newFrame)


    def showCameraError(self):
        img = np.zeros((self.width, self.height, 4), dtype=np.uint8)

        #Add Logo
        self._addLogoText(img)

        x_offset = 25
        y1 = 50
        y2 = 120

        cv2.line(img, (x_offset, y1), (self.width - x_offset, y2), (255, 0, 0), 8)
        cv2.line(img, (x_offset, y2), (self.width - x_offset, y1), (255, 0, 0), 8)

        newFrame = Image.fromarray(img)
        self._updateDisplay(newFrame)


    def showCamera(self, frame):
        self._updateDisplay(frame)

    def showCameraPos(self, data):
        yaw = data.yaw  * 180.0 / math.pi
        if yaw < 0:
            yaw += 360
        patch = data.pitch * 180.0 / math.pi
        if patch < 0:
            patch += 360
        roll = data.roll * 180.0 / math.pi
        if roll < 0:    
            roll += 360

        img = np.zeros((self.width, self.height, 4), dtype=np.uint8)

        sensors = [ "Yaw",
                    str(yaw),
                    "Pitch", 
                    str(patch), 
                    "Roll",
                    str(roll)
                ]

        menuStart_y = 10
        offset = 16

        for idx, sensor in enumerate(sensors):
            x = int(self.width / 2) - int(self._getTextSize(sensor)[0][0] / 2)
            color = self.COLOR_WHITE

            self._addText(img, sensor, x, menuStart_y + (offset * idx), color)

        newFrame = Image.fromarray(img)
        self._updateDisplay(newFrame)

    def showSensors(self, data):
        img = np.zeros((self.width, self.height, 4), dtype=np.uint8)

        # Logo
        # self._addLogo(img)

        sensors = ["System Temperature",
                    str(data.temperature),
                    "Air Pressure",
                    str(data.pressure),
                    "Air Humidity",
                    str(data.humidity),
                    "Air Flow",
                    str(data.airFlowMps)
                ]

        menuStart_y = 10
        offset = 16

        for idx, sensor in enumerate(sensors):
            x = int(self.width / 2) - int(self._getTextSize(sensor)[0][0] / 2)
            color = self.COLOR_WHITE

            self._addText(img, sensor, x, menuStart_y + (offset * idx), color)

        newFrame = Image.fromarray(img)
        self._updateDisplay(newFrame)


    def showSettings(self):
        pass

    def showLoading(self):
        pass

    def showOffline(self):
        pass

    

    def test(self):
        # pass
        # self.showLogo()
        # time.sleep(1.0)
        # self.showLogoSymbol()
        # time.sleep(1.0)
        # self.exampleBootSeq()
        self.showCameraPos()


def __init__():
    p1 = DisplayST7735()
    # p1.start()
    p1.test()


if __name__ == "__main__":
    __init__() 