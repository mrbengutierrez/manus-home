
from CheaperManusController import ArmController
import time

def testPositionControl():
	arm = ArmController()
	while(True):
		arm.setPosition(-0.15,0.4)
		time.sleep(5)
		arm.setPosition(0.15,0.4)
		time.sleep(5)
		
		

def main():
	testPositionControl()
	
	
if __name__ == "__main__":
	main()
