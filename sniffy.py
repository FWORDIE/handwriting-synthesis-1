import math
import time
from py_silhouette import SilhouetteDevice, enumerate_devices

import os

from modulea.plottie.cli import main


class TimeoutError(Exception):
    
    pass

def sendSting(self, string):
    self._send(string)

def waitforNothing(self, required, timeout = False):
    start_time = time.time()  
    while True:
        current_time = time.time()  
        elapsed_time = current_time - start_time  
        DATA = str(self.get_state())
        print('DATA', DATA)
        if DATA == required:
            break
        elif elapsed_time > 15 and timeout:  
            raise TimeoutError("Operation took too long. Never reached state: " + required + ' but instead is in state: ' + DATA)

def poop(self):
    print('pooing')
    ### Command for potrait 3 to eject out the back
    sendSting(self, b"AH0,500,200\x03")
    self.flush()
    waitforNothing(self, 'DeviceState.unloaded', True)
    
def eat(self):
    print('eating')
    ### Command for potrait 3 to auto feed and set up for moving
    sendSting(self,b"AF1,75,99,75,23\x03")
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
    for dev, params in enumerate_devices():
        print("    Found '{}'".format(params.product_name))
    input("    The expected device models should have been listed. <Press Enter>")

    print("  Test 0b: Connecting to first device")
    d = SilhouetteDevice()

    args = [
        "--plot", 
        "--native-order", 
        "--speed=100%", 
        "--force=10%", 
        "letters/My-Anchor-For-12-Years   S6_B2_L44_D2-7_N1-0_G0-9_C55_M20_displacedA4.svg"
    ]
    poop(d)
    eat(d)
    # d.flush()
    main(args)
    # os.system(f'plottie --plot --native-order --speed=100% --force=10% "letters/My-Anchor-For-12-Years   S6_B2_L44_D2-7_N1-0_G0-9_C55_M20_displacedA4.svg"')  
    poop(d)
