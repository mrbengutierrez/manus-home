"""
This files test the angular velocity of OdriveMotor.py


Author: Benjamin Gutierrez
email: mrbengutierrez@gmail.com
date: 02/03/2020
"""



import sys
sys.path.append("..")

from OdriveMotor import OdriveController
from OdriveMotor import OdriveMotor



def testAngularVelocity():
	"""Tests the angular velocity of the odrive motor"""
	
	motorController = OdriveController()
	#motorController.calibrate()
	[leftMotor,rightMotor] = motorController.getMotors()
	
	import time
	print("")
	
	print("Testing left motor")
	
	print(leftMotor.getAngularVelocity())

	print("Testing setAngularVelocity(50.7)")
	leftMotor.setAngularVelocity(50.7)
	time.sleep(5)
	print(leftMotor.getAngularVelocity())
	time.sleep(5)
	
	print("Testing setAngularVelocity(-10.0)")
	leftMotor.setAngularVelocity(-10.0)
	time.sleep(5)
	print(leftMotor.getAngularVelocity())
	time.sleep(5)
	
	leftMotor.stop()
	
	
	print("Testing right motor")
	
	print(rightMotor.getAngularVelocity())

	print("Testing setAngularVelocity(50.7)")
	rightMotor.setAngularVelocity(50.7)
	time.sleep(5)
	print(rightMotor.getAngularVelocity())
	time.sleep(5)
	
	print("Testing setAngularVelocity(-10.0)")
	rightMotor.setAngularVelocity(-10.0)
	time.sleep(5)
	print(rightMotor.getAngularVelocity())
	time.sleep(5)
	
	rightMotor.stop()


def main():
	testAngularVelocity()



if __name__ == "__main__":
	main()
