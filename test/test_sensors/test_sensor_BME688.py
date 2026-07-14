import pytest
from unittest.mock import MagicMock, patch, PropertyMock

#Connect
def test_connected():
    from sensors.sensorBME688 import SensorBME688

    BME688 = SensorBME688()
    assert BME688._isConnected(1) == True

@patch("sensors.sensorBME688.smbus2.SMBus")
def test_connected_wrongAddress(mockSmBus):
    from sensors.sensorBME688 import SensorBME688

    mockBus = MagicMock()
    mockSmBus.return_value.__enter__.return_value = mockBus
    mockBus.write_quick.side_effect = OSError()

    BME688 = SensorBME688()
    assert BME688._isConnected(1) == False

@patch("sensors.sensorBME688.smbus2.SMBus")
def test_connected_wrongBus(mockSmBus):
    from sensors.sensorBME688 import SensorBME688

    mockSmBus.side_effect = OSError

    BME688 = SensorBME688()
    assert BME688._isConnected(99) == False


#Test set/get regs
@patch("sensors.sensorBME688.smbus2.SMBus")
def test_setRegs_sucess_byte(mockSmBus):
    from sensors.sensorBME688 import SensorBME688

    mockBus = MagicMock()
    mockSmBus.return_value.__enter__.return_value = mockBus

    BME688 = SensorBME688()
    
    BME688._setRegs(10, 5) 

    mockBus.write_byte_data.assert_called_once()

@patch("sensors.sensorBME688.smbus2.SMBus")
def test_setRegs_sucess_block(mockSmBus):
    from sensors.sensorBME688 import SensorBME688

    mockBus = MagicMock()
    mockSmBus.return_value.__enter__.return_value = mockBus

    BME688 = SensorBME688()
    
    BME688._setRegs(10, [20, 10, 5]) 

    mockBus.write_i2c_block_data.assert_called_once()

@patch("sensors.sensorBME688.smbus2.SMBus")
def test_setRegs_failedWrite(mockSmBus):
    from sensors.sensorBME688 import SensorBME688

    mockBus = MagicMock()
    mockSmBus.return_value.__enter__.return_value = mockBus
    mockBus.write_byte_data.side_effect = OSError()
    mockBus.write_i2c_block_data.side_effect = OSError()

    BME688 = SensorBME688()
    
    with pytest.raises(OSError):
        BME688._setRegs(10, 20)

    with pytest.raises(OSError):
        BME688._setRegs(10, [20, 10, 5])

    mockBus.write_byte_data.assert_called_once()
    mockBus.write_i2c_block_data.assert_called_once()

@patch("sensors.sensorBME688.smbus2.SMBus")
def test_getRegs_sucess_byte(mockSmBus):
    from sensors.sensorBME688 import SensorBME688

    mockBus = MagicMock()
    mockSmBus.return_value.__enter__.return_value = mockBus
    mockBus.read_byte_data.return_value = 10

    BME688 = SensorBME688()
    
    assert BME688._getRegs(10, 1) == 10 
    mockBus.read_byte_data.assert_called_once()

@patch("sensors.sensorBME688.smbus2.SMBus")
def test_getRegs_sucess_block(mockSmBus):
    from sensors.sensorBME688 import SensorBME688

    mockBus = MagicMock()
    mockSmBus.return_value.__enter__.return_value = mockBus
    mockBus.read_i2c_block_data.return_value = [10, 10]

    BME688 = SensorBME688()
    
    assert BME688._getRegs(10, 2) == [10, 10] 
    mockBus.read_i2c_block_data.assert_called_once()

@patch("sensors.sensorBME688.smbus2.SMBus")
def test_getRegs_failedRead(mockSmBus):
    from sensors.sensorBME688 import SensorBME688

    mockBus = MagicMock()
    mockSmBus.return_value.__enter__.return_value = mockBus
    mockBus.read_byte_data.side_effect = OSError()
    mockBus.read_i2c_block_data.side_effect = OSError()

    BME688 = SensorBME688()
    
    with pytest.raises(OSError):
        BME688._getRegs(10, 1)

    with pytest.raises(OSError):
        BME688._getRegs(10, 2)

    mockBus.read_byte_data.assert_called_once()
    mockBus.read_i2c_block_data.assert_called_once()



#Test Calibration Data
def test_calibarion_sucess():
    pass

def test_calibration_brokenData():
    pass


#Bootup
def test_bootup_sucess():
    from sensors.sensorBME688 import SensorBME688

    BME688 = SensorBME688()

    mockCali = MagicMock()
    BME688._getCalibrationData = mockCali
    
    assert BME688.bootup() == True

def test_bootup_fail():
    from sensors.sensorBME688 import SensorBME688

    BME688 = SensorBME688()

    mockSoftReset = MagicMock()
    mockSoftReset.side_effect = OSError()
    BME688._getCalibrationData = mockSoftReset
    
    assert BME688.bootup() == False



#Test Calc functions
def test_calc_temp():
    pass

def test_calc_temp_wrongTemp():
    pass

def test_calc_temp_wrongCalibration():
    pass

def test_calc_pressure():
    pass

def test_calc_pressure_wrongTemp():
    pass

def test_calc_pressure_wrongCalibration():
    pass

def test_calc_humidity():
    pass

def test_calc_humidity_wrongTemp():
    pass

def test_calc_humidity_wrongCalibration():
    pass


#Get Sensor Data
def test_getSensorData():
    from sensors.sensorBME688 import SensorBME688

    BME688 = SensorBME688()
    BME688.connected = True

    mockCalcTemp = MagicMock()
    mockCalcPres = MagicMock()
    mockCalcHumi = MagicMock()
    
    BME688._calcTemp = mockCalcTemp
    BME688._calcPressure = mockCalcPres
    BME688._calcHumidity = mockCalcHumi

    assert BME688.getSensorData() == True

def test_getSensorData_10Attempts():
    from sensors.sensorBME688 import SensorBME688

    BME688 = SensorBME688()
    BME688.connected = True

    mockCalcTemp = MagicMock()
    mockCalcPres = MagicMock()
    mockCalcHumi = MagicMock()

    mockGetRegs = MagicMock()
    mockGetRegs.return_value = 10
    
    BME688._calcTemp = mockCalcTemp
    BME688._calcPressure = mockCalcPres
    BME688._calcHumidity = mockCalcHumi
    BME688._getRegs = mockGetRegs

    assert BME688.getSensorData() == False

def test_getSensorData_setPowerFail():
    from sensors.sensorBME688 import SensorBME688

    BME688 = SensorBME688()
    BME688.connected = True

    mockCalcTemp = MagicMock()
    mockCalcPres = MagicMock()
    mockCalcHumi = MagicMock()

    mockSetPower = MagicMock()
    mockSetPower.side_effect = ValueError()
    
    BME688._calcTemp = mockCalcTemp
    BME688._calcPressure = mockCalcPres
    BME688._calcHumidity = mockCalcHumi
    BME688._setPowerMode = mockSetPower

    assert BME688.getSensorData() == False