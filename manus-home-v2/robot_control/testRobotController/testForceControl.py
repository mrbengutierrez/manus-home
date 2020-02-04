"""
This file tests the setForce function for the Manus Home V2
Author: Benjamin Gutierrez
email: mrbengutierrez@gmail.com
"""

import sys
sys.path.append("..")

from RobotController import ArmController
import time
import numpy as np


sys.path.append("..")

from RobotController import ArmController


def printRobotInformation(arm):
	print("joint angles (deg)" + str(list(arm.getJointAngles()*180.0/np.pi)))
	print("position (m): " + str(list(arm.getPosition())))
	print("velocity (m/s): " + str(list(arm.getVelocity())))
	print("force (N): " + str(list(arm.getForce())))
	print("")
	

def testForceControl():
	arm = ArmController()
	arm.calibratePosition(angles=[180.0, 90.0], delayTime=10, calibrateMotors=False)
	print("Starting in 5 seconds")
	time.sleep(5)	
	
	while(True):
		try:
			arm.setForce(np.array([0,1.0])) # N
			printRobotInformation(arm)
			time.sleep(5)
			arm.setForce(np.array([0,-1.0])) # N
			printRobotInformation(arm)
			time.sleep(5)
		except KeyboardInterrupt:
			arm.stop()
			raise KeyboardInterrupt

		
		

def main():
	testForceControl()
	
	
if __name__ == "__main__":
	main()
