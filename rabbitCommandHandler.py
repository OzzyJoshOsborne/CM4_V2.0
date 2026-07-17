
class RabbitCommandHandler:

    def __init__(self):
        pass

    def processsMsg(self, msg):
        print(f"New MSG Recived - {msg}")

    def handleCommand(self, command):

        match command:
            case 1:
                pass
            case 2:
                pass

            #...

