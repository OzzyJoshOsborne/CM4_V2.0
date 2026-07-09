
import time
import math
from tkinter import W
import smbus2

import board
import busio

from adafruit_bno08x import(
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
)
from adafruit_bno08x.i2c import BNO08X_I2C

class Data:
    def __init__(self):
        self.yaw = None
        self.pitch = None
        self.roll = None

class SensorBNO086:

    def __init__(self):
        #Address
        self.sensorAddress = 0x4B

        self.data = Data()

        self.connected = False

    def bootup(self):
        self.checkConnection()
        if(self.connected):
            try:
                self.i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
                self.bno = BNO08X_I2C(self.i2c, address=0x4B)

                self.bno.enable_feature(BNO_REPORT_ACCELEROMETER)
                self.bno.enable_feature(BNO_REPORT_GYROSCOPE)
                self.bno.enable_feature(BNO_REPORT_MAGNETOMETER)
                self.bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

                return True
            
            except OSError as e:
                print(f"Error booting up BNO086 Sensor - {e}")
        return False

    def _isConnected(self, busNum):
        try: 
            with smbus2.SMBus(busNum) as bus:
                bus.write_quick(self.sensorAddress)
            return True
        except OSError:
            return False

    def checkConnection(self):
        self.connected = self._isConnected(1)
        return self.connected

    def getConnectionStatus(self):
        return self.connected


    def _calucateEulerAngles(self, w, x, y, z):
        #Make sure Quaternion is (w, x, y, z) / (real, i, j, k)
        #Yaw = atan2(2(wz + xy), 1 - 2(y^2 + z^2))
        y1 = w * z
        y2 = x * y
        yaw = math.atan2(2(y1 + y2), 1 - 2(y^2 + z^2))
        
        #Pitch = asin(2(wy - zx))
        p1 = w * z
        p2 = z * x
        pitch = math.asin(2 * (p1 - p2))

        #Roll = atan2(2(wx + yz), 1 - 2(x^2 + y^2))
        r1 = w * x
        r2 = y * z
        roll = math.atan2(2(r1 + r2), 1 - 2(x^2 + y^2))

        return yaw, pitch, roll
        

    def getSensorData(self):
        if self.connected:
            
            # print("Rotation Vector Quaternion:")
            quat_i, quat_j, quat_k, quat_real = self.bno.quaternion
            # print("I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat_i, quat_j, quat_k, quat_real))
            yaw, pitch, roll = self._calucateEulerAngles(quat_real, quat_i, quat_j, quat_k)
            # print(f"Yaw - {yaw} - Pitch - {pitch} - Roll - {roll}")

            self.data.yaw = yaw
            self.data.pitch = pitch
            self.data.roll = roll

            return True
        else:
            return False

    def getData(self):
        return self.data

    def printSensorData(self):
        pass

    def run(self):
        try:
            while True:
                self.getSensorData()

                self.printSensorData()
                time.sleep(0.2)

        except OSError as e:
            print(f"Error Reading from sensor BNO086 - {e}")
            return None
        
def __init__():
    bno = SensorBNO086()
    bno.bootup()
    bno.run()

if __name__ == "__main__":
    __init__()