#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This library provides an interface between a python file and the nanotec motors.
The interface should provide the same functionality as described in the Nanotec.h file.

There are three implementations fo the NanotecMotor interface:
NanotecWrapper
NanotecSharedMemory
NanotecClient
"""




# Use abstract base class for interface
from abc import ABCMeta, abstractmethod


class NanotecMotorAbstract:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, serialPort, ID):
		""" Initializes a new Nanotec Motor "
		
			Parameters:
			serialPort (string): name of the port that the motor is connected to
			ID (int): (optional) a unique number to identify the motor.
			
			Returns:
			nothing
		"""
		raise NotImplementedError
	
	@abstractmethod
	def getID(self):
		"""Returns the ID number of the motor
		
			Returns:
			int: value of of ID number of motor 
		"""
		raise NotImplementedError
		
	@abstractmethod
	def getSerialPort(self):
		"""Returns the serial port of the motor is connected to
		
			Returns:
			string: serial port that the motor is connected to
		"""
		raise NotImplementedError
		
	@abstractmethod
	def torqueMode(self,torque = 0, maxTorque = 1000, maxCurr = 1800, nomCurr = 1800, slope = 1000):
		"""Method to activate the Profile Torque or torque profile.
		
			Parameters:
			torque (int):  Torque value in percentage (decimal value 0-1000=100%)
			maxTorque (int):  Maximum torque in percentage (decimal value 0-1000=100%)
			maxCurr (int):  Maximum current, commonly 1800 mA
			nomCurr (int):  Nominal current, commonly 1800 mA
			slope (int): Slope to arrive to the torque, 1000 means go directly
			
			Returns:
			None
		"""
		raise NotImplementedError
	
	@abstractmethod	
	def angularVelocityMode(self,angVel = 0):
		"""Method to activate the angular velocity control
		
			Parameters:
			angVel (int): angualr velocity in rpm
			
			Returns:
			None
		"""
		raise NotImplementedError
		
	@abstractmethod
	def angularPositionMode(self, angPos = 0.0, angVel = 200):
		"""Method to activate the angular position control
			
			Parameters:
			angPos (double): angular position value (negative to reverse direction)
							(-360.0 <= angPos <= 360.0)
			angVel (int): angular velocity value in rpm (must always be positive)
			
			Returns:
			None
		"""
		raise NotImplementedError
	
	@abstractmethod
	def setTorque(self, torque):
		"""Method to activate the Profile Torque or torque profile.

			Parameters:
			torque (int): Torque value in percentage (decimal value 0-1000=100%)
			maxTorque (int):  Maximum torque in percentage (decimal value 0-1000=100%)
			maxCurr (int): Maximum current, commonly 1800 mA
			nomCurr (int):  Nominal current, commonly 1800 mA
			slope (int): Slope to arrive to the torque, 1000 means go directly
			
			Returns:
			None
		"""
		raise NotImplementedError

	
	@abstractmethod
	def setAngularVelocity(self, angVel):
		"""Method to change the angular velocity value in real time
		
			Parameters:
			angVel (int): Angular velocity in rpm
			
			Returns
			None
		"""
		raise NotImplementedError
	
	@abstractmethod
	def setRelativeAngularPosition(self, angPos, angVel = 200):
		"""Method to change the relative angular position value in real time. 
			The position is set using the current position as the zero position.
			
			Parameters:
			angPos (double): angular position value in degrees (negative to reverse direction)
							(-360.0 <= angPos <= 360.0)
			angVel (int): angular velocity value in rpm (must always be positive)
			
			Returns:
			None
		"""
		raise NotImplementedError
		
	@abstractmethod
	def setAbsoluteAngularPosition(self, angPos, angVel = 200):
		"""Method to change the absolute angular position value in real time with ability to control direction.
		
			Parameters:
			angPos (double): angular position value in degrees (negative to reverse direction)
						(-360.0 <= angPos <= 360.0)
			angVel (int): angular velocity value in rpm (must always be positive)
			
			Returns:
			None
		"""
		raise NotImplementedError
	
	@abstractmethod
	def setAbsoluteAngularPositionShortestPath(self, angPos,angVel = 200):
		"""Method to change the absolute angular position value in real time. 
			Motor rotates in the shortest path to new target angular position.
			
			Parameters:
			angPos (double): angular position value in degrees (must always be positive)
							(0.0 <= angPos <= 360.0)
			angVel (int): angular velocity value in rpm (must always be positive)
			
			Returns:
			None
		"""
		raise NotImplementedError
	
	@abstractmethod
	def stop(self):
		"""Method that sends the commands to stop the motor.
		
			Returns:
			None	
		"""
		raise NotImplementedError
	
	@abstractmethod
	def getTorque(self):
		"""Returns the torque as thousandths of the torque
		
			Returns:
			int: value of the angular torque as thousandths of the torque,
				 e.g., the value "500" means "50%" of the rated torque;
				 (0 <= value <= 1000)
		"""
		raise NotImplementedError
	
	@abstractmethod
	def getAngularVelocity(self):
		"""Returns the current angular velocity in rpm
		
			Returns:
			int: current angular velocity in rpm
		"""
		raise NotImplementedError
	
	@abstractmethod
	def getAbsoluteAngularPosition(self):
		"""Returns the absolute angular position of the motor shaft in degrees
		
			Returns:
			double: absolute angular position of the motor shaft in degrees
					(0.0 <= output < 360.0)
		"""
		raise NotImplementedError
		
	
	@abstractmethod	
	def readPhysicalEncoder(self):
		"""Reads the value of the encoder
		
			Returns:
			int: value of the encoder
				(0 <= value <= 4095)
		"""
		raise NotImplementedError
	
	@abstractmethod
	def closePort(self):
		"""Method to close the port of the serial communication.
		
			Returns:
			None
		"""
		raise NotImplementedError









#--------------------------------------------------------------------------------------------------------------------------------------
'''
Nanotec Wrapper

The NanotecWrapper class directly communicates between a NanotecMotor.h
using the ctypes python standard library

Author: Benjamin Gutierrez
Date: 06/11/2019

ctypes Translation table for some Python and C/C++ types
Python												C type
None 												NULL 	 
ctypes.char_p 										char* 	 
ctypes.c_int 										int 		No need to cast
ctypes.c_longlong 									long long 	 
ctypes.c_double 									double 	 
numpy.ctypeslib.ndpointer(dtype=numpy.float64)] 	double* 	pass a numpy array of type numpy.float64
numpy.ctypeslib.ndpointer(dtype=numpy.int32)] 		int* 		pass a numpy array of type numpy.int32
ctypes.byref(...) 									& 			pass by reference (suitable for arguments returning results)

'''
import os
import glob
import ctypes # Python standard library for managing Python to c interfacing


def findFileInSubdirectories(filename):
	"""Finds a file recursively in the subdirectories"""
	for root, dirs, files in os.walk("/"):
		for file in files:
			if "NanotecMotor.so" in file:
				return os.path.join(root,file)

# Shared C Library for the NanotecMotor.cpp
sharedCLibraryLocation = findFileInSubdirectories("NanotecMotor.so")
#print("sharedCLibraryLocation: " + str(sharedCLibraryLocation))
sharedCLibrary = ctypes.cdll.LoadLibrary(sharedCLibraryLocation)


	


class NanotecWrapper(NanotecMotorAbstract):
	
	
	def __init__(self, serialPort, ID):		
		
		#Initial variables for NanotecMotor.h public functions
		
		# Constructor parameters
		sharedCLibrary.NanotecMotor_new.argtypes = [ctypes.c_char_p,ctypes.c_int]
		sharedCLibrary.NanotecMotor_new.restype = ctypes.c_void_p
		
		
		# Method to get the ID number & serialport of the motor
		
		# getID parameters
		sharedCLibrary.NanotecMotor_getID.argtypes = []
		sharedCLibrary.NanotecMotor_getID.restype = ctypes.c_int
		
		# getSerialPort parameters
		sharedCLibrary.NanotecMotor_getSerialPort.argtypes = []
		sharedCLibrary.NanotecMotor_getSerialPort.restype = ctypes.c_char_p
		
		
		# Modes of Operation
		
		# torqueMode parameters
		sharedCLibrary.NanotecMotor_torqueMode.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
		sharedCLibrary.NanotecMotor_torqueMode.restype = ctypes.c_void_p
		
		# angularVelocityMode parameters
		sharedCLibrary.NanotecMotor_angularVelocityMode.argtypes = [ctypes.c_int]
		sharedCLibrary.NanotecMotor_angularVelocityMode.restype = ctypes.c_void_p
		
		# angularPositionMode parameters
		sharedCLibrary.NanotecMotor_angularPositionMode.argtypes = [ctypes.c_int, ctypes.c_double]
		sharedCLibrary.NanotecMotor_angularPositionMode.restype = ctypes.c_void_p
		
		
		# Methods to control motor
		
		# setTorque parameters
		sharedCLibrary.NanotecMotor_setTorque.argtypes = [ctypes.c_int]
		sharedCLibrary.NanotecMotor_setTorque.restype = ctypes.c_void_p
		
		# setAngularVelocity parameters
		sharedCLibrary.NanotecMotor_setAngularVelocity.argtypes = [ctypes.c_int]
		sharedCLibrary.NanotecMotor_setAngularVelocity.restype = ctypes.c_void_p
		
		# setRelativeAngularPosition parameters
		sharedCLibrary.NanotecMotor_setRelativeAngularPosition.argtypes = [ctypes.c_int, ctypes.c_double]
		sharedCLibrary.NanotecMotor_setRelativeAngularPosition.restype = ctypes.c_void_p
		
		# setAbsoluteAngularPosition parameters
		sharedCLibrary.NanotecMotor_setAbsoluteAngularPosition.argtypes = [ctypes.c_int, ctypes.c_double]
		sharedCLibrary.NanotecMotor_setAbsoluteAngularPosition.restype = ctypes.c_void_p
		
		# setAbsoluteAngularPositionShortestPath parameters
		sharedCLibrary.NanotecMotor_setAbsoluteAngularPositionShortestPath.argtypes = [ctypes.c_int, ctypes.c_double]
		sharedCLibrary.NanotecMotor_setAbsoluteAngularPositionShortestPath.restype = ctypes.c_void_p

		# stop parameters
		sharedCLibrary.NanotecMotor_stop.argtypes = []
		sharedCLibrary.NanotecMotor_stop.restype = ctypes.c_void_p
		
		# Methods to get information from the motor
		
		# getTorque parameters
		sharedCLibrary.NanotecMotor_getTorque.argtypes = []
		sharedCLibrary.NanotecMotor_getTorque.restype = ctypes.c_int
		
		# getAngularVelocity parameters
		sharedCLibrary.NanotecMotor_getAngularVelocity.argtypes = []
		sharedCLibrary.NanotecMotor_getAngularVelocity.restype = ctypes.c_int
		
		# getAbsoluteAngularPosition parameters
		sharedCLibrary.NanotecMotor_getAbsoluteAngularPosition.argtypes = []
		sharedCLibrary.NanotecMotor_getAbsoluteAngularPosition.restype = ctypes.c_double
		
		# readPhysicalEncoder parameters
		sharedCLibrary.NanotecMotor_readPhysicalEncoder.argtypes = []
		sharedCLibrary.NanotecMotor_readPhysicalEncoder.restype = ctypes.c_int
		
		# Method to close the serial port connection
		sharedCLibrary.NanotecMotor_closePort.argtypes = []
		sharedCLibrary.NanotecMotor_closePort.restype = ctypes.c_void_p
		
		

		# Initialize a new Nanotec Motor
		
		# This object contains the information for this nanotecmotor
		bytesSerialPort = serialPort.encode('ascii') # converts to bytes
		charPointerSerialPort = ctypes.c_char_p(bytesSerialPort) # convert to ctypes char*
		
		# This object contains the information for this nanotec motor
		self.obj = sharedCLibrary.NanotecMotor_new(charPointerSerialPort,ID)	
		
		
	def getID(self):
		return sharedCLibrary.NanotecMotor_getID(self.obj)
	
	def getSerialPort(self):
		return sharedCLibrary.NanotecMotor_getSerialPort(self.obj).decode("ascii")
		
	def torqueMode(self,torque = 0, maxTorque = 1000, maxCurr = 1800, nomCurr = 1800, slope = 1000):
		return sharedCLibrary.NanotecMotor_torqueMode(self.obj, torque, maxTorque, maxCurr, nomCurr, slope)
		
	def angularVelocityMode(self,angVel = 0):
		return sharedCLibrary.NanotecMotor_angularVelocityMode(self.obj, angVel)
		
	def angularPositionMode(self, angPos = 0.0, angVel = 200):
		return sharedCLibrary.NanotecMotor_angularPositionMode(self.obj, angPos, angVel)
	
	def setTorque(self, torque):
		return sharedCLibrary.NanotecMotor_setTorque(self.obj, torque)
	
	def setAngularVelocity(self, angVel):
		return sharedCLibrary.NanotecMotor_setAngularVelocity(self.obj, angVel)
	
	def setRelativeAngularPosition(self, angPos, angVel = 200):
		return sharedCLibrary.NanotecMotor_setRelativeAngularPosition(self.obj, angPos, angVel)
		
	def setAbsoluteAngularPosition(self, angPos, angVel = 200):
		return sharedCLibrary.NanotecMotor_setAbsoluteAngularPosition(self.obj, angPos, angVel)
	
	def setAbsoluteAngularPositionShortestPath(self, angPos,angVel = 200):
		return sharedCLibrary.NanotecMotor_setAbsoluteAngularPositionShortestPath(self.obj, angPos, angVel)
	
	def stop(self):
		return sharedCLibrary.NanotecMotor_stop(self.obj)
	
	def getTorque(self):
		return sharedCLibrary.NanotecMotor_getTorque(self.obj)
	
	def getAngularVelocity(self):
		return sharedCLibrary.NanotecMotor_getAngularVelocity(self.obj)
	
	def getAbsoluteAngularPosition(self):
		return sharedCLibrary.NanotecMotor_getAbsoluteAngularPosition(self.obj)
				
	def readPhysicalEncoder(self):
		return sharedCLibrary.NanotecMotor_readPhysicalEncoder(self.obj)
	
	def closePort(self):
		return sharedCLibrary.NanotecMotor_closePort(self.obj)
	
	
		














#--------------------------------------------------------------------------------------------------------------------------------------
'''
NanotecClient

The NanotecClient class provides the parsing functionality to other clients

Author: Benjamin Gutierrez
Date: 07/08/2019
'''

class NanotecClient(NanotecMotorAbstract):
	def __init__(self,serialPort,ID = 0):
		"""Initializes the client"""
		raise NotImplementedError
		
	def sendInstruction(self,instruction):
		"""Sends an instruction using shared memory
		
			Parameters:
			instruction (string): instruction to be sent
									Format: "function_name,arg1,arg2,..." 
  									If "function_name" represents an instance of a nanotec motor, 
									"arg1" must be the serial port of that motor
			
			Return:
			(string): string representation of return value from the corresponding function in NanotecMotor
		"""
		raise NotImplementedError
		
	@staticmethod
	def argumentsToString(listOfArguments,delimiter = ","):
		argumentString = ""
		for i in range(len(listOfArguments)):
			if i == 0: # don't add delimiter to first arguments
				argumentString += str(listOfArguments[i])
			else:
				argumentString += delimiter + str(listOfArguments[i])
		return argumentString	

	def getID(self):
		instruction = NanotecSharedMemoryClient.argumentsToString(["getID",self.serialPort])
		result = self.sendInstruction(instruction)
		return int(result)
		
	def getSerialPort(self):
		instruction = NanotecSharedMemoryClient.argumentsToString(["getSerialPort",self.serialPort])
		result = self.sendInstruction(instruction)
		return str(result)
		
	def torqueMode(self,torque = 0, maxTorque = 1000, maxCurr = 1800, nomCurr = 1800, slope = 1000):
		instruction = NanotecSharedMemoryClient.argumentsToString(["torqueMode",self.serialPort,torque,maxTorque,maxCurr,nomCurr,slope])
		result = self.sendInstruction(instruction)
		return None
		
	def angularVelocityMode(self,angVel = 0):
		instruction = NanotecSharedMemoryClient.argumentsToString(["angularVelocityMode",self.serialPort,angVel])
		result = self.sendInstruction(instruction)
		return None
		
	def angularPositionMode(self, angPos = 0.0, angVel = 200):
		instruction = NanotecSharedMemoryClient.argumentsToString(["angularPositionMode",self.serialPort,angPos,angVel])
		result = self.sendInstruction(instruction)
		return None
	
	def setTorque(self, torque):
		instruction = NanotecSharedMemoryClient.argumentsToString(["setTorque",self.serialPort,torque])
		result = self.sendInstruction(instruction)
		return None
	
	def setAngularVelocity(self, angVel):
		instruction = NanotecSharedMemoryClient.argumentsToString(["setAngularVelocity",self.serialPort,angVel])
		result = self.sendInstruction(instruction)
		return None
	
	def setRelativeAngularPosition(self, angPos, angVel = 200):
		instruction = NanotecSharedMemoryClient.argumentsToString(["setRelativeAngularPosition",self.serialPort,angPos,angVel])
		result = self.sendInstruction(instruction)
		return None
		
	def setAbsoluteAngularPosition(self, angPos, angVel = 200):
		instruction = NanotecSharedMemoryClient.argumentsToString(["setAbsoluteAngularPosition",self.serialPort,angPos,angVel])
		result = self.sendInstruction(instruction)
		return None
	
	def setAbsoluteAngularPositionShortestPath(self, angPos,angVel = 200):
		instruction = NanotecSharedMemoryClient.argumentsToString(["setAbsoluteAngularPositionShortestPath",self.serialPort,angPos,angVel])
		result = self.sendInstruction(instruction)
		return None
	
	def stop(self):
		instruction = NanotecSharedMemoryClient.argumentsToString(["stop",self.serialPort])
		result = self.sendInstruction(instruction)
		return None
	
	def getTorque(self):
		instruction = NanotecSharedMemoryClient.argumentsToString(["getTorque",self.serialPort])
		result = self.sendInstruction(instruction)
		return int(result)
	
	def getAngularVelocity(self):
		instruction = NanotecSharedMemoryClient.argumentsToString(["getAngularVelocity",self.serialPort])
		result = self.sendInstruction(instruction)
		return int(result)
	
	def getAbsoluteAngularPosition(self):
		instruction = NanotecSharedMemoryClient.argumentsToString(["getAbsoluteAngularPosition",self.serialPort])
		result = self.sendInstruction(instruction)
		return float(result)
				
	def readPhysicalEncoder(self):
		instruction = NanotecSharedMemoryClient.argumentsToString(["readPhysicalEncoder",self.serialPort])
		result = self.sendInstruction(instruction)
		return int(result)
	
	def closePort(self):
		instruction = NanotecSharedMemoryClient.argumentsToString(["closePort",self.serialPort])
		result = self.sendInstruction(instruction)
		return None








#--------------------------------------------------------------------------------------------------------------------------------------
'''
NanotecSharedMemoryClient
The NanotecSharedMemory class directly communicates between NanotecMotor.h using shared memory
Author: Benjamin Gutierrez
Date: 07/03/2019
'''

import sysv_ipc # shared memory module
import time
class NanotecSharedMemoryClient(NanotecClient):
	
	def __init__(self,serialPort,ID = 0):
		"""Initializes the status and data memory"""
		self.dataMemory = sysv_ipc.SharedMemory(65)
		self.statusMemory = sysv_ipc.SharedMemory(88)
		
		instruction = NanotecSharedMemoryClient.argumentsToString(["NanotecMotor",serialPort,ID])
		self.serialPort = self.sendInstruction(instruction)
		return
	
	@staticmethod
	def readMemory(memory): # static method
		"""Reads a shared memory location
		
		Parameters:
		memory (sysv_ipc.SharedMemory): shared memory object
		
		Returns:
		(string): string representation of the data in the shared memory location
		"""
		# Read value from shared memory
		memoryValue = memory.read()
		# Find the 'end' of the string and strip
		i = memoryValue.find(ord('\0'))
		if i != -1:
			memoryValue = memoryValue[:i]
		else:
			errorMessage = "i: " + str(i) + " should be -1 to have read \0 in memory location"
			raise ValueError(errorMessage)
		return str(memoryValue.decode('ascii'))
	
	@staticmethod
	def writeMemory(memory,message): # static method
		"""Writes to a shared memory location
		
		Parameters:
		memory (sysv_ipc.SharedMemory): shared memory object
		message (string): message to write to shared memory
		
		Returns:
		None
		"""
		message += chr(0)
		bytesMessage = message.encode('ascii')
		memory.write(bytesMessage)
		return
		
	def sendInstruction(self,instruction):
		startMessage = "start"
		endMessage = "end"
		
		# make sure no other NanotecSharedMemoryClients are writing to memory
		while(NanotecSharedMemoryClient.readMemory(self.statusMemory) == startMessage ):
			pass
		
		NanotecSharedMemoryClient.writeMemory(self.dataMemory,instruction)
		NanotecSharedMemoryClient.writeMemory(self.statusMemory,startMessage)
		
		# wait for instruction to be executed
		currentStatus = NanotecSharedMemoryClient.readMemory(self.statusMemory)
		while ( currentStatus != endMessage):
			currentStatus = NanotecSharedMemoryClient.readMemory(self.statusMemory)

		returnString = NanotecSharedMemoryClient.readMemory(self.dataMemory)
		return returnString

























#--------------------------------------------------------------------------------------------------------------------------------------
'''
NanotecNetworkClient

The NanotecNetworkClient class communicates between NanotecMotor.h using a port

Author: Benjamin Gutierrez
Date: 07/08/2019
'''

import socket


class NanotecNetworkClient(NanotecClient):
	
	def __init__(self,serialPort,ID = 0):
		"""Initializes the port and a new nanotec motor"""
		host = '127.0.0.1'  # The server's hostname or IP address
		port = 8888        # The port used by the server
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create new socket object using TCP protocol
		
		self.socket.connect((host,port)) # connect to server
			
		
		instruction = NanotecSharedMemoryClient.argumentsToString(["NanotecMotor",serialPort,ID])
		self.serialPort = self.sendInstruction(instruction)
		return
	

	
		
	def sendInstruction(self,instruction):
		instruction += chr(0) # '\0' represents end of string in char array for c++
		bytesInstruction = instruction.encode('ascii')
		self.socket.sendall(bytesInstruction)
		
		result = self.socket.recv(1024)
		resultString = result.decode('ascii')
		#print("resultString: " + resultString) # for debugging
		return resultString

		
		
		
		
		
			












		







def main():
	"""This main method was used to test the nanotec motors to make sure that they work.
	
		Feel free to comment this method out. This library will work without it.
	"""
	import time
	motor = NanotecWrapper("/dev/ttyACM0",18)
	
	
	
	startTime = time.time()
	numCalls = 1000
	serialPort = ""
	for _ in range(numCalls):
		serialPort = motor.getSerialPort()
	endTime = time.time()
	totalTime = endTime - startTime
	print("")
	print("serialPort Call: " + serialPort )
	print("numCalls: " + str(numCalls))
	print("total time: " + str(totalTime))
	print("time per call: " + str(totalTime/numCalls))
	
	
	startTime = time.time()
	numCalls = 1000
	for _ in range(numCalls):
		position = motor.getAbsoluteAngularPosition()
	endTime = time.time()
	totalTime = endTime - startTime
	print("")
	print("Position Call")
	print("numCalls: " + str(numCalls))
	print("total time: " + str(totalTime))
	print("time per call: " + str(totalTime/numCalls))
	

if __name__ == "__main__":
	main()
	
