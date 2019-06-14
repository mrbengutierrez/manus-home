#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
This library provides an interface between a python file and the nanotec motors.
This library should provide the same functionality as described in the Nanotec.h file.

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

import ctypes # Python standard library for managing Python to c interfacing

# Shared C Library for the NanotecMotor.cpp
sharedCLibrary = ctypes.cdll.LoadLibrary('./nanotec-motor/NanotecMotor.so')


class NanotecMotor(object):
	
	
	def __init__(self, serialPort, ID):
		""" Initializes a new Nanotec Motor "
		
			Parameters:
			serialPort (string): name of the port that the motor is connected to
			ID (int): (optional) a unique number to identify the motor.
			
			Returns:
			nothing
		"""
		
		
		#Initial variables for NanotecMotor.h public functions
		
		# Constructor parameters
		sharedCLibrary.NanotecMotor_new.argtypes = [ctypes.c_char_p,ctypes.c_int]
		sharedCLibrary.NanotecMotor_new.restype = ctypes.c_void_p
		
		
		# Method to get the ID number of the motor
		
		# getID parameters
		sharedCLibrary.NanotecMotor_getID.argtypes = []
		sharedCLibrary.NanotecMotor_getID.restype = ctypes.c_int
		
		
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
		"""Returns the ID number of the motor
		
			Returns:
			int: value of of ID number of motor 
		"""
		return sharedCLibrary.NanotecMotor_getID(self.obj)
	
	
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
		return sharedCLibrary.NanotecMotor_torqueMode(self.obj, torque, maxTorque, maxCurr, nomCurr, slope)
		
	def angularVelocityMode(self,angVel = 0):
		"""Method to activate the angular velocity control
		
			Parameters:
			angVel (int): angualr velocity in rpm
			
			Returns:
			None
		"""
		return sharedCLibrary.NanotecMotor_angularVelocityMode(self.obj, angVel)
		
	
	def angularPositionMode(self, angPos = 0.0, angVel = 200):
		"""Method to activate the angular position control
			
			Parameters:
			angPos (double): angular position value (negative to reverse direction)
							(-360.0 <= angPos <= 360.0)
			angVel (int): angular velocity value in rpm (must always be positive)
			
			Returns:
			None
		"""
		return sharedCLibrary.NanotecMotor_angularPositionMode(self.obj, angPos, angVel)
	
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
		return sharedCLibrary.NanotecMotor_setTorque(self.obj, torque)

	
	def setAngularVelocity(self, angVel):
		"""Method to change the angular velocity value in real time
		
			Parameters:
			angVel (int): Angular velocity in rpm
			
			Returns
			None
		"""
		return sharedCLibrary.NanotecMotor_setAngularVelocity(self.obj, angVel)
	
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
		return sharedCLibrary.NanotecMotor_setRelativeAngularPosition(self.obj, angPos, angVel)
		

	
	def setAbsoluteAngularPosition(self, angPos, angVel = 200):
		"""Method to change the absolute angular position value in real time with ability to control direction.
		
			Parameters:
			angPos (double): angular position value in degrees (negative to reverse direction)
						(-360.0 <= angPos <= 360.0)
			angVel (int): angular velocity value in rpm (must always be positive)
			
			Returns:
			None
		"""
		return sharedCLibrary.NanotecMotor_setAbsoluteAngularPosition(self.obj, angPos, angVel)
	
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
		return sharedCLibrary.NanotecMotor_setAbsoluteAngularPositionShortestPath(self.obj, angPos, angVel)
	
	def stop(self):
		"""Method that sends the commands to stop the motor.
		
			Returns:
			None	
		"""
		return sharedCLibrary.NanotecMotor_stop(self.obj)
	
	def getTorque(self):
		"""Returns the torque as thousandths of the torque
		
			Returns:
			int: value of the angular torque as thousandths of the torque,
				 e.g., the value "500" means "50%" of the rated torque;
				 (0 <= value <= 1000)
		"""
		return sharedCLibrary.NanotecMotor_getTorque(self.obj)
	
	def getAngularVelocity(self):
		"""Returns the current angular velocity in rpm
		
			Returns:
			int: current angular velocity in rpm
		"""
		return sharedCLibrary.NanotecMotor_getAngularVelocity(self.obj)
	
	def getAbsoluteAngularPosition(self):
		"""Returns the absolute angular position of the motor shaft in degrees
		
			Returns:
			double: absolute angular position of the motor shaft in degrees
					(0.0 <= output < 360.0)
		"""
		return sharedCLibrary.NanotecMotor_getAbsoluteAngularPosition(self.obj)
		
		
	def readPhysicalEncoder(self):
		"""Reads the value of the encoder
		
			Returns:
			int: value of the encoder
				(0 <= value <= 4095)
		"""
		return sharedCLibrary.NanotecMotor_readPhysicalEncoder(self.obj)
	
	def closePort(self):
		"""Method to close the port of the serial communication.
		
			Returns:
			None
		"""
		return sharedCLibrary.NanotecMotor_closePort(self.obj)
	
	
		
		







def main():
	"""This main method was used to test the nanotec motors to make sure that they work.
	
		Feel free to comment this method out. This library will work without it.
	"""
	
	

if __name__ == "__main__":
	main()
	
