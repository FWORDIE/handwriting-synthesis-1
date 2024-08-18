import time
from py_silhouette import SilhouetteDevice, enumerate_devices, DeviceState
from modulea.plottie.cli import main, args_to_outlines, parse_arguments, zero_on_regmarks, svg_to_outlines

class TimeoutError(Exception):
    pass


def sendSting(self, string):
    self._send(string)


def waitforNothing(self, required, timeout=False):
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        DATA = str(self.get_state())
        # print('DATA', DATA)
        if DATA == required:
            break
        elif elapsed_time > 15 and timeout:
            raise TimeoutError("Operation took too long. Never reached state: " +
                               required + ' but instead is in state: ' + DATA)


def poop(self):
    print('pooing')
    
    # Command for potrait 3 to eject out the back
    sendSting(self, b"AH0,500,200\x03")
    self.flush()
    waitforNothing(self, 'DeviceState.unloaded', True)


def eat(self):
    print('eating')
    
    # Command for potrait 3 to auto feed and set up for moving
    sendSting(self, b"AF1,75,99,75,23\x03")
    self.flush()
    waitforNothing(self, 'DeviceState.ready', True)


def testRoute(self):
    print('moving')
    self.move_to(40, 0, False)
    self.move_to(60, 0, True)

    self.move_to(0, 40, False)
    self.move_to(0, 60, True)

    self.move_to(170, 40, False)
    self.move_to(170, 60, True)

    self.move_to(40, 140, False)
    self.move_to(60, 140, True)

    self.move_to(150, 140, False)
    self.move_to(170, 140, True)
    self.move_to(170, 120, True)

    self.move_home()
    self.flush()


def printLetter(fileName):
    print(fileName)
    print('INKING')
    d = SilhouetteDevice()

    args = [
        "--plot",
        "--native-order",
        "--speed=100%",
        "--force=10%",
        f"{fileName}"
    ]
    
    
    poop(d)
    eat(d)
    d.flush()

    args = parse_arguments(args, d)

    lines = args_to_outlines(args)

    d.set_force(args.force)
    d.set_speed(args.speed)
    d.set_tool_diameter(
        d.params.tool_diameters["Pen"]
    )

    for line in lines:
        # print(line)
        for i, (x, y) in enumerate(line):
            pen_down = i > 0
            d.move_to(x, y, pen_down)
        d.flush()

    d.move_home()
    d.flush()

    while d.get_state() == DeviceState.moving:
        time.sleep(0.5)

    poop(d)


if __name__ == '__main__':
    
    printLetter('letters/My-Anchor-For-12-Years   S6_B2_L44_D2-7_N1-0_G0-9_C55_M20_displacedA4-01.svg')

    
