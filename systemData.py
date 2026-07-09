
class SystemData:

    def __init__(self):
        #Sensor Data
        self.BME688Status = None
        self.FS3000Status = None
        self.BNO086Status = None

        # BME688
        self.temperature = None
        self.pressure = None
        self.humidity = None

        # FS3000
        self.airFlowMps = None

        # BNO086
        self.yaw = None
        self.pitch = None
        self.roll = None

        # Camera
        self.cameraStatus = False

        # Display

        # Rabbit

