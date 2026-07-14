import sys
import pytest
from unittest.mock import MagicMock, patch, PropertyMock

mockBME = MagicMock()
mockBNO = MagicMock()
mockFE3 = MagicMock()
sys.modules["sensors.sensorBME688"] = mockBME
sys.modules["sensors.sensorBNO086"] = mockBNO
sys.modules["sensors.sensorFS3000"] = mockFE3

from sensorController import SensorController
import systemData

#Bootup
def test_bootup_sucess():

    controller = SensorController(systemData.SystemData())

    assert controller.bootup() == True

@patch("sensorController.BME688")
@patch("sensorController.BNO086")
@patch("sensorController.FS3000")
def test_bootup_sensorFails(mockFS3, mockBNO, mockBME):

    mockBME.SensorBME688.return_value.bootup.return_value = False
    mockBNO.SensorBNO086.return_value.bootup.return_value = False
    mockFS3.SensorFS3000.return_value.bootup.return_value = False
    
    controller = SensorController(systemData.SystemData())

    assert controller.bootup() == True
    mockBME.SensorBME688.assert_called_once()
    mockBME.SensorBME688.return_value.bootup.assert_called_once()
    assert controller.data.BME688Status == False
    mockBNO.SensorBNO086.assert_called_once()
    mockBNO.SensorBNO086.return_value.bootup.assert_called_once()
    assert controller.data.BNO086Status == False
    mockFS3.SensorFS3000.assert_called_once()
    mockFS3.SensorFS3000.return_value.bootup.assert_called_once()
    assert controller.data.FS3000Status == False

#Run Sensors
@patch("sensorController.BME688")
@patch("sensorController.BNO086")
@patch("sensorController.FS3000")
def test_run_sucess(mockFS3, mockBNO, mockBME):

    controller = SensorController(systemData.SystemData())

    controller.runBME688()
    controller.runBNO086()
    controller.runFS3000()
    mockBME.SensorBME688.return_value.getData.assert_called_once()
    mockBNO.SensorBNO086.return_value.getData.assert_called_once()
    mockFS3.SensorFS3000.return_value.getData.assert_called_once()


@patch("sensorController.BME688")
@patch("sensorController.BNO086")
@patch("sensorController.FS3000")
def test_run_failed(mockFS3, mockBNO, mockBME):

    mockBME.SensorBME688.return_value.getSensorData.side_effect = IOError
    mockBNO.SensorBNO086.return_value.getSensorData.side_effect = IOError
    mockFS3.SensorFS3000.return_value.getSensorData.side_effect = IOError
    
    controller = SensorController(systemData.SystemData())

    controller.runBME688()
    controller.runBNO086()
    controller.runFS3000()
    mockBME.SensorBME688.return_value.bootup.assert_called_once()
    mockBNO.SensorBNO086.return_value.bootup.assert_called_once()
    mockFS3.SensorFS3000.return_value.bootup.assert_called_once()

#Run all Sensors