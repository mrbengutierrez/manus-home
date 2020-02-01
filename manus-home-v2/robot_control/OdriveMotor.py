"""
This file acts as an object to interface with a the odrive and actuation
module for the Manus Home V2.

The motor that was used was a 
9235-100KV Turnigy Multistar Brushless Multi-Rotor Motor

Author: Benjamin Gutierrez
Email: mrbengutierrez@gmail.com
Date: 01/30/2019


"""


import odrive
from odrive.enums import *


# gear ratio of the actuation module
GEAR_RATIO = 4

#number of encoder ticks per revolution (AS5047p encoder)
ENCODER_TICKS_PER_REV = 4000

class OdriveController:
	def __init__(self,serialPort=None,numMotors=2):
		""" Initializes parameters for the Odrive Controller 
		
			Parameters:
			serialPort (string): name of the odrive that the motor is connected to
			numMotors (int): Number of motors to initialize. Can be 1 or 2 only.
			
			Returns:
			nothing
		"""
		# save input parameters
		self.serialPort = serialPort
		self.numMotors = numMotors
		
		# Find a connected ODrive (this will block until you connect one)
		print("finding an odrive...")
		if serialPort == None:
			self.my_drive = odrive.find_any()
		else:
			# Find an ODrive that is connected on the serial port /dev/ttyUSB0
			#self.my_drive = odrive.find_any("serial:/dev/ttyUSB0")
			self.my_drive = odrive.find_any("serial:" + serialPort)
			

		# Set brake resistor value
		self.my_drive.config.brake_resistance = 2 # Ohm
		
		self.motors = []
		if numMotors == 1:
			self.motors = [self.my_drive.axis0]
		elif numMotors == 2:
			self.motors = [self.my_drive.axis0,self.my_drive.axis1]
		
		for axis in self.motors:

			# Set current limit
			axis.motor.config.current_lim = 10 # Amps
			
			# Set velocity limit
			#self.my_drive.axis0.motor.config.vel_limit = 100 # counts/s
			
			# Set number of magnet poles 
			numMagnets = 40 
			axis.motor.config.pole_pairs = int(numMagnets/2)


			# Note from ODRIVE documentation
			# If 100’s of mA of current noise is “small” for you, 
			# you can choose MOTOR_TYPE_HIGH_CURRENT. If 100’s of mA of current noise
			# is “large” for you, and you do not intend to spin the motor very fast (Ω * L « R), 
			# and the motor is fairly large resistance (1 ohm or larger), 
			# you can chose MOTOR_TYPE_GIMBAL.
			axis.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
			
			# Set the Encoder Count Per Revolution [CPR]
			# This is 4x the Pulse Per Revolution (PPR) value. 
			# Usually this is indicated in the datasheet of your encoder.
			axis.encoder.config.cpr =  ENCODER_TICKS_PER_REV # CPR
			
			
		# Print Values ----
			
		# Or to change a value, just assign to the property
		#my_drive.axis0.controller.pos_setpoint = 3.14
		print("Position setpoint is " + str(axis.controller.pos_setpoint))

		# And this is how function calls are done:
		for i in [1,2,3,4]:
			print('voltage on GPIO{} is {} Volt'.format(i, self.my_drive.get_adc_voltage(i)))
			
	def calibrate():
		""" Calibrates the odrive motors by spinning them through one free revolution"""
		# NOTE: Make sure you mechanically disengage the motor from anything
		# other than the encoder, so it can spin freely
		for axis in self.motors:
			# Use index
			axis.encoder.config.use_index = True
			
			# This will make the motor turn in one direction until it finds the encoder index
			axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
			
			# Encoder offset calibration
			# The rotor must be allowed to rotate without any biased load during startup.
			axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
			
			# Check to make sure encoder offset calibration was a success
			print("axis.error: " + str(axis.error) + ", reference value: 0")
			print("axis.encoder.config.offset: " + str(axis.encoder.config.offset) + ", reference value: a number, like -326 or 1364")
			print("axis.motor.config.direction: " + str(axis.motor.config.direction) + ", reference value: 1 or -1")
			
			# Confirm that the offset is valid with respect to the index pulse
			axis.encoder.config.pre_calibrated = True
			
			# Save the current motor calibration and avoid doing it again on bootup.
			axis.motor.config.pre_calibrated = True
		
		# Save all .config parameters to persistent memory so the ODrive remembers them between power cycles.
		self.my_drive.save_configuration
		
		# Reboot following save of configuration due to known issue
		try:
			self.my_drive.reboot()
		except fibre.protocol.ChannelBrokenException: # error from rebooting
			pass
		self.__init__(self.serialPort, self.numMotors)
			
		
	def getMotors(self):
		"""Returns a list of Odrive motor objects"""
		return [OdriveMotor(axis) for axis in self.motors]
	

class OdriveMotor:
	
	def __init__(self, motor, initialPosition=0.0):
		""" Initializes a new motor connected to an Odrive motor controller "
		
			Parameters:
			motor (odrive.axis): motor specifier where odrive is the current odrive & axis is the axis of that odrive
			initialPosition (float): initial position of motor in degrees (0 <= initialPosition <= 360.0)
			
			Returns:
			nothing
		"""
		# set transmission gear ratio
		self.gearRatio = GEAR_RATIO
		
		# set initial position value
		self.setpointPerRev = ENCODER_TICKS_PER_REV
		
		# set the offset setpoint referencing from zero degrees
		self.setpointOffset = int(0) # initialize offset setpoint
		self.calibrateAngularPosition(initialPosition)
		
		
		# use closed loop control
		self.axis = motor

	
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
	
	def angularVelocityMode(self,angVel = 0):
		"""Method to activate the angular velocity control
		
			Parameters:
			angVel (int): angualr velocity in rpm
			
			Returns:
			None
		"""
		raise NotImplementedError
		
	def angularPositionMode(self):
		"""Method to activate the angular position control
			
			Parameters:
			None
			
			Returns:
			None
		"""
		# use closed loop control
		self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
		return
	
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
	
	def setAngularVelocity(self, angVel):
		"""Method to change the angular velocity value in real time
		
			Parameters:
			angVel (int): Angular velocity in rpm
			
			Returns
			None
		"""
		raise NotImplementedError
	
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
		
		setpoint = self._getSetpoint()
		relativeSetpoint = self._degreesToSetpoint(angPos)
		newSetpoint = setpoint + relativeSetpoint
		self._setSetpoint(newSetpoint)
		self._setSetpoint(newSetpoint)
		return
		
	def setAbsoluteAngularPosition(self, angPos, angVel = 200, direction="counter-clockwise"):
		"""Method to change the absolute angular position value in real time with ability to control direction.
		
			Parameters:
			angPos (double): angular position value in degrees (must always be positive)
						(0 <= angPos <= 360.0)
			angVel (int): angular velocity value in rpm (must always be positive)
			direction (string): direction that motor should rotate
								can be "counter-clockwise" or "clockwise" only
			
			Returns:
			None
		"""
		
		#set sign of angPos
		if direction == "clockwise":
			angPos = -angPos
		
		currentPosition = self.getAbsoluteAngularPosition()
		degreesPerRevolution = 360.0
			
		positiveAngularPosition = angPos * OdriveMotor._sign(angPos)
			
		# deltaPosition is the difference between target position and current position
		deltaPosition = (positiveAngularPosition - currentPosition) * OdriveMotor._sign(angPos)
		if (deltaPosition < 0.0):
			 deltaPosition += degreesPerRevolution # make sure deltaPosition < 360.0 degrees
		deltaPosition *= OdriveMotor._sign(angPos) # account for direction of rotation
	
		self.setRelativeAngularPosition( deltaPosition, angVel )
		return
		
	
	def setAbsoluteAngularPositionShortestPath(self, angPos,angVel = 200):
		""" Method to change the absolute angular position value in real time. 
			Motor rotates in the shortest path to new target angular position.
			
			Parameters:
			angPos (double): angular position value in degrees (must always be positive)
							(0.0 <= angPos <= 360.0)
			angVel (int): angular velocity value in rpm (must always be positive)
			
			Returns:
			None
		"""
		currentPosition = self.getAbsoluteAngularPosition()
		deltaPosition = angPos - currentPosition
		self.setRelativeAngularPosition(deltaPosition)
		return
	
	def stop(self):
		"""Method that sends the commands to stop the motor.
		
			Returns:
			None    
		"""
		# Disable motor PWM and do nothing
		self.axis.requested_state = AXIS_STATE_IDLE 
	
	def getTorque(self):
		"""Returns the torque as thousandths of the torque
		
			Returns:
			int: value of the angular torque as thousandths of the torque,
				 e.g., the value "500" means "50%" of the rated torque;
				 (0 <= value <= 1000)
		"""
		raise NotImplementedError
	
	def getAngularVelocity(self):
		"""Returns the current angular velocity in rpm
		
			Returns:
			int: current angular velocity in rpm
		"""
		raise NotImplementedError
	
	def getAbsoluteAngularPosition(self):
		"""Returns the absolute angular position of the motor shaft in degrees
		
			Returns:
			double: absolute angular position of the motor shaft in degrees
					(0.0 <= output < 360.0)
		"""
		setpoint = self._getSetpoint()
		deltaSetpoint = setpoint - self.setpointOffset
		degrees = self._setpointToDegrees(deltaSetpoint)
		return degrees

	
	def closePort(self):
		"""Method to close the port of the serial communication.
		
			Returns:
			None
		"""
		raise NotImplementedError
	
	def calibrateAngularPosition(self, specifiedAngularPosition):
		""" Calibrates motor to have its current angular position be set to a a specified angular position
		
			Parameters:
			newPosition (float): The new angular position to set the motor to
			
			Returns:
			None
		"""
		self.setpointOffset = self._degreesToSetpoint(specifiedAngularPosition)
		return


	# Private Methods ---
	
	def _setpointToDegrees(self, setpoint):
		""" Converts setpoint to degrees 
		
			Parameters:
			setpoint (int): current setpoint of the motor
			
			Returns:
			(float): current angle of the secondary or output shaft of the
			         transmission in degrees
		"""
		degreesPerRevolution = 360.0
		degrees = float( degreesPerRevolution*setpoint / (self.setpointPerRev*self.gearRatio) )
		return degrees
	
	def _degreesToSetpoint(self, degrees):
		""" Converts setpoint to degrees 
		
			Parameters:
			degrees (float): current angle of the secondary or output shaft of the
							 transmission in degrees 
			
			Returns:
			(int):  current setpoint of the motor
		"""
		degreesPerRevolution = 360.0
		setpoint = int( degrees*self.setpointPerRev*self.gearRatio / degreesPerRevolution )
		return setpoint	
		
	def _setSetpoint(self, setpoint):
		""" Sets the new setpoint of the motor
		
			Parameters:
			setpoint (int): setpoint to set motor to
			
			Returns:
			None
		"""
		#print("set setpoint: " + str(setpoint))
		setpoint = int(setpoint)
		self.axis.controller.pos_setpoint = setpoint
		
	def _getEncoderTick(self):
		""" Returns the current encoder tick of the motor
		
			Parameters:
			None
			
			Returns:
			(int): current setpoint of the motor
		"""
		#print("get setpoint: " + str(self.axis.controller.pos_setpoint))
		return self.axis.controller.pos_setpoint
	
	@staticmethod
	def _sign(value):
		""" Returns sign of a number
		
			Parameters:
			value (float, int): value to take sign of
			
			Returns:
			(float): -1.0 if value is negative, else returns 1.0
		"""
		if value < -0.0:
			return -1.0
		return 1.0
		


def main():
	motorController = OdriveController()
	#motorController.calibrate()
	[leftMotor,rightMotor] = motorController.getMotors()
	
	import time
	print("")
	
	leftMotor.angularPositionMode()
	
	print("Testing setRelativeAngularPosition(90.0)")
	print(leftMotor.getAbsoluteAngularPosition())
	leftMotor.setRelativeAngularPosition(90.0)
	time.sleep(5)
	
	print("Testing setRelativeAngularPosition(-90.0)")
	print(leftMotor.getAbsoluteAngularPosition())
	leftMotor.setRelativeAngularPosition(-90.0)
	time.sleep(5)
	
	print('Testing setAbsoluteAngularPosition(angPos=180.0, direction="counter-clockwise")')
	print(leftMotor.getAbsoluteAngularPosition())	
	leftMotor.setAbsoluteAngularPosition(angPos=180.0, direction="counter-clockwise")
	time.sleep(5)

	print('Testing setAbsoluteAngularPosition(angPos=90.0, direction="clockwise")')
	print(leftMotor.getAbsoluteAngularPosition())	
	leftMotor.setAbsoluteAngularPosition(angPos=90.0, direction="clockwise")
	time.sleep(5)	
	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=270.0)")
	print(leftMotor.getAbsoluteAngularPosition())	
	leftMotor.setAbsoluteAngularPositionShortestPath(angPos=270.0)
	time.sleep(5)
	
	print("Testing setAbsoluteAngularPositionShortestPath(angPos=0.0)")
	print(leftMotor.getAbsoluteAngularPosition())	
	leftMotor.setAbsoluteAngularPositionShortestPath(angPos=0.0)
	time.sleep(5)	
	
	print(leftMotor.getAbsoluteAngularPosition())	
	leftMotor.stop()


if __name__ == "__main__":
	main()



