import sys
import pytest
from unittest.mock import MagicMock, patch, PropertyMock

mockSmbus2 = MagicMock()
sys.modules["smbus2"] = mockSmbus2

mockBoard = MagicMock()
sys.modules["board"] = mockBoard

mockBusio= MagicMock()
sys.modules["busio"] = mockBusio

mockAdafruit = MagicMock()
sys.modules["adafruit_bno08x"] = mockAdafruit

mockAdafruitI2c = MagicMock()
sys.modules["adafruit_bno08x.i2c"] = mockAdafruitI2c


from sensors.sensorBNO086 import SensorBNO086

#Connect
def test_connected():
    
    BNO086 = SensorBNO086()
    assert BNO086._isConnected(1) == True

@patch("sensors.sensorBNO086.smbus2.SMBus")
def test_connected_wrongAddress(mockSmBus):
    mockBus = MagicMock()
    mockSmBus.return_value.__enter__.return_value = mockBus
    mockBus.write_quick.side_effect = OSError()

    BNO086 = SensorBNO086()
    assert BNO086._isConnected(1) == False

@patch("sensors.sensorBNO086.smbus2.SMBus")
def test_connected_wrongBus(mockSmBus):
    mockSmBus.side_effect = OSError

    BNO086 = SensorBNO086()
    assert BNO086._isConnected(99) == False

#Bootup
def test_bootup_sucess():
    BNO086 = SensorBNO086()

    assert BNO086.bootup() == True

@patch("sensors.sensorBNO086.busio.I2C")
def test_bootup_fail_i2c(mockI2c):
    mockI2c.side_effect = OSError("I2C Bus Failed")

    BNO086 = SensorBNO086()

    assert BNO086.bootup() == False

@patch("sensors.sensorBNO086.BNO08X_I2C")
def test_bootup_fail_bno(mockBNO):
    mockBNO.side_effect = OSError("BNO Sensor Failed")

    BNO086 = SensorBNO086()

    assert BNO086.bootup() == False

@patch("sensors.sensorBNO086.BNO08X_I2C")
def test_bootup_fail_bno_cali(mockBNO):

    mockSensor = MagicMock()

    mockBNO.return_value = mockSensor

    mockSensor.begin_calibration.side_effect = OSError("BNO Calibration Failed")

    BNO086 = SensorBNO086()

    assert BNO086.bootup() == False

@patch("sensors.sensorBNO086.BNO08X_I2C")
def test_bootup_fail_bno_enable(mockBNO):

    mockSensor = MagicMock()

    mockBNO.return_value = mockSensor

    mockSensor.enable_feature.side_effect = OSError("BNO Enable Feature Failed")

    BNO086 = SensorBNO086()

    assert BNO086.bootup() == False


#Quaternion Data
def test_quaternion():
    mockBNO = MagicMock()

    type(mockBNO).quaternion = PropertyMock(
        return_value=(10,10,10,10)
    )

    BNO086 = SensorBNO086()
    BNO086.bno = mockBNO

    BNO086._getQuaternionData()

    assert BNO086.quaternionData == (10,10,10,10)

def test_quaternion_fail():
    mockBNO = MagicMock()

    type(mockBNO).quaternion = PropertyMock(
        side_effect=RuntimeError()
    )

    BNO086 = SensorBNO086()
    BNO086.bno = mockBNO

    BNO086._getQuaternionData()

    assert BNO086._getQuaternionData() == False


#Calc Euler
def test_calcEuler():
    BNO086 = SensorBNO086()

    w,x,y,z = (0.9238795, 0.0, 0.3826834, 0.0)  # w x y z
    yaw_pitch_roll = ( 0.0,
        0.7853981633974483,
        0.0
    )  # yaw pitch roll degrees

    assert BNO086._calcEulerAngles(w,x,y,z) == pytest.approx(yaw_pitch_roll, abs=0.000001)

def test_calcEuler_badData():
    BNO086 = SensorBNO086()

    w,x,y,z = (5.0, -3.0, 8.0, 2.0)  # w x y z

    assert BNO086._calcEulerAngles(w,x,y,z) == (0, 0, 0)

def test_calcEuler_noData():
    BNO086 = SensorBNO086()

    assert BNO086._calcEulerAngles(None, None, None, None) == (0, 0, 0)


#Get Sensor Data
def test_getSensorData():
    mockBNO = MagicMock()

    type(mockBNO).quaternion = PropertyMock(
        return_value=(0.0, 0.3826834, 0.0, 0.9238795)
    )

    
    BNO086 = SensorBNO086()
    BNO086.connected = True
    BNO086.bno = mockBNO
    # BNO086.quaternionData = (0.9238795, 0.0, 0.3826834, 0.0)

    assert BNO086.getSensorData() == True
    assert BNO086.data.yaw == pytest.approx(0.0, abs=0.000001)
    assert BNO086.data.pitch == pytest.approx(0.7853981633974483, abs=0.000001)
    assert BNO086.data.roll == pytest.approx(0.0, abs=0.000001)

def test_getSensorData_noSensor():
    BNO086 = SensorBNO086()
    BNO086.connected = True
    BNO086.quaternionData = {}
    
    assert BNO086.getSensorData() == False
