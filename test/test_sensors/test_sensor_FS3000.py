import pytest
from unittest.mock import MagicMock, patch

#Connected
@patch("sensors.sensorFS3000.smbus2.SMBus")
def test_connected(mockSmBus): 
    from lib.sensors.sensorFS3000 import SensorFS3000

    mockBus = MagicMock()
    mockSmBus.return_value.__enter__.return_value = mockBus

    FS3000 = SensorFS3000()
    assert FS3000._isConnected(1) == True


@patch("sensors.sensorFS3000.smbus2.SMBus")
def test_connected_wrongAddress(mockSmBus):
    from lib.sensors.sensorFS3000 import SensorFS3000

    mockBus = MagicMock()
    mockSmBus.return_value.__enter__.return_value = mockBus
    mockBus.write_quick.side_effect = OSError()

    FS3000 = SensorFS3000()
    assert FS3000._isConnected(1) == False

@patch("sensors.sensorFS3000.smbus2.SMBus")
def test_connected_wrongBus(mockSmBus):
    from lib.sensors.sensorFS3000 import SensorFS3000

    mockSmBus.side_effect = OSError

    FS3000 = SensorFS3000()
    assert FS3000._isConnected(99) == False


#Boot up
def test_bootup():
    from lib.sensors.sensorFS3000 import SensorFS3000

    FS3000 = SensorFS3000()
    FS3000.connected = True
    assert FS3000.bootup() == True

def test_bootup_fail():
    from lib.sensors.sensorFS3000 import SensorFS3000

    FS3000 = SensorFS3000()
    FS3000.checkConnection = MagicMock(return_value=False)
    FS3000.connected = False
    assert FS3000.bootup() == False


#Check Sum
def test_checksum_valid():
    from lib.sensors.sensorFS3000 import SensorFS3000

    FS3000 = SensorFS3000()

    data = [0x6A, 0x01, 0x95, 0x00, 0x00]

    assert FS3000._checkSum(data) == True
    
def test_checksum_invaild():
    from lib.sensors.sensorFS3000 import SensorFS3000
    
    FS3000 = SensorFS3000()

    data = [0x6B, 0x01, 0x95, 0x00, 0x00]

    assert FS3000._checkSum(data) == False

def test_checksum_short_packet():
    from lib.sensors.sensorFS3000 import SensorFS3000

    FS3000 = SensorFS3000()

    data = [0x6A, 0x01, 0x95, 0x00]

    assert FS3000._checkSum(data) == False

def test_checksum_corrupted():
    from lib.sensors.sensorFS3000 import SensorFS3000

    FS3000 = SensorFS3000()

    data = [0x6A, 0x01, 0x96, 0x00, 0x00]

    assert FS3000._checkSum(data) == False


#Raw Air Flow
@patch("sensors.sensorFS3000.smbus2")
def test_get_rawAirflow(mockSmBus):
    from lib.sensors.sensorFS3000 import SensorFS3000

    FS3000 = SensorFS3000()

    fakeRead = MagicMock()
    fakeRead.__iter__.side_effect = lambda: iter(
        [0x6A, 0x01, 0x95, 0x00, 0x00]
    )
    mockSmBus.i2c_msg.read.return_value = fakeRead

    assert FS3000._rawAirflow() == True

def test_get_rawAirFlow_bad_data():
    from lib.sensors.sensorFS3000 import SensorFS3000
    
    FS3000 = SensorFS3000()

    assert FS3000._rawAirflow() == False

@patch("sensors.sensorFS3000.smbus2.SMBus")
def test_get_rawAirflow_brokenBus(mockSmBus):
    from lib.sensors.sensorFS3000 import SensorFS3000
    
    mockSmBus.side_effect = OSError

    FS3000 = SensorFS3000()
    assert FS3000._rawAirflow() == False


#MPS AIr Flow
def test_mps_none():
    from lib.sensors.sensorFS3000 import SensorFS3000

    FS3000 = SensorFS3000()

    FS3000.rawData = None

    assert FS3000._mpsAirflow() == None

def test_mps_zero():
    from lib.sensors.sensorFS3000 import SensorFS3000

    FS3000 = SensorFS3000()

    FS3000.rawData = 0

    assert FS3000._mpsAirflow() == 0

def test_mps_min():
    from lib.sensors.sensorFS3000 import SensorFS3000

    FS3000 = SensorFS3000()

    FS3000.rawData = 409

    assert FS3000._mpsAirflow() == 0

def test_mps_max():
    from lib.sensors.sensorFS3000 import SensorFS3000

    FS3000 = SensorFS3000()

    FS3000.rawData = 3686

    assert FS3000._mpsAirflow() == 7.23

def test_mps_exactDataPoint():
    from lib.sensors.sensorFS3000 import SensorFS3000

    FS3000 = SensorFS3000()

    FS3000.rawData = 2523

    assert FS3000._mpsAirflow() == 3.97


@pytest.mark.parametrize(
        "raw, expected",
        [
            (2180.25, 3.2425), # 25%
            (2294.5, 3.485), # 50%
            (2408.75, 3.7275), # 75%
        ]
)
def test_mps_notExactDataPoints(raw, expected):
    from lib.sensors.sensorFS3000 import SensorFS3000
    
    FS3000 = SensorFS3000()

    FS3000.rawData = raw

    assert FS3000._mpsAirflow() == pytest.approx(expected, abs=0.1)



#Get Sensor Data
def test_getSensorData():
    from lib.sensors.sensorFS3000 import SensorFS3000

    FS3000 = SensorFS3000()

    FS3000.connected = True

    assert FS3000.getSensorData() == True

def test_getSensorData_noSensor():
    from lib.sensors.sensorFS3000 import SensorFS3000
    
    FS3000 = SensorFS3000()

    FS3000.connected = False

    assert FS3000.getSensorData() == False



