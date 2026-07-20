import pytest 
import subprocess
from unittest.mock import MagicMock, patch

from lib.camera.cameraController import CameraController
from lib.systemData import SystemData


#Bootup
def test_bootup_pass():
    mockCamera = MagicMock()
    mockCamera.bootup.return_value = True

    cameraController = CameraController(SystemData())
    cameraController.camera = mockCamera

    assert cameraController.bootupCamera() == True

def test_bootup_fail():
    mockCamera = MagicMock()
    mockCamera.bootup.return_value = False

    cameraController = CameraController(SystemData())
    cameraController.camera = mockCamera

    assert cameraController.bootupCamera() == False


