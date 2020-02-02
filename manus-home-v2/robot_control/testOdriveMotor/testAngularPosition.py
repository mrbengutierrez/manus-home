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
	#motorController.calibrate()
	[leftMotor,rightMotor] = motorController.getMotors()
	
	import time
	print("")
	
	print("Testing Left Motor")
	
	print(leftMotor.getAbsoluteAngularPosition())
	print("Setting Angular Position Mode")
	leftMotor.angularPositionMode()
	print(leftMotor.getAbsoluteAngularPosition())

	print("Testing setRelativeAngularPosition(90.0)")
	leftMotor.setRelativeAngularPosition(90.0)
	time.sleep(5)
	print(leftMotor.getAbsoluteAngularPosition())
	
	print("Testing setRelativeAngularPosition(-90.0)")
	leftMotor.setRelativeAngularPosition(-90.0)
	time.sleep(5)
	print(leftMotor.getAbsoluteAngularPosition())
	
	print('Testing setAbsoluteAngularPosition(angPos=180.0, direction="counter-clockwise")')
	leftMotor.setAbsoluteAngularPosition(angPos=180.0, direction="counter-clockwise")
	time.sleep(5)
	print(leftMotor.getAbsoluteAngularPosition())

	print('Testing setAbsoluteAngularPosition(angPos=90.0, direction="clockwise")')	
	leftMotor.setAbsoluteAngularPosition(angPos=90.0, direction="clockwise")
	time.sleep(5)
	print(leftMotor.getAbsoluteAngularPosition())	
	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=270.0)")	
	leftMotor.setAbsoluteAngularPositionShortestPath(angPos=270.0)
	time.sleep(5)
	print(leftMotor.getAbsoluteAngularPosition())
	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=0.0)")
	leftMotor.setAbsoluteAngularPositionShortestPath(angPos=0.0)
	time.sleep(5)
	print(leftMotor.getAbsoluteAngularPosition())	
	
	leftMotor.stop()
	
	print("Testing Right Motor")
	
	print(rightMotor.getAbsoluteAngularPosition())
	print("Setting Angular Position Mode")
	rightMotor.angularPositionMode()
	print(rightMotor.getAbsoluteAngularPosition())

	print("Testing setRelativeAngularPosition(90.0)")
	rightMotor.setRelativeAngularPosition(90.0)
	time.sleep(5)
	print(rightMotor.getAbsoluteAngularPosition())
	
	print("Testing setRelativeAngularPosition(-90.0)")
	rightMotor.setRelativeAngularPosition(-90.0)
	time.sleep(5)
	print(rightMotor.getAbsoluteAngularPosition())
	
	print('Testing setAbsoluteAngularPosition(angPos=180.0, direction="counter-clockwise")')
	rightMotor.setAbsoluteAngularPosition(angPos=180.0, direction="counter-clockwise")
	time.sleep(5)
	print(rightMotor.getAbsoluteAngularPosition())

	print('Testing setAbsoluteAngularPosition(angPos=90.0, direction="clockwise")')	
	rightMotor.setAbsoluteAngularPosition(angPos=90.0, direction="clockwise")
	time.sleep(5)
	print(rightMotor.getAbsoluteAngularPosition())	
	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=270.0)")	
	rightMotor.setAbsoluteAngularPositionShortestPath(angPos=270.0)
	time.sleep(5)
	print(rightMotor.getAbsoluteAngularPosition())
	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=0.0)")
	rightMotor.setAbsoluteAngularPositionShortestPath(angPos=0.0)
	time.sleep(5)
	print(rightMotor.getAbsoluteAngularPosition())	
	
	rightMotor.stop()


def main():
	testAngularPosition()



if __name__ == "__main__":
	main()
