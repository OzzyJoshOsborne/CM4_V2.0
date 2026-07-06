import time
import smbus2
import sensorBME688 as BME688
import sensorFS3000 as FS3000


class SensorData:
    
    def __init__(self):
        # BME688
        self.temperature = None
        self.pressure = None
        self.humidity = None

        #FS3000
        self.airFlowMps = None
        

class SensorController:

    def __init__(self, systemData):

        self.data = systemData

        self.BME688 = BME688.SensorBME688()
        self.FS3000 = FS3000.SensorFS3000()
        # Sensor IMU

        self.running = True

    def bootup(self):
        bme688Status = self.BME688.bootup()
        fs3000Status = self.FS3000.bootup()

        # self.chcekBME688()
        # self.checkFS3000()
        #Sensor IMU
        
        #Return boot up data back to main
        return [bme688Status, fs3000Status, False]

    def I2cDevicePresence(self, bus_number, address):
        try:
            with smbus2.SMBus(bus_number) as bus:
                bus.write_quick(address)
            return True
        except OSError:
            return False


    def chcekBME688(self):
        if self.I2cDevicePresence(1, 0x76):
            self.BME688 = BME688.SensorBME688()
            print("BME688 Sensor Present")
            return True
        else:
            # print("BME688 Sensor Not Found")
            return False

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
    
    def checkFS3000(self):
        if self.I2cDevicePresence(1, 0x28):
            self.FS3000 = FS3000.SensorFS3000()
            print("FS3000 Sensor Present")
            return True
        else:
            # print("FS3000 Sensor Not Found")
            return False

    def runFS3000(self):
        try:
            self.FS3000.getSensorData()
            
            data = self.FS3000.getData()

            self.data.airFlowMps = data

        except (RuntimeError, IOError) as e:
            print(f"FS3000 - {e}")
            self.FS3000.bootup()


    def printData(self):
        print("=======================")
        print(f"BM688 - Status: {"Active" if self.BME688.getConnectionStatus() else "Not Active"}")
        print(f"Temp - {self.data.temperature}")
        print(f"Pres - {self.data.pressure}")
        print(f"Humi - {self.data.humidity}")
        print("------------")
        print(f"FS3000 - Status: {"Active" if self.FS3000.getConnectionStatus() else "Not Active"}")
        print(f"Velo - {self.data.airFlowMps}")
        
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

                    
                    # self.printData()

                except (RuntimeError, IOError) as e:
                    pass

                time.sleep(1)
        except (RuntimeError, IOError) as e:
            self.connected = False


    def run(self):
        self.runSensors()


def __init__():
    p1 = SensorController()
    p1.bootup()

    # p1.start()
    p1.run()


if __name__ == "__main__":
    __init__() 
