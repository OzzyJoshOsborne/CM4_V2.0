import pytest 
import subprocess
from unittest.mock import MagicMock, patch

from cameraController import CameraController
from systemData import SystemData


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


