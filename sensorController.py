import time
import smbus2
import sensorBME688 as BME688


class SensorData:
    
    def __init__(self):
        self.temperature = None
        self.pressure = None
        self.humidity = None

class SensorController:

    def __init__(self):
        self.data = SensorData()

        self.BME688 = None
        # Sensor FS3000
        # Sensor IMU

        self.bootup()

        self.running = True

    def bootup(self):
        self.chcekBME688()
        #Sensor FS3000
        #Sensor IMU

    def chcekBME688(self):
        if self.I2cDevicePresence(1, 0x76):
            self.BME688 = BME688.SensorBME688()
            print("BME688 Sensor Present")
            return True
        else:
            print("BME688 Sensor Not Found")
            return False


    def I2cDevicePresence(self, bus_number, address):
        try:
            with smbus2.SMBus(bus_number) as bus:
                bus.write_quick(address)
            return True
        except OSError:
            return False


    def runSensorBM688(self):
        try:
            self.BME688.getSensorData()
            
            data = self.BME688.getData()
            
            self.data.temperature = data.temperature
            self.data.pressure = data.pressure
            self.data.humidity = data.humidity

            print("================================")
            print(data.temperature)
            print(data.pressure)
            print(data.humidity)

        except (RuntimeError, IOError) as e:
            # self.connected = False
            self.BME688 = None
            pass

    def runSensors(self):
        try:
            while self.running: 
                try:
                    if self.BME688 is not None:
                        self.runSensorBM688()
                    else:
                        self.chcekBME688()

                except (RuntimeError, IOError) as e:
                    pass

                time.sleep(1)
        except (RuntimeError, IOError) as e:
            self.connected = False


    def run(self):
        self.runSensors()


def __init__():
    p1 = SensorController()
    # p1.start()
    p1.run()


if __name__ == "__main__":
    __init__() 
