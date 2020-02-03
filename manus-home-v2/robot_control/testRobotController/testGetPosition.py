"""
This file tests the getPosition function for the Manus Home V2
Author: Benjamin Gutierrez
email: mrbengutierrez@gmail.com
"""

import sys
sys.path.append("..")

import time
from RobotController import ArmController




def testGetPosition():
	arm = ArmController()
	while(True):
		position = arm.getPosition()
		x = position[0]
		y = position[1]
		print("x: " + str(round(x,2)) + "m, y: " + str(round(y,2)) + "m")
		print("")
		time.sleep(1) # delay one second
		

def main():
	testGetPosition()

if __name__ == "__main__":
	main()
