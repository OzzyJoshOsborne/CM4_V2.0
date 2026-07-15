from sys import exception

import cv2
import time
import subprocess

class Camera:

    def __init__(self):
        
        self.connected = False

    def bootup(self):
        self.checkConnection()
        if self.connected:

            #Check Stream is running
            if self.checkStreamRunning():
                self.endStream()
                time.sleep(0.2)

            self.startStream()

            return True
        else:
            return False        

    def _isConnected(self):
        try:
            result = subprocess.run(
                ["v4l2-ctl", "--list-devices"],
                capture_output=True, 
                text=True
            )
            # print(result)
            devices = {}
            currentDevices = None

            for line in result.stdout.splitlines():
                line = line.rstrip()

                if line and not line.startswith("\t"):
                    currentDevices = line.rstrip(":")
                    devices[currentDevices] = []

                elif line.startswith("\t"):
                    path = line.strip()
                    devices[currentDevices].append(path)

            foundDevice = False

            for d_key in devices:
                if "3D" in d_key:
                    foundDevices = True
                    if len(devices[d_key]) >= 3:
                        foundDevice = True

            return foundDevice
        except Exception as e:
            print(f"Error while checking if camera is connected - {e}")
            return False

    def checkConnection(self):
        self.connected = self._isConnected()
        return self.connected
    

    def checkStreamRunning(self):
        try:
            result = subprocess.run(
                ["pgrep", "-f", "mjpg_streamer"], 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error while trying to check if stream is running - {e}")
            raise Exception("Failed to check if stream is running")

    def createCommand(self):
        mjpgLocation = "/usr/local/bin/mjpg_streamer"

        devicesInput = "/usr/local/lib/mjpg-streamer/input_uvc.so"
        fps = "10"
        res = "2560x720"
        timeout = "15"
        #Quality

        streamOutput = "/usr/local/lib/mjpg-streamer/output_http.so"
        port = "8085"
        webRoot = "/usr/local/share/mjpg-streamer/www"

        inputCommand = devicesInput + " -n" + " -f " + fps + " -r " + res + " -timeout " + timeout
        outputCommand = streamOutput + " -p " + port + " -w " + webRoot

        print(inputCommand)
        print(outputCommand)

        command = [
            mjpgLocation,
            "-i", inputCommand,
            "-o", outputCommand,
        ]

        return command

    def startStream(self):
        try:
            command = self.createCommand()

            process = subprocess.Popen(command)
        
            return process.returncode == 0
        except FileNotFoundError as e:
            print(e)
            return None

    def endStream(self):
        try:
            result = subprocess.run(
                ["pkill", "-f", "mjpg_streamer"], 
                capture_output=True
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error while trying to close the stream - {e}")
            raise Exception("Failed to close the stream")

    def run(self):
        status = self.bootup()

        time.sleep(0.2)

        if(status):
            video_capture = cv2.VideoCapture("http://127.0.0.1:8085/?action=stream")

            while True:
                result, video_frame = video_capture.read()
                if result is False:
                    break

                cv2.imshow(
                    "USB Camera Test", video_frame
                )

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            
            video_capture.release()
            cv2.destroyAllWindows()


def __init__():
    c1 = Camera()
    c1.run()


if __name__ == "__main__":
    __init__()