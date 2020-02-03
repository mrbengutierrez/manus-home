
from CheaperManusController import ArmController
import time
import numpy as np

def printRobotInformation(arm):
	print("joint angles (deg)" + str(list(arm.getJointAngles()*180.0/np.pi)))
	print("position (m): " + str(list(arm.getPosition())))
	print("velocity (m/s): " + str(list(arm.getVelocity())))
	print("force (Nm): " + str(list(arm.getForce())))
	print("")

def testPositionControl():
	arm = ArmController()
	while(True):
		arm.setPosition(np.array([-0.1,0.4]))
		printRobotInformation(arm)
		time.sleep(5)
		arm.setPosition(np.array([0.1,0.4]))
		printRobotInformation(arm)
		time.sleep(5)
		
		

def main():
	testPositionControl()
	
	
if __name__ == "__main__":
	main()
