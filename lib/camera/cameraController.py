
import cv2
import time
import threading
from lib.camera.camera import Camera

class CameraController:

    def __init__(self, systemData):
        
        self.data = systemData

        self.camera = Camera()

        self.lastFrame = None
        self.getStreamThread = None
        self.threadLock = threading.Lock()

        self.IFMode = False

        self.running = True

    def bootupCamera(self):
        cameraBootupStatus = self.camera.bootup()
        self.data.cameraStatus = cameraBootupStatus

        return cameraBootupStatus

    def toggleIFMode(self):
        self.IFMode = not self.IFMode 

    def setRunning(self, status:bool):
        self.running = status

    def getFrame(self):
        with self.threadLock:
            if self.lastFrame is None:
                return None
            
            return self.lastFrame.copy()

    def getStreamData(self):
        if not self.camera.streamRunning:
            return
        
        try:
            streamCapture = cv2.VideoCapture(self.camera.streamLocation)
            #Possible Errors - cv2.error, AttributeError, TypeError

            while self.running:
                result, videoFrame = streamCapture.read()

                if result is False:
                    break
                
                processedFrame = self.framePreProcessing(videoFrame)
                
                with self.threadLock:
                    self.lastFrame = processedFrame

            streamCapture.release()
        except (cv2.error, AttributeError, TypeError) as e:
            print(f"Exception while video Capture - {e}")
            streamCapture.release()

    def framePreProcessing(self, frame):
        # print(frame.shape)
        newFrame = cv2.resize(frame, (256, 128))

        if self.IFMode:
            cropimg = newFrame[0:128,128:256, :]
            coling = cv2.applyColorMap(cropimg, cv2.COLORMAP_JET)
            colorImg = cv2.cvtColor(coling, cv2.COLOR_BGR2RGB)
            return colorImg
        else:
            cropimg = newFrame[0:128,0:128, :]
            colorImg = cv2.cvtColor(cropimg, cv2.COLOR_BGR2RGB)
            return colorImg
    
    def checkStreamStatus(self):
        if not self.camera.streamRunning():
            self.bootupCamera()
        #TODO: Add safty net, if ran X times break and report error to user - something wrong with camera.

    def run(self):
        #Check Stream status
        if not self.camera.streamRunning:
            self.bootupCamera()

        self.getStreamThread = threading.Thread(target = self.getStreamData , daemon = True)
        self.getStreamThread.start()





def __init__():
    c1 = CameraController()
    c1.run()


if __name__ == "__main__":
    __init__()