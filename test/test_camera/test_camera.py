import pytest 
import subprocess
from unittest.mock import MagicMock, patch

from camera import Camera

#Connected
@patch("camera.subprocess")
def test_isConnected_connected(mockSubPro):
    mockSubPro.run.return_value = subprocess.CompletedProcess(
        args=["my-command"],
        returncode=0,
        stdout="3D USB Camera: 3D USB Camera (usb-fe9c0000.xhci-1.1):\n\t/dev/video0\n\t/dev/video1\n\t/dev/media4\n\nbcm2835-codec (vchiq:bcm2835-codec):\n\t/dev/media2\n",
        stderr="",
    )

    camera = Camera()

    assert camera._isConnected() == True

@patch("camera.subprocess")
def test_isConnected_notConnected(mockSubPro):
    mockSubPro.run.return_value = subprocess.CompletedProcess(
        args=["my-command"],
        returncode=0,
        stdout="Some Output",
        stderr="",
    )
    
    camera = Camera()

    assert camera._isConnected() == False

@patch("camera.subprocess")
def test_isConnected_wrongName(mockSubPro):
    mockSubPro.run.return_value = subprocess.CompletedProcess(
        args=["my-command"],
        returncode=0,
        stdout="SomeWrong Camera Name (usb-fe9c0000.xhci-1.1):\n\t/dev/video0\n\t/dev/video1\n\t/dev/media4\n\nbcm2835-codec (vchiq:bcm2835-codec):\n\t/dev/media2\n",
        stderr="",
    )
    
    camera = Camera()

    assert camera._isConnected() == False

@patch("camera.subprocess")
def test_isConnected_numVideoDevices(mockSubPro):
    mockSubPro.run.return_value = subprocess.CompletedProcess(
        args=["my-command"],
        returncode=0,
        stdout="3D USB Camera: 3D USB Camera (usb-fe9c0000.xhci-1.1):\n\t/dev/video0\n\t/dev/video1\n\nbcm2835-codec (vchiq:bcm2835-codec):\n\t/dev/media2\n",
        stderr="",
    )
    
    camera = Camera()

    assert camera._isConnected() == False

@patch("camera.subprocess")
def test_isConnected_emptyOutput(mockSubPro):
    mockSubPro.run.return_value = subprocess.CompletedProcess(
        args=["my-command"],
        returncode=0,
        stdout="",
        stderr="",
    )
    
    camera = Camera()

    assert camera._isConnected() == False

@patch("camera.subprocess")
def test_isConnected_subprocessException(mockSubPro):
    mockSubPro.run.side_effect = FileNotFoundError()
    
    camera = Camera()

    assert camera._isConnected() == False


#Check Stream Running
@patch("camera.subprocess")
def test_checkStreamRunning_running(mockSubPro):
    mockSubPro.run.return_value = subprocess.CompletedProcess(
        args=["my-command"],
        returncode=0,
        stdout="",
        stderr="",
    )

    camera = Camera()

    assert camera.checkStreamRunning() == True

@patch("camera.subprocess")
def test_checkStreamRunning_notRunning(mockSubPro):
    mockSubPro.run.return_value = subprocess.CompletedProcess(
        args=["my-command"],
        returncode=1,
        stdout="",
        stderr="",
    )
    
    camera = Camera()

    assert camera.checkStreamRunning() == False

@patch("camera.subprocess")
def test_checkStreamRunning_exception(mockSubPro):
    mockSubPro.run.side_effect = FileNotFoundError()
    
    camera = Camera()

    with pytest.raises(Exception) as excInfo:
        camera.checkStreamRunning()


#Create Command
def test_createCommand_default():
    camera = Camera()

    assert camera.createCommand() == ["/usr/local/bin/mjpg_streamer",
                                    "-i", "/usr/local/lib/mjpg-streamer/input_uvc.so -n -f 10 -r 2560x720 -timeout 15",
                                    "-o", "/usr/local/lib/mjpg-streamer/output_http.so -p 8085 -w /usr/local/share/mjpg-streamer/www"]


#Start Stream
@patch("camera.subprocess")
def test_startStream_pass(mockSubPro):
    mockSubPro.Popen.return_value = subprocess.CompletedProcess(
        args=["my-command"],
        returncode=0,
        stdout="",
        stderr="",
    )
    
    camera = Camera()

    assert camera.startStream() == True

@patch("camera.subprocess")
def test_startStream_failed(mockSubPro):
    mockSubPro.Popen.return_value = subprocess.CompletedProcess(
        args=["my-command"],
        returncode=1,
        stdout="",
        stderr="",
    )
    
    camera = Camera()

    assert camera.startStream() == False

#End Strean
@patch("camera.subprocess")
def test_endStream_sucess(mockSubPro):
    mockSubPro.run.return_value = subprocess.CompletedProcess(
        args=["my-command"],
        returncode=0,
        stdout="",
        stderr="",
    )
    
    camera = Camera()

    assert camera.endStream() == True

@patch("camera.subprocess")
def test_endStream_fail(mockSubPro):
    mockSubPro.run.return_value = subprocess.CompletedProcess(
        args=["my-command"],
        returncode=1,
        stdout="",
        stderr="",
    )
    
    camera = Camera()

    assert camera.endStream() == False

@patch("camera.subprocess")
def test_endStream_error(mockSubPro):
    mockSubPro.run.return_value = FileNotFoundError()
    
    camera = Camera()

    with pytest.raises(Exception) as excInfo:
        camera.endStream()


#Bootup
def test_bootup_success():

    mockConnection = MagicMock()
    mockCheckStream = MagicMock()
    mockCheckStream.return_value = False

    camera = Camera()
    camera.connected = True

    camera.checkConnection = mockConnection
    camera.checkStreamRunning = mockCheckStream

    assert camera.bootup() == True

def test_bootup_fail():
    
    camera = Camera()

    assert camera.bootup() == False



