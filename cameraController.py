
import cv2
import time
import threading
from camera import Camera

class CameraController:

    def __init__(self, systemData):
        
        self.data = systemData

        self.camera = Camera()

        self.lastFrame = None
        self.threadLock = threading.Lock()

        self.running = True

    def bootupCamera(self):
        cameraBootupStatus = self.camera.bootup()
        self.data.cameraStatus = cameraBootupStatus

        return cameraBootupStatus
    
    def setRunning(self, status:bool):
        self.running = status

    def getFrame(self):
        with self.threadLock:
            if self.lastFrame is None:
                return None
            
            return self.lastFrame.copy()

    def getStreamData(self):
        if not self.camera.streamRunning:
            self.camera.startStream()
            time.sleep(0.2)

        streamCapture = cv2.VideoCapture(self.camera.streamLocation)
        #Possible Errors - cv2.error, AttributeError, TypeError

        while self.running:
            result, videoFrame = streamCapture.read()

            if result is False:
                break
            
            videoFrame = self.framePreProcessing(videoFrame)
            
            with self.threadLock:
                self.lastFrame = videoFrame

        streamCapture.release()

    def framePreProcessing(self, frame):
        newFrame = cv2.resize(frame, 256, 128)
        return newFrame