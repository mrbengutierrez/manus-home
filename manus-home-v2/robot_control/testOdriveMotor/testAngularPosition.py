"""
This files test the angular position of OdriveMotor.py


Author: Benjamin Gutierrez
email: mrbengutierrez@gmail.com
date: 02/01/2020
"""



import sys
sys.path.append("..")

from OdriveMotor import OdriveController
from OdriveMotor import OdriveMotor



def testAngularPosition():
	"""Tests the angular position of the odrive motor"""
	
	motorController = OdriveController()
	motorController.calibrate()
	[leftMotor,rightMotor] = motorController.getMotors()
	
	import time
	shortDelay = 2
	longDelay = 7
	print("")
	
	print("Testing Left Motor")
	
	print(leftMotor.getAbsoluteAngularPosition())

	print("")
	print("Testing setRelativeAngularPosition(90.0)")
	leftMotor.setRelativeAngularPosition(90.0)
	time.sleep(shortDelay)
	print(leftMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)
	
	print("")
	print("Testing setRelativeAngularPosition(-90.0)")
	leftMotor.setRelativeAngularPosition(-90.0)
	time.sleep(shortDelay)
	print(leftMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)
	
	print("")
	print('Testing setAbsoluteAngularPosition(angPos=180.0, direction="counter-clockwise")')
	leftMotor.setAbsoluteAngularPosition(angPos=180.0, direction="counter-clockwise")
	time.sleep(shortDelay)
	print(leftMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)

	print("")
	print('Testing setAbsoluteAngularPosition(angPos=0.0, direction="clockwise")')	
	leftMotor.setAbsoluteAngularPosition(angPos=0.0, direction="clockwise")
	time.sleep(shortDelay)
	print(leftMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)	

	print("")	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=270.0)")	
	leftMotor.setAbsoluteAngularPositionShortestPath(angPos=270.0)
	time.sleep(shortDelay)
	print(leftMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)

	print("")	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=0.0)")
	leftMotor.setAbsoluteAngularPositionShortestPath(angPos=0.0)
	time.sleep(shortDelay)
	print(leftMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)	

	print("")	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=90.0)")	
	leftMotor.setAbsoluteAngularPositionShortestPath(angPos=90.0)
	time.sleep(shortDelay)
	print(leftMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)

	print("")	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=0.0)")
	leftMotor.setAbsoluteAngularPositionShortestPath(angPos=0.0)
	time.sleep(shortDelay)
	print(leftMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)		

	print("")	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=-90.0)")	
	leftMotor.setAbsoluteAngularPositionShortestPath(angPos=-90.0)
	time.sleep(shortDelay)
	print(leftMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)

	print("")	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=0.0)")
	leftMotor.setAbsoluteAngularPositionShortestPath(angPos=0.0)
	time.sleep(shortDelay)
	print(leftMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)	
	
	leftMotor.stop()
	
	print("Testing Right Motor")
	
	print(rightMotor.getAbsoluteAngularPosition())

	print("")
	print("Testing setRelativeAngularPosition(90.0)")
	rightMotor.setRelativeAngularPosition(90.0)
	time.sleep(shortDelay)
	print(rightMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)

	print("")	
	print("Testing setRelativeAngularPosition(-90.0)")
	rightMotor.setRelativeAngularPosition(-90.0)
	time.sleep(shortDelay)
	print(rightMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)

	print("")	
	print('Testing setAbsoluteAngularPosition(angPos=180.0, direction="counter-clockwise")')
	rightMotor.setAbsoluteAngularPosition(angPos=180.0, direction="counter-clockwise")
	time.sleep(shortDelay)
	print(rightMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)

	print("")
	print('Testing setAbsoluteAngularPosition(angPos=0.0, direction="clockwise")')	
	rightMotor.setAbsoluteAngularPosition(angPos=0.0, direction="clockwise")
	time.sleep(shortDelay)
	print(rightMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)

	print("")	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=270.0)")	
	rightMotor.setAbsoluteAngularPositionShortestPath(angPos=270.0)
	time.sleep(shortDelay)
	print(rightMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)

	print("")	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=0.0)")
	rightMotor.setAbsoluteAngularPositionShortestPath(angPos=0.0)
	time.sleep(shortDelay)
	print(rightMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)

	print("")	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=90.0)")	
	rightMotor.setAbsoluteAngularPositionShortestPath(angPos=90.0)
	time.sleep(shortDelay)
	print(rightMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)

	print("")	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=0.0)")
	rightMotor.setAbsoluteAngularPositionShortestPath(angPos=0.0)
	time.sleep(shortDelay)
	print(rightMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)	

	print("")	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=-90.0)")	
	rightMotor.setAbsoluteAngularPositionShortestPath(angPos=-90.0)
	time.sleep(shortDelay)
	print(rightMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)

	print("")	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=0.0)")
	rightMotor.setAbsoluteAngularPositionShortestPath(angPos=0.0)
	time.sleep(shortDelay)
	print(rightMotor.getAbsoluteAngularPosition())
	time.sleep(longDelay)	
		
	rightMotor.stop()


def main():
	testAngularPosition()



if __name__ == "__main__":
	main()
