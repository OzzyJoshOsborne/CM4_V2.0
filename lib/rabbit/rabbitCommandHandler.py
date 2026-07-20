import json
class RabbitCommandHandler:

    def __init__(self):
        pass

    def processsMsg(self, msg):
        decode = json.loads(msg)
        print(f"New MSG Recived - Command Handler - {decode}")
        self.handleCommand(decode)

    def handleCommand(self, decodedMsg):

        match decodedMsg['Type']:
            case 1:
                # Get State
                print("Command for - Get State")
            case 2:
                # Get settings
                print(f"Command for - Get Settings - Data: {decodedMsg['data']}")
            case 3:
                # Set Event
                print(f"Command for - Set Event - Data: {decodedMsg['data']}")
            case 4:
                # Set Core Temp
                print(f"Command for - Set Core Temp - Data: {decodedMsg['data']}")
            case 5:
                # Set Ati Temperature
                print(f"Command for - Set Air Temp - Data: {decodedMsg['data']}")
            case 6:
                # Set Air Pressure
                print(f"Command for - Set Air Pressure - Data: {decodedMsg['data']}")
            case 7:
                # Set Air Hum
                print(f"Command for - Set Air Hum - Data: {decodedMsg['data']}")
            case 8:
                # Set Air Vel
                print(f"Command for - Set Air Vel - Data: {decodedMsg['data']}")
            case 9:
                # Set IMU Pitch
                print(f"Command for - Set IMU Pitch - Data: {decodedMsg['data']}")
            case 10:
                # Set IMU Roll
                print(f"Command for - Set IMU Roll - Data: {decodedMsg['data']}")
            case 11:
                # Set IMU Yaw
                print(f"Command for - Set IMU Yaw - Data: {decodedMsg['data']}")
            case 12:
                # Set IMU All
                print(f"Command for - Set IMU All - Data: {decodedMsg['data']}")
            case 13:
                # Save Settings
                print(f"Command for - Save Settings - Data: {decodedMsg['data']}")
            case 20:
                # Send Initialised
                print(f"Command for - Send Initialised - Data: {decodedMsg['data']}")
            case 21:
                # Dis coms connected
                print(f"Command for - Dis Coms Connected - Data: {decodedMsg['data']}")
            case 23:
                # Dis upgrading
                print(f"Command for - Dis upgrading - Data: {decodedMsg['data']}")
            case 40:
                # Stopping Video
                print(f"Command for - Stopping Video - Data: {decodedMsg['data']}")
            case 41:
                # Exiting App
                print(f"Command for - Exiting App - Data: {decodedMsg['data']}")

            case _:
                print(f"New command #{decodedMsg['Type']} - data {decodedMsg['data']}")

