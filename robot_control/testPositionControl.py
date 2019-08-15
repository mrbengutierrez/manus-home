
from CheaperManusController import ArmController
import time
import numpy as np

def testPositionControl():
	arm = ArmController()
	while(True):
		arm.setPosition(np.array([-0.15,0.4]))
		time.sleep(5)
		arm.setPosition(np.array([0.15,0.4]))
		time.sleep(5)
		
		

def main():
	testPositionControl()
	
	
if __name__ == "__main__":
	main()
