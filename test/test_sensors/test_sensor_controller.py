import sys
import pytest
from unittest.mock import MagicMock, patch, PropertyMock

import lib.systemData as systemData

#Bootup
def test_bootup_sucess():
    from lib.sensors.sensorController import SensorController

    controller = SensorController(systemData.SystemData())

    assert controller.bootup() == True

@patch("lib.sensors.sensorController.BME688")
@patch("lib.sensors.sensorController.BNO086")
@patch("lib.sensors.sensorController.FS3000")
def test_bootup_sensorFails(mockFS3, mockBNO, mockBME):
    from lib.sensors.sensorController import SensorController

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
@patch("lib.sensors.sensorController.BME688")
@patch("lib.sensors.sensorController.BNO086")
@patch("lib.sensors.sensorController.FS3000")
def test_run_sucess(mockFS3, mockBNO, mockBME):
    from lib.sensors.sensorController import SensorController

    controller = SensorController(systemData.SystemData())

    controller.runBME688()
    controller.runBNO086()
    controller.runFS3000()
    mockBME.SensorBME688.return_value.getData.assert_called_once()
    mockBNO.SensorBNO086.return_value.getData.assert_called_once()
    mockFS3.SensorFS3000.return_value.getData.assert_called_once()


@patch("lib.sensors.sensorController.BME688")
@patch("lib.sensors.sensorController.BNO086")
@patch("lib.sensors.sensorController.FS3000")
def test_run_failed(mockFS3, mockBNO, mockBME):
    from lib.sensors.sensorController import SensorController

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