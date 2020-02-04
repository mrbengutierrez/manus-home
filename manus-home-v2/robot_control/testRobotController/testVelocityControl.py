"""
This file tests the setVelocity function for the Manus Home V2
Author: Benjamin Gutierrez
email: mrbengutierrez@gmail.com
"""

import sys
"""
This file tests the setVelocity function for the Manus Home V2
Author: Benjamin Gutierrez
email: mrbengutierrez@gmail.com
"""
import sys
sys.path.append("..")

from RobotController import ArmController
import time
import numpy as np



def printRobotInformation(arm):
	print("joint angles (deg)" + str(list(arm.getJointAngles()*180.0/np.pi)))
	print("position (m): " + str(list(arm.getPosition())))
	print("velocity (m/s): " + str(list(arm.getVelocity())))
	print("force (Nm): " + str(list(arm.getForce())))
	print("")
	

def testVelocityControl():
	arm = ArmController()
	arm.calibratePosition(angles=[180.0, 90.0], delayTime=10, calibrateMotors=False)
	print("Starting in 5 seconds")
	time.sleep(5)
	arm.__init__()
	while(True):
		try:
			arm.setVelocity(np.array([0,0.05])) # m/s
			printRobotInformation(arm)
			time.sleep(2)
			arm.setVelocity(np.array([0,-0.05])) # m/s
			printRobotInformation(arm)
			time.sleep(2)
		except KeyboardInterrupt:
			arm.stop()
			raise KeyboardInterrupt		
		
		

def main():
	testVelocityControl()
	
	
if __name__ == "__main__":
	main()
