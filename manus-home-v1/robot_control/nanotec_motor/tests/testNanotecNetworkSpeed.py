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


def speedTest(functionName, functionCall,arguments = []):
	startTime = time.time()
	numCalls = 100
	for _ in range(numCalls):
		result = functionCall(*arguments)
	endTime = time.time()
	totalTime = endTime - startTime
	print("")
	print(functionName)
	print("numCalls: " + str(numCalls))
	print("total time: " + str(totalTime))
	print("time per call: " + str(totalTime/numCalls))	


def main():
	motor = NanotecMotor("/dev/ttyACM0",18)
	
	speedTest("getID",motor.getID)
	speedTest("getSerialPort",motor.getSerialPort)
	
	speedTest("setTorque",motor.setTorque,[0])
	speedTest("setAngularVelocity",motor.setAngularVelocity,[0])
	speedTest("setRelativeAngularPosition",motor.setRelativeAngularPosition,[0])
	speedTest("setAbsoluteAngularPosition",motor.setAbsoluteAngularPosition,[0])
	speedTest("setAbsoluteAngularPositionShortestPath",motor.setAbsoluteAngularPositionShortestPath,[0])
	speedTest("stop",motor.stop)
	
	speedTest("getTorque",motor.getTorque)
	speedTest("getAngularVelocity",motor.getAngularVelocity)
	speedTest("getAbsoluteAngularPosition",motor.getAbsoluteAngularPosition)
	speedTest("readPhysicalEncoder",motor.readPhysicalEncoder)
	

	motor.closePort()
	
	
	
	
	
	
	
	
	


if __name__ == "__main__":
	main()
