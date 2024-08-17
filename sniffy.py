import math
import time
from py_silhouette import SilhouetteDevice, enumerate_devices, DeviceState
import os

from modulea.plottie.cli import main, args_to_outlines, parse_arguments, zero_on_regmarks


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
        print('DATA', DATA)
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


if __name__ == '__main__':

    print("Test 0: Discovery and connection.")
    print("  Test 0a: Enumerating devices:")
    # for dev, params in enumerate_devices():
    #     print("    Found '{}'".format(params.product_name))
    # input("    The expected device models should have been listed. <Press Enter>")

    print("  Test 0b: Connecting to first device")
    d = SilhouetteDevice()

    args = [
        "--plot",
        "--native-order",
        "--speed=100%",
        "--force=10%",
        "letters/My-Anchor-For-12-Years   S6_B2_L44_D2-7_N1-0_G0-9_C55_M20_displacedA4-01.svg"
    ]
    poop(d)
    eat(d)
    d.flush()
    # testRoute(d)

    # args = parse_arguments(args)

    # # if args is None:
    # #     return 0

    # lines = args_to_outlines(args)
    
    lines = [[(9.46051379104969, 17.28334314338315), (9.46051379104969, 17.46725029690205), (9.437529982111592, 17.789087815560134), (9.414546173173495, 18.202878910977667), (9.391562364235392, 18.63965840058506), (9.368578555297294, 19.076437890192455), (9.368578555297296, 19.513217379799855), (9.345594746359195, 19.904020081027525), (9.345594746359195, 20.248845993875463), (9.345594746359195, 20.524706724153816), (9.368578555297296, 20.708613877672718), (9.391562364235392, 20.800567454432173), (9.414546173173495, 20.823555848622036)]]

    # if args.regmarks:
    #     zero_on_regmarks(d, args.regmarks)

    # d.set_force(args.force)
    # d.set_speed(args.speed)
    # # if args.auto_blade_depth is not None:
    # #     try:
    # #         d.set_depth(args.auto_blade_depth)
    # #     except py_silhouette.AutoBladeNotSupportedError:
    # #         sys.stderr.write("--auto-blade-depth not supported by this device")
    # d.set_tool_diameter(
    #     # d.params.tool_diameters["Knife"]
    #     # if args.plot_mode == PlotMode.cut else
    #     d.params.tool_diameters["Pen"]
    # )
    # print(lines)
    # d.flush()

    for line in lines:
        print(line)
        for i, (x, y) in enumerate(line):
            pen_down = i > 0
            d.move_to(x, y, pen_down)
        d.flush()

    d.move_home()
    d.flush()

    while d.get_state() == DeviceState.moving:
        time.sleep(0.5)

    # os.system(f'plottie --plot --native-order --speed=100% --force=10% "letters/My-Anchor-For-12-Years   S6_B2_L44_D2-7_N1-0_G0-9_C55_M20_displacedA4.svg"')
    poop(d)
