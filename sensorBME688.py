import time 
import smbus2
from threading import Thread

connected = True
running = True

#Constants for BME688
OS_2X = 2
OS_4X = 3
OS_8X = 4
FILTER_SIZE_3 = 2
ENABLE_GAS_MEAS = -1

SLEEP_MODE = 0
FORCED_MODE = 1

SOFT_RESET_ADDR = 0xe0
SOFT_RESET_CMD = 0xb6
RESET_PERIOD = 10

FIELD0_ADDR = 0x1d
FIELD_LENGTH = 17

NEW_DATA_MSK = 0x80
POLL_PERIOD_MS = 10

CONF_OS_H_ADDR = 0X72
OSH_MSK = 0X07
OSH_POS = 0
CONF_T_P_MODE_ADDR = 0X74
OSP_MSK = 0X1C
OSP_POS = 2
OST_MSK = 0XE0
OST_POS = 5
CONF_ODR_FILT_ADDR = 0X75
FILTER_MSK = 0X1C
FILTER_POS = 2
CONF_ODR_RUN_GAS_NBC_ADDR = 0X71
RUN_GAS_MSK = 0X30
RUN_GAS_POS = 4
MODE_MSK = 0x03
MODE_POS = 0

T1_LSB_REG = 33
T1_MSB_REG = 34
T2_LSB_REG = 1
T2_MSB_REG = 2
T3_REG = 3

P1_LSB_REG = 5
P1_MSB_REG = 6
P2_LSB_REG = 7
P2_MSB_REG = 8
P3_REG = 9
P4_LSB_REG = 11
P4_MSB_REG = 12
P5_LSB_REG = 13
P5_MSB_REG = 14
P7_REG = 15
P6_REG = 16
P8_LSB_REG = 19
P8_MSB_REG = 20
P9_LSB_REG = 21
P9_MSB_REG = 22
P10_REG = 23

HUM_REG_SHIFT_VAL = 4
BIT_H1_DATA_MSK = 0x0F
H2_MSB_REG = 25
H2_LSB_REG = 26
H1_LSB_REG = 26
H1_MSB_REG = 27
H3_REG = 28
H4_REG = 29
H5_REG = 30
H6_REG = 31
H7_REG = 32

def bytesToWords(msb, lsb, bits=16, signed=False):
    """Convert a most and least significant byte into a word."""
    # TODO: Reimplement with struct
    word = (msb << 8) | lsb
    if signed:
        word = twosComp(word, bits)
    return word

def twosComp(val, bits=16):
    """Convert two bytes into a two's compliment signed word."""
    # TODO: Reimplement with struct
    if val & (1 << (bits - 1)) != 0:
        val = val - (1 << bits)
    return val


class CalibrationData:
    
    def __init__(self):
        self.t1 = 0
        self.t2 = 0
        self.t3 = 0
    
        self.t_fine = 0

        self.p1 = 0
        self.p2 = 0
        self.p3 = 0
        self.p4 = 0
        self.p5 = 0
        self.p6 = 0
        self.p7 = 0
        self.p8 = 0
        self.p9 = 0
        self.p10 = 0

        self.h1 = 0
        self.h2 = 0
        self.h3 = 0
        self.h4 = 0
        self.h5 = 0
        self.h6 = 0
        self.h7 = 0


    def setFromArray(self, calibration):
        self.t1 = bytesToWords(calibration[T1_MSB_REG], calibration[T1_LSB_REG])
        self.t2 = bytesToWords(calibration[T2_MSB_REG], calibration[T2_LSB_REG], bits=16, signed=True)
        self.t3 = twosComp(calibration[T3_REG], bits=8)

        self.p1 = bytesToWords(calibration[P1_MSB_REG], calibration[P1_LSB_REG])
        self.p2 = bytesToWords(calibration[P2_MSB_REG], calibration[P2_LSB_REG], bits=16, signed=True)
        self.p3 = twosComp(calibration[P3_REG], bits=8)
        self.p4 = bytesToWords(calibration[P4_MSB_REG], calibration[P4_LSB_REG], bits=16, signed=True)
        self.p5 = bytesToWords(calibration[P5_MSB_REG], calibration[P5_LSB_REG], bits=16, signed=True)
        self.p6 = twosComp(calibration[P6_REG], bits=8)
        self.p7 = twosComp(calibration[P7_REG], bits=8)
        self.p8 = bytesToWords(calibration[P8_MSB_REG], calibration[P8_LSB_REG], bits=16, signed=True)
        self.p9 = bytesToWords(calibration[P9_MSB_REG], calibration[P9_LSB_REG], bits=16, signed=True)
        self.p10 = calibration[P10_REG]

        self.h1 = (calibration[H1_MSB_REG] << HUM_REG_SHIFT_VAL) | (calibration[H1_LSB_REG] & BIT_H1_DATA_MSK)
        self.h2 = (calibration[H2_MSB_REG] << HUM_REG_SHIFT_VAL) | (calibration[H2_LSB_REG] >> HUM_REG_SHIFT_VAL)
        self.h3 = twosComp(calibration[H3_REG], bits=8)
        self.h4 = twosComp(calibration[H4_REG], bits=8)
        self.h5 = twosComp(calibration[H5_REG], bits=8)
        self.h6 = calibration[H6_REG]
        self.h7 = twosComp(calibration[H7_REG], bits=8)

class Data:
    def __init__(self):
        self.status = None
        # self.heatStable = None
        # self.gasIndex = None
        # self.measIndex = None
        self.temperature = None
        self.pressure = None
        self.humidity = None
        # self.gasResistance = None

class SensorBME688:

    def __init__(self):
        super().__init__()
        
        self.sensorAddress = 0x76

        self.calibrationData = CalibrationData()
        self.data = Data()

        self.busNum = 1

        self.connected = False

        # self.airTemperature = 0.0
        # self.airPressure = 0.0
        # self.airHumidity = 0.0

        # self.airTemperatureState = True
        # self.airPressureState = True
        # self.airHumidityState = True

        # self.airTemperatureMinimum = 20
        # self.airTemperatureMaximum = 40

        # self.airPressureMinimum = 500
        # self.airPressureMaximum = 1500

        # self.airHumidityMinimum = 30
        # self.airHumidityMaximum = 40


    def bootup(self):
        self.checkConnection()
        if(self.connected):
            #Rap in try block, if failed return False.
            self._softReset()
            self._setPowerMode(SLEEP_MODE)

            self._getCalibrationData()

            self.setHumidityOversample(OS_2X)
            self.setPressureOversample(OS_4X)
            self.setTemperatureOversample(OS_8X)
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


    def _getCalibrationData(self):
        calibration = self._getRegs(0x89, 25)
        calibration += self._getRegs(0xe1, 16)

        #heat range, value, etc

        self.calibrationData.setFromArray(calibration)

    def _softReset(self):
        self._setRegs(SOFT_RESET_ADDR, SOFT_RESET_CMD)
        time.sleep(RESET_PERIOD / 1000.0)


    def setHumidityOversample(self, value):
        self._setBits(CONF_OS_H_ADDR, OSH_MSK, OSH_POS, value)

    def setPressureOversample(self, value):
        self._setBits(CONF_T_P_MODE_ADDR, OSP_MSK, OSP_POS, value)

    def setTemperatureOversample(self, value):
        self._setBits(CONF_T_P_MODE_ADDR, OST_MSK, OST_POS, value)

    def setFilter(self, filter_size):
        pass

    def setGasStatus(self, status):
        pass

    def setTempOffset(self, offset):
        pass


    def _setBits(self, register, mask, position, value):
        temp = self._getRegs(register, 1)
        temp &= ~mask
        temp |= value << position
        self._setRegs(register, temp)

    def _setRegs(self, register, value):
        with smbus2.SMBus(self.busNum ) as bus:
            if isinstance(value, int):
                bus.write_byte_data(self.sensorAddress, register, value)
            else:
                bus.write_i2c_block_data(self.sensorAddress, register, value)

    def _getRegs(self, register, length):
        with smbus2.SMBus(self.busNum ) as bus:
            if length == 1:
                return bus.read_byte_data(self.sensorAddress, register)
            else:
                return bus.read_i2c_block_data(self.sensorAddress, register, length)


    def _setPowerMode(self, mode):
        if mode not in [SLEEP_MODE, FORCED_MODE]:
            raise ValueError("Invalid power mode")

        self._setBits(CONF_T_P_MODE_ADDR, MODE_MSK, MODE_POS, mode)


    def _calcTemp(self, temp_adc):
        var1 = (temp_adc >> 3) - (self.calibrationData.t1 << 1)
        var2 = (var1 * (self.calibrationData.t2)) >> 11
        var3 = ((var1 >> 1) * (var1 >> 1)) >> 12
        var3 = ((var3) * (self.calibrationData.t3 << 4)) >> 14


        self.calibrationData.t_fine = (var2 + var3) + 0
        calcTemp = (((self.calibrationData.t_fine * 5) + 128) >> 8) / 100.0
        return calcTemp

    def _calcPressure(self, pres_adc):
        var1 = ((self.calibrationData.t_fine) >> 1) - 64000
        var2 = ((((var1 >> 2) * (var1 >> 2)) >> 11) * self.calibrationData.p6) >> 2
        var2 = var2 + ((var1 * self.calibrationData.p5) << 1)
        var2 = (var2 >> 2) + (self.calibrationData.p4 << 16)
        var1 = (((((var1 >> 2) * (var1 >> 2)) >> 13) * ((self.calibrationData.p3 << 5)) >> 3) + 
                ((self.calibrationData.p2 * var1) >> 1))
        var1 = var1 >> 18

        var1 = ((32768 + var1) * self.calibrationData.p1) >> 15
        calc_pres = 1048576 - pres_adc
        calc_pres = ((calc_pres - (var2 >> 12)) * 3125)

        if calc_pres >= (1 << 31):
            calc_pres = ((calc_pres // var1) << 1)
        else:
            calc_pres = ((calc_pres << 1) // var1)

        var1 = (self.calibrationData.p9 * (((calc_pres >> 3) * (calc_pres >> 3)) >> 13)) >> 12
        var2 = ((calc_pres >> 2) * self.calibrationData.p8) >> 13
        var3 = ((calc_pres >> 8) * (calc_pres >> 8) * (calc_pres >> 8) * self.calibrationData.p10) >> 17

        calc_pres = (calc_pres) + ((var1 + var2 + var3 + (self.calibrationData.p7 << 7)) >> 4)

        return calc_pres / 100.0

    def _calcHumidity(self, hum_adc):

        temp_scaled = ((self.calibrationData.t_fine * 5) + 128) >> 8
        var1 = (hum_adc - ((self.calibrationData.h1 * 16))) -\
                (((temp_scaled * self.calibrationData.h3) // (100)) >> 1)
        var2 = (self.calibrationData.h2 *
                (((temp_scaled * self.calibrationData.h4) // (100)) +
                    (((temp_scaled * ((temp_scaled * self.calibrationData.h5) // (100))) >> 6) //
                    (100)) + (1 * 16384))) >> 10
        var3 = var1 * var2
        var4 = self.calibrationData.h6 << 7
        var4 = ((var4) + ((temp_scaled * self.calibrationData.h7) // (100))) >> 4
        var5 = ((var3 >> 14) * (var3 >> 14)) >> 10
        var6 = (var4 * var5) >> 1
        calc_hum = (((var3 + var6) >> 10) * (1000)) >> 12

        return min(max(calc_hum, 0), 100000) / 1000.0


    def getSensorData(self):
        if self.connected:
            self._setPowerMode(FORCED_MODE)

            for attempt in range(10):
                status = self._getRegs(FIELD0_ADDR, 1)

                if (status & NEW_DATA_MSK) == 0:
                    time.sleep(POLL_PERIOD_MS / 1000.0)
                    continue

                regs = self._getRegs(FIELD0_ADDR, FIELD_LENGTH)
                            
                adc_pres = (regs[2] << 12) | (regs[3] << 4) | (regs[4] >> 4)
                adc_temp = (regs[5] << 12) | (regs[6] << 4) | (regs[7] >> 4)
                adc_hum = (regs[8] << 8) | regs[9]
                
                self.data.temperature = self._calcTemp(adc_temp)
                self.data.pressure = self._calcPressure(adc_pres)
                self.data.humidity = self._calcHumidity(adc_hum)

                return True
            return False
        else:
            return False

    def getData(self):
        return self.data


    def printSensorData(self):
        print("================================")
        print(self.data.temperature)
        print(self.data.pressure)
        print(self.data.humidity)

    def run(self):
        try:
            while self.connected: 
                try:
                    self.getSensorData()
                    self.printSensorData()

                except (RuntimeError, IOError) as e:
                    self.connected = False
                    # print(e)

                time.sleep(1)
        except (RuntimeError, IOError) as e:
            self.connected = False
            # print(e)


def __init__():
    p1 = SensorBME688()
    # p1.start()
    p1.run()


if __name__ == "__main__":
    __init__() 