import time
import sensorBME688 as BME688
import sensorFS3000 as FS3000
import sensorBNO086 as BNO086

class SensorController:

    def __init__(self, systemData):

        self.data = systemData

        self.BME688 = BME688.SensorBME688()
        self.FS3000 = FS3000.SensorFS3000()
        self.BNO086 = BNO086.SensorBNO086()

        self.running = True

    def bootup(self):
        self.data.BME688Status = self.BME688.bootup()
        self.data.FS3000Status = self.FS3000.bootup()
        self.data.BNO086Status = self.BNO086.bootup()

        return True


    def runBM688(self):
        try:
            #Add check if get sensor data worked
            self.BME688.getSensorData()
            
            data = self.BME688.getData()
            
            self.data.temperature = data.temperature
            self.data.pressure = data.pressure
            self.data.humidity = data.humidity

        except (RuntimeError, IOError) as e:
            # self.connected = False
            print(f"BM688 Error - {e}")
            self.BME688.bootup()
    
    def runFS3000(self):
        try:
            self.FS3000.getSensorData()
            
            data = self.FS3000.getData()

            self.data.airFlowMps = data

        except (RuntimeError, IOError) as e:
            print(f"FS3000 - {e}")
            self.FS3000.bootup()

    def runBNO086(self):
        try:
            self.BNO086.getSensorData()

            data = self.BNO086.getData()
            
            self.data.yaw = data.yaw
            self.data.pitch = data.pitch
            self.data.roll = data.roll

        except (RuntimeError, IOError) as e:
            print(f"BNO086 - {e}")
            self.BNO086.bootup()

    def printData(self):
        print("=======================")
        print(f"BM688 - Status: {"Active" if self.BME688.getConnectionStatus() else "Not Active"}")
        print(f"Temp - {self.data.temperature} - Pres - {self.data.pressure} - Humi - {self.data.humidity}")
        print("------------")
        print(f"FS3000 - Status: {"Active" if self.FS3000.getConnectionStatus() else "Not Active"}")
        print(f"Velo - {self.data.airFlowMps}")
        print("------------")
        print(f"FS3000 - Status: {"Active" if self.FS3000.getConnectionStatus() else "Not Active"}")
        print(f"Yaw - {self.data.yaw} - Pitch - {self.data.pitch} - Roll - {self.data.roll}")
        print("=======================")
        
    def runSensors(self):
        try:
            while self.running: 
                try:
                    if self.BME688.getConnectionStatus():
                        self.runBM688()
                    else:
                        self.BME688.bootup()

                    if self.FS3000.getConnectionStatus():
                        self.runFS3000()
                    else:
                        self.FS3000.bootup()

                    
                    if self.BNO086.getConnectionStatus():
                        self.runBNO086()
                    else:
                        self.BNO086.bootup()

                except (RuntimeError, IOError) as e:
                    pass

                time.sleep(1)
        except (RuntimeError, IOError) as e:
            self.running = False


    def run(self):
        self.runSensors()


def __init__():
    p1 = SensorController()
    p1.bootup()

    # p1.start()
    p1.run()


if __name__ == "__main__":
    __init__() 
