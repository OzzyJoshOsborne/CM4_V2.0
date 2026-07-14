import time
import smbus2

class SensorFS3000:

    def __init__(self):
        #Address
        self.sensorAddress = 0x28
        
        self.rawData = None
        self.mpsData = None

        #Define data points
        self.mpsDataPoints = [0, 1.07, 2.01, 3.00, 3.97, 4.96, 5.98, 6.99, 7.23]
        self.rawDataPoints = [409, 915, 1522, 2066, 2523, 2908, 3256, 3572, 3686]

        self.connected = False

    def bootup(self):
        self.checkConnection()
        if(self.connected):
            #Bootup sensor if needed
            return True
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

    
    def _checkSum(self, data):
        if (len(data) != 5):
            return False

        sum = 0
        for i in range(1,5):
            sum += data[i]
        
        sum = sum % 256
        crc_byte = data[0]
        overall = sum + crc_byte
        overall = overall % 256

        return overall == 0

    def _rawAirflow(self):
        try:
            with smbus2.SMBus(1) as bus:
                read = smbus2.i2c_msg.read(self.sensorAddress, 5)
                bus.i2c_rdwr(read)

                print(list(read))
                print(list(read))

                if not self._checkSum(list(read)):
                    print("Checksum failed")
                    return False

                print(list(read))

                airflowRaw = 0
                dataHighByte = list(read)[1]
                dataLowByte = list(read)[2]

                dataHighByte = dataHighByte & 0x0F

                airflowRaw = (dataHighByte << 8) | dataLowByte

                self.rawData = airflowRaw
                return True
            
        except OSError as e:
            print(f"Error reading from sensor: {e}")
            return False

    def _mpsAirflow(self):
        if self.rawData is None:
            self.rawData = None
            return None

        dataPos = 0
        for i in range(len(self.rawDataPoints)):
            if self.rawData > self.rawDataPoints[i]:
                dataPos = i

        if self.rawData <= 409:
            return 0
        if self.rawData >= 3686:
            return self.mpsDataPoints[-1]

        windowSize = self.rawDataPoints[dataPos + 1] - self.rawDataPoints[dataPos]
        diff = self.rawData - self.rawDataPoints[dataPos]
        percentageOfWindow = diff / windowSize
        mpsWindowSize = self.mpsDataPoints[dataPos + 1] - self.mpsDataPoints[dataPos]
        airflowMps = self.mpsDataPoints[dataPos] + (percentageOfWindow * mpsWindowSize)

        return airflowMps


    def getSensorData(self):
        if self.connected:
            self._rawAirflow()
            self.mpsData = self._mpsAirflow()
            return True
        else:
            return False

    def getData(self):
        return self.mpsData

    def printSensorData(self):
        print("================================")
        print(self.mpsData)

    def run(self):
        try:
            while True:
                self._rawAirflow()
                self.mpsData = self._mpsAirflow()

                self.printSensorData()
                time.sleep(0.2)

        except OSError as e:
            print(f"Error reading from sensor 2: {e}")
            return None



def __init__():
    p1 = SensorFS3000()
    # p1.start()
    p1.run()


if __name__ == "__main__":
    __init__() 