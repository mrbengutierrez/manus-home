
from CheaperManusController import ArmController
import time
import numpy as np

def printRobotInformation(arm):
	print("joint angles (deg)" + str(list(arm.getJointAngles()*180.0/np.pi)))
	print("position (m): " + str(list(arm.getPosition())))
	print("velocity (m/s): " + str(list(arm.getVelocity())))
	print("force (N): " + str(list(arm.getForce())))
	print("")
	
def testReadout():
	arm = ArmController()
	while(True):
		printRobotInformation(arm)
		time.sleep(5)
		

def main():
	testReadout()
	
	
if __name__ == "__main__":
	main()
