import sys
import pytest
from unittest.mock import MagicMock

# sys.modules["smbus2"] = MagicMock()
# sys.modules["board"] = MagicMock()
# sys.modules["busio"] = MagicMock()
# sys.modules["adafruit_bno08x"] = MagicMock()
# sys.modules["adafruit_bno08x.i2c"] = MagicMock()

@pytest.fixture(autouse=True)
def mock_pi_libraries(monkeypatch):
    monkeypatch.setitem(sys.modules, "smbus2", MagicMock())
    monkeypatch.setitem(sys.modules, "board", MagicMock())
    monkeypatch.setitem(sys.modules, "busio", MagicMock())
    monkeypatch.setitem(sys.modules, "adafruit_bno08x", MagicMock())
    monkeypatch.setitem(sys.modules, "adafruit_bno08x.i2c", MagicMock())

    for module in list(sys.modules):
        if module.startswith("lib.sensors."):
            del sys.modules[module]