"""
This files test the torque of OdriveMotor.py


Author: Benjamin Gutierrez
email: mrbengutierrez@gmail.com
date: 02/03/2020
"""



import sys
sys.path.append("..")

from OdriveMotor import OdriveController
from OdriveMotor import OdriveMotor



def testAngularVelocity():
	"""Tests the torque of the odrive motor"""
	
	motorController = OdriveController()
	motorController.calibrate()
	[leftMotor,rightMotor] = motorController.getMotors()
	
	highTorque = 0.7
	lowTorque = -0.3
	
	import time
	print("")
	
	print("Testing left motor")
	
	print(leftMotor.getTorque())

	print("Testing setTorque(" + str(highTorque) + ")")
	leftMotor.setTorque(highTorque)
	time.sleep(5)
	print(leftMotor.getTorque())
	time.sleep(5)
	
	print("Testing setTorque(" + str(lowTorque) + ")")
	leftMotor.setTorque(lowTorque)
	time.sleep(5)
	print(leftMotor.getTorque())
	time.sleep(5)
	
	leftMotor.stop()
	
	
	print("Testing right motor")
	
	print(rightMotor.getTorque())

	print("Testing setTorque(" + str(highTorque) + ")")
	rightMotor.setTorque(highTorque)
	time.sleep(5)
	print(rightMotor.getTorque())
	time.sleep(5)
	
	print("Testing setTorque(" + str(lowTorque) + ")")
	rightMotor.setTorque(lowTorque)
	time.sleep(5)
	print(rightMotor.getTorque())
	time.sleep(5)
	
	rightMotor.stop()


def main():
	testAngularVelocity()



if __name__ == "__main__":
	main()
