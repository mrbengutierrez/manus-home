'''
Manual tests to test NanotecLibrary.py

Full partition tests are not done. Only typical use cases are tested.
'''


sleepTime = 5

import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('../')

from NanotecLibrary import NanotecNetworkClient as NanotecMotor
#from NanotecLibrary import NanotecSharedMemoryServer as NanotecServer

import time

def printMotorsInformation(motors):
	time.sleep(1)
	for motor in motors:
		printMotorInformation(motor)
	return

def printMotorInformation(motor):
	print("")
	print("MotorID: " + str(motor.getID()))
	print("encoder value: " + str(motor.readPhysicalEncoder()))
	print("torque: " + str(motor.getTorque()))
	print("angular velocity: " + str(motor.getAngularVelocity()))
	print("angular position: " + str(motor.getAbsoluteAngularPosition()))
	return


def testAngularPosition(motors):
	
	for motor in motors:
		motor.angularPositionMode()
	printMotorsInformation(motors)
	
	for motor in motors:
		motor.setAbsoluteAngularPosition(90.0)
	printMotorsInformation(motors)
	time.sleep(sleepTime)
	
	for motor in motors:
		motor.setRelativeAngularPosition(360.0)	
	printMotorsInformation(motors)
	time.sleep(sleepTime)
	
	for motor in motors:
		motor.setAbsoluteAngularPositionShortestPath(0.0)
	printMotorsInformation(motors)	
	time.sleep(sleepTime)
	
	return

def testAngularVelocity(motors):
	
	for motor in motors:
		motor.angularVelocityMode()
	printMotorsInformation(motors)	
	
	for motor in motors:
		motor.setAngularVelocity(100)
	printMotorsInformation(motors)
	time.sleep(sleepTime)

	for motor in motors:
		motor.setAngularVelocity(-100)
	printMotorsInformation(motors)
	time.sleep(sleepTime)	
	
	for motor in motors:
		motor.setAngularVelocity(0)
	printMotorsInformation(motors)
	time.sleep(sleepTime)
	
	return
	
def testTorque(motors):
	
	for motor in motors:
		motor.torqueMode()
	printMotorsInformation(motors)
	
	for motor in motors:
		motor.setTorque(100)
	printMotorsInformation(motors)
	time.sleep(sleepTime)
	
	for motor in motors:
		motor.setTorque(-100)
	printMotorsInformation(motors)
	time.sleep(sleepTime)
	
	return
		
	


def main():
	#Server = NanotecServer()
	#Server.startServer()
	
	serialPort0 = "/dev/ttyACM0"
	ID0 = 1
	firstMotor = NanotecMotor(serialPort0,ID0)
	
	serialPort1 = "/dev/ttyACM1"
	ID1 = 2
	secondMotor = NanotecMotor(serialPort1, ID1)	
	
	motors = [firstMotor,secondMotor]
	
	#firstMotor.setAbsoluteAngularPosition(90.0)
	#time.sleep(5)

	print("Position")
	testAngularPosition(motors)
	print("Velocity")
	testAngularVelocity(motors)
	print("Torque")
	testTorque(motors)
	
	# stop motors and close serial ports
	for motor in motors:
		motor.stop()
		motor.closePort()
	#Server.closeServer()
	
	
	
	
	
	
	


if __name__ == "__main__":
	main()
