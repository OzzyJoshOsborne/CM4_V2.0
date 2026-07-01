import time
import bme680.__init__ as bme680
from threading import Thread

AirTemperature=0.0
AirPressure =0.0
AirHumidity=0.0

AirTemperatureState=True
AirPressureState=True
AirHumidityState=True

AirTemperatureMinimum=20
AirTemperatureMaximum=40

AirPressureMinimum=500
AirPressureMaximum=1500

AirHumidityMinimum = 30
AirHumidityMaximum = 40

Connected=False
Running=True
def RunSensor():
    global Running
    global AirTemperature
    global AirPressure
    global AirHumidity
    
    global AirTemperatureState
    global AirPressureState
    global AirHumidityState
    
    global AirTemperatureMinimum
    global AirTemperatureMaximum

    global AirPressureMinimum
    global AirPressureMaximum

    global AirHumidityMinimum
    global AirHumidityMaximum
    
    global Connected
    try:
        sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        # sensor.set_humidity_oversample(bme680.OS_2X)
        # sensor.set_pressure_oversample(bme680.OS_4X)
        # sensor.set_temperature_oversample(bme680.OS_8X)
        # sensor.set_filter(bme680.FILTER_SIZE_3)
        # sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        
        # sensor.set_gas_heater_temperature(320)
        # sensor.set_gas_heater_duration(150)
        # sensor.select_gas_heater_profile(0)
        Connected=True
        while Connected==True:
            if Running==False:
                break
            try:
                if sensor.get_sensor_data():
                    AirTemperature=sensor.data.temperature
                    tstate =True
                    if (AirTemperature>AirTemperatureMaximum):
                        tstate=False
                    if (AirTemperature<AirTemperatureMinimum):
                        tstate=False
                    AirTemperatureState=tstate
                    
                    AirPressure=sensor.data.pressure
                    tstate =True
                    if (AirPressure<AirPressureMinimum):
                        tstate=False
                    if (AirPressure>AirPressureMaximum):
                        tstate=False
                    AirPressureState=tstate
                    
                    AirHumidity=sensor.data.humidity
                    tstate =True
                    if (AirHumidity<AirHumidityMinimum):
                        tstate=False
                    if (AirHumidity>AirHumidityMaximum):
                        tstate=False
                    AirHumidityState=tstate
                    
                    print("================================")
                    print(AirTemperature)
                    print(AirPressure)
                    print(AirHumidity)

            except (RuntimeError, IOError):
                Connected=False

            time.sleep(1)
    except RuntimeError:
        Connected=False    
        
    Connected=False
    time.sleep(2)
    __init__()



def _get_regs(self, register, length):
    """Get one or more registers."""
    if length == 1:
        return self._i2c.read_byte_data(self.i2c_addr, register)
    else:
        return self._i2c.read_i2c_block_data(self.i2c_addr, register, length)

def get_sensor_data(self):

    for attempt in range(10):

        regs = self._get_regs(constants.FIELD0_ADDR, constants.FIELD_LENGTH)

        self.data.status = regs[0] & constants.NEW_DATA_MSK
        # Contains the nb_profile used to obtain the current measurement
        self.data.gas_index = regs[0] & constants.GAS_INDEX_MSK
        self.data.meas_index = regs[1]

        adc_pres = (regs[2] << 12) | (regs[3] << 4) | (regs[4] >> 4)
        adc_temp = (regs[5] << 12) | (regs[6] << 4) | (regs[7] >> 4)
        adc_hum = (regs[8] << 8) | regs[9]


        self.data.heat_stable = (self.data.status & constants.HEAT_STAB_MSK) > 0

        temperature = self._calc_temperature(adc_temp)
        self.data.temperature = temperature / 100.0
        self.ambient_temperature = temperature  # Saved for heater calc

        self.data.pressure = self._calc_pressure(adc_pres) / 100.0
        self.data.humidity = self._calc_humidity(adc_hum) / 1000.0


    
def __init__():
        
        p1=Thread(target=RunSensor)
        p1.start()
        
__init__()
        
    
