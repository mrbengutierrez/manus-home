"""
This file acts as an object to interface with a the odrive and actuation
module for the Manus Home V2.

The motor that was used was a 
9235-100KV Turnigy Multistar Brushless Multi-Rotor Motor

Author: Benjamin Gutierrez
Email: mrbengutierrez@gmail.com
Date: 02/03/2020


"""

# import odrive libraries for motor controller
import odrive
from odrive.enums import *

import enum # for control modes

class ControlMode(enum.Enum):
	""" Enumeration for specifying control mode that OdriveMotor is in"""
	Off = 0
	AngularPosition = 1
	AngularVelocity = 2
	Torque = 3


# gear ratio of the actuation module
GEAR_RATIO = 4

#number of encoder ticks per revolution (AS5047p encoder)
ENCODER_TICKS_PER_REV = 4000

class OdriveController:
	def __init__(self,serialPort=None,numMotors=2,calibrate=False):
		""" Initializes parameters for the Odrive Controller 
		
			Parameters:
			serialPort (string): name of the odrive that the motor is connected to
			numMotors (int): Number of motors to initialize. Can be 1 or 2 only.
			calibrate (bool): calibrates odrive motor(s) if True, else assumes
			                  motors are already calibrated
			
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
			axis.motor.config.current_lim = 40 # Amps
			
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
		
		# calibrate if specified to calibrate
		if calibrate: 
			self.calibrate()
		
		# search for index
		if numMotors == 1:
			axis = self.motors[0]
			axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
		if numMotors == 2:
			# reverse direction of index search
			axis = self.motors[1]
			axis.config.calibration_lockin.vel = -axis.config.calibration_lockin.vel
			axis.config.calibration_lockin.accel = -axis.config.calibration_lockin.accel
			axis.config.calibration_lockin.ramp_distance = -axis.config.calibration_lockin.ramp_distance
			
			#search for index
			axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH

			# reset direction of index search
			axis = self.motors[1]
			axis.config.calibration_lockin.vel = -axis.config.calibration_lockin.vel
			axis.config.calibration_lockin.accel = -axis.config.calibration_lockin.accel
			axis.config.calibration_lockin.ramp_distance = -axis.config.calibration_lockin.ramp_distance			
		# index is now found for each motor
		
		# make sure each axis is disabled to start
		for axis in self.motors:
			axis.requested_state = AXIS_STATE_IDLE		
		return
		
		
		
			
			
	def calibrate(self):
		""" Calibrates the odrive motors by spinning them through one free revolution"""
		# NOTE: Make sure you mechanically disengage the motor from anything
		# other than the encoder, so it can spin freely
		for axis in self.motors:
			# store previous angular velocity limit
			previousAngularVelocityLimit = axis.controller.config.vel_limit
			# make sure angular velocity is fast enough to prevent
			# spinning motor from stopping abruptly during calibration
			axis.controller.config.vel_limit = 50000 # counts/sec
			
			# Use index
			axis.encoder.config.use_index = True
			
			axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE # Run motor calibration and then encoder offset calibration
			import time
			time.sleep(20) # give time for motor to calibrate
			
			# restore previous angular velocity limit
			axis.controller.config.vel_limit = previousAngularVelocityLimit
			
			# This will make the motor turn in one direction until it finds the encoder index
			#axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
			
			# Encoder offset calibration
			# The rotor must be allowed to rotate without any biased load during startup.
			#axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
			
			# Check to make sure encoder offset calibration was a success
			print("axis.error: " + str(axis.error) + ", reference value: 0")
			print("axis.encoder.config.offset: " + str(axis.encoder.config.offset) + ", reference value: a number, like -326 or 1364")
			print("axis.motor.config.direction: " + str(axis.motor.config.direction) + ", reference value: 1 or -1")
			
			# Confirm that the offset is valid with respect to the index pulse
			axis.encoder.config.pre_calibrated = True
			
			# Save the current motor calibration and avoid doing it again on bootup.
			axis.motor.config.pre_calibrated = True
			
		
		# Save all .config parameters to persistent memory so the ODrive remembers them between power cycles.
		self.my_drive.save_configuration()
		time.sleep(1) # give time for motor save calibration
		
		# Reboot following save of configuration due to known issue
		try:
			self.my_drive.reboot()
		except: # error from rebooting
			pass
		# reset parameter for odrive controller
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
		# create variable to represent odrive axis
		self.axis = motor
		
		# set transmission gear ratio
		self.gearRatio = GEAR_RATIO
		
		# set initial position value
		self.encoderTickPerRev = ENCODER_TICKS_PER_REV
		
		# set the offset setpoint referencing from zero degrees
		self.encoderTickOffset = int(0) # initialize offset encoder tick
		self.calibrateAngularPosition(initialPosition)

		# set maximum angular velocity
		maxAngularVelocity = 100 # rpm
		self._setMaxAngularVelocity(maxAngularVelocity)	
		
		# allow larger speed limit violations to prevent error codes
		self.axis.controller.config.vel_limit_tolerance = 4
		
		# make sure motor is stopped
		self.stop()
		
		#set control mode to off
		self.controlMode = ControlMode.Off
		

	

	
	def setTorque(self, torque, maxAngVel=400):
		"""Method to activate the Profile Torque or torque profile.

			Parameters:
			torque (float): Torque value in percentage (decimal value 0-1000=100%)
			Returns:
			None
		"""
		# set the maximum planned angular velocity
		self._setMaxAngularVelocity(maxAngVel)
				
		# make sure we are are in torque control mode
		if self.controlMode != ControlMode.Torque:
			self._torqueMode()
		
		# set the torque
		current = self._torqueToCurrent(torque)
		self.axis.controller.current_setpoint = current
	
	def setAngularVelocity(self, angVel):
		"""Method to change the angular velocity value in real time
		
			Parameters:
			angVel (float): Angular velocity in rpm
			
			Returns
			None
		"""
		# make sure we are in angular velocity control mode
		if self.controlMode != ControlMode.AngularVelocity:
			self._angularVelocityMode()
		
		# set the angular velocity
		scaledAngularVelocity = self._rpmToCountsPerSec(angVel) # counts/sec, int
		self.axis.controller.vel_setpoint = scaledAngularVelocity
	
	def setRelativeAngularPosition(self, angPos, angVel = 20):
		"""Method to change the relative angular position value in real time. 
			The position is set using the current position as the zero position.
			
			Parameters:
			angPos (double): angular position value in degrees 
							positive for counter-clockwise direction, negative for clockwise direction
							(-360.0 <= angPos <= 360.0)
			angVel (int): angular velocity value in rpm (must always be positive)
			
			Returns:
			None
		"""
		# set the maximum planned angular velocity
		self._setMaxAngularVelocity(angVel)
			
		# make sure we are in angular position control mode
		if self.controlMode != ControlMode.AngularPosition:
			self._angularPositionMode()
		
		# set relative angular position
		encoderTick = self._getEncoderTick()
		relativeEncoderTick = self._degreesToEncoderTicks(angPos)
		newSetpoint = encoderTick + relativeEncoderTick
		self._setSetpoint(newSetpoint)
		return
		
	def setAbsoluteAngularPosition(self, angPos, angVel = 20, direction="counter-clockwise"):
		"""Method to change the absolute angular position value in real time with ability to control direction.
		
			Parameters:
			angPos (double): angular position value in degrees (must always be positive)
						(0 <= angPos < 360.0)
			angVel (int): angular velocity value in rpm (must always be positive)
			direction (string): direction that motor should rotate
								can be "counter-clockwise" or "clockwise" only
			
			Returns:
			None
		"""
		# set the maximum planned angular velocity
		self._setMaxAngularVelocity(angVel)		
		
		# make sure we are in angular position control mode
		if self.controlMode != ControlMode.AngularPosition:
			self._angularPositionMode()
		
		degreesPerRevolution = 360.0
		currentPosition = self.getAbsoluteAngularPosition()
		deltaPosition = angPos - currentPosition
		
		relativePosition = None # initialize relativePosition
		if direction == "counter-clockwise":
			if deltaPosition >= 0.0:
				relativePosition = deltaPosition
			else: # deltaPosition < 0.0
				relativePosition = deltaPosition + degreesPerRevolution
		
		if direction == "clockwise":
			if deltaPosition >= 0.0:
				relativePosition = -deltaPosition + degreesPerRevolution
			else: # deltaPosition < 0.0
				relativePosition = deltaPosition
		
		self.setRelativeAngularPosition(relativePosition, angVel)
		return
		
	
	def setAbsoluteAngularPositionShortestPath(self, angPos,angVel = 20):
		""" Method to change the absolute angular position value in real time. 
			Motor rotates in the shortest path to new target angular position.
			
			Parameters:
			angPos (double): angular position value in degrees (must always be positive)
							(-360.0 < angPos < 360.0)
			angVel (int): angular velocity value in rpm (must always be positive)
			
			Returns:
			None
		"""

		# set the maximum planned angular velocity
		self._setMaxAngularVelocity(angVel)		
		
		# make sure we are in angular position control mode
		if self.controlMode != ControlMode.AngularPosition:
			self._angularPositionMode()
								
		# degrees per revolution
		degreesPerRotation = 360.0		
		
		# bound angular position in range 0.0 - 360.0 degrees
		angPos = OdriveMotor._boundAngle(angPos)
		print("angPos given: " + str(angPos)) # for debugging
			
		# set angular position
		currentPosition = self.getAbsoluteAngularPosition()
		deltaPosition = angPos - currentPosition
		
		relativePosition = None
		# case 1: rotate clockwise
		if deltaPosition > 0.0 and abs(deltaPosition) >= degreesPerRotation/2:
			relativePosition = -abs(degreesPerRotation - deltaPosition) # clockwise
			print("case 1") # for debugging
			
		# case 2: rotate clockwise
		elif deltaPosition < 0.0 and abs(deltaPosition) <= degreesPerRotation/2:
			relativePosition = -abs(deltaPosition) # clockwise
			print("case 2") # for debugging

		# case 3: rotate counter-clockwise
		elif deltaPosition < 0.0 and abs(deltaPosition) >= degreesPerRotation/2:
			relativePosition = abs(degreesPerRotation + deltaPosition) # counter-clockwise
			print("case 3") # for debugging
			
		# case 4: rotate counter-clockwise
		elif deltaPosition > 0.0 and abs(deltaPosition) <= degreesPerRotation/2:
			relativePosition = abs(deltaPosition) # counter-clockwise		
			print("case 4") # for debugging
			
		else:
			raise RuntimeError("position difference did not meet any cases")
		
		
		self.setRelativeAngularPosition(relativePosition, angVel)
		
		return
	
	def stop(self):
		"""Method that sends the commands to stop the motor.
		
			Returns:
			None    
		"""
		# Disable motor PWM and do nothing
		self.axis.requested_state = AXIS_STATE_IDLE 
		self.controlMode = ControlMode.Off
		return
	
	def getTorque(self):
		"""Returns the torque as thousandths of the torque
		
			Returns:
			int: value of the angular torque as thousandths of the torque,
				 e.g., the value "500" means "50%" of the rated torque;
				 (0 <= value <= 1000)
		"""
		current = self.axis.motor.current_control.Iq_measured
		torque = self._torqueToCurrent(current)
		return torque
	
	def getAngularVelocity(self):
		"""Returns the current angular velocity in rpm
		
			Returns:
			float: current angular velocity in rpm
		"""
		measuredAngularVelocity = self.axis.encoder.vel_estimate # counts/sec, int
		scaledAngularVelocity = self._countsPerSecToRPM(measuredAngularVelocity) # rpm, float
		return scaledAngularVelocity
	
	def getAbsoluteAngularPosition(self):
		"""Returns the absolute angular position of the motor shaft in degrees
		
			Returns:
			double: absolute angular position of the motor shaft in degrees
					(0.0 <= output < 360.0)
		"""
		encoderTick = self._getEncoderTick()
		deltaEncoderTick = encoderTick - self.encoderTickOffset
		degrees = self._encoderTickToDegrees(deltaEncoderTick)
		
		# check to see if angle in bounds (0.0-360.0)
		boundedAngle = OdriveMotor._boundAngle(degrees)
		return boundedAngle

	
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
		encoderTick = self._getEncoderTick()
		specifiedEncoderTick = self._degreesToEncoderTicks(specifiedAngularPosition)
		self.encoderTickOffset = encoderTick - specifiedEncoderTick
		return


	# Private Methods ---
	
	def _encoderTickToDegrees(self, encoderTick):
		""" Converts encoder tick to degrees 
		
			Parameters:
			encoderTick (int): current encoder tick of the motor
			
			Returns:
			(float): current angle of the secondary or output shaft of the
			         transmission in degrees
		"""
		degreesPerRevolution = 360.0
		degrees = float( degreesPerRevolution*encoderTick / (self.encoderTickPerRev*self.gearRatio) )
		return degrees
	
	def _degreesToEncoderTicks(self, degrees):
		""" Converts encoder tick to degrees 
		
			Parameters:
			degrees (float): current angle of the secondary or output shaft of the
							 transmission in degrees 
			
			Returns:
			(int):  current setpoint of the motor
		"""
		degreesPerRevolution = 360.0
		encoderTick = int( degrees*self.encoderTickPerRev*self.gearRatio / degreesPerRevolution )
		return encoderTick
		
	def _setSetpoint(self, setpoint):
		""" Sets the new setpoint of the motor
		
			Parameters:
			setpoint (int): setpoint to set motor to
			
			Returns:
			None
		"""
		setpoint = int(setpoint)
		self.axis.controller.pos_setpoint = setpoint
		
	def _getEncoderTick(self):
		""" Returns the current encoder tick of the motor
		
			Parameters:
			None
			
			Returns:
			(int): current encoder tick of the motor
		"""
		return self.axis.encoder.pos_estimate
	
	def _rpmToCountsPerSec(self, rpm):
		""" Converts revolutions per minute to counts per second
		
			Parameters: 
			rpm (float): value of rpm
			
			Returns:
			(int): value of rpm in counts per second
		"""
		minPerSec = 1/60
		#convert from rpm to count/sec
		scaledAngularVelocity = rpm*minPerSec*self.encoderTickPerRev*self.gearRatio # counts/sec
		scaledAngularVelocity = int(scaledAngularVelocity) # counts/sec must be int
		return scaledAngularVelocity	
	
	def _countsPerSecToRPM(self, countsPerSec):
		""" Converts counts per second to revolutions per minute
		
			Paramters:
			countsPerSec (int): value of counts per sec
			
			Returns:
			(float): value of countsPerSec in rpm
		"""
		secPerMin = 60
		#convert from count/s to rpm
		scaledAngularVelocity = countsPerSec*secPerMin/(self.encoderTickPerRev*self.gearRatio)
		scaledAngularVelocity = float(scaledAngularVelocity)
		return scaledAngularVelocity	
	
	def _setMaxAngularVelocity(self, angVel):
		""" Set the maximum angular velocity that the motor can spin
		
			Parameters:
			angVel (float): maximum angular velocity in rpms
			
			Returns:
			None
		"""
		scaledAngularVelocity = self._rpmToCountsPerSec(angVel) # counts/sec, int
		self.axis.controller.config.vel_limit = scaledAngularVelocity
		return
	
	def _torqueToCurrent(self, torque):
		""" Converts torque to current
		
			Parameters: 
			torque (float): torque value in Newton-meters
			
			Returns:
			(float): value of current in Amps
		"""
		# Using the motor current and the known KV of your motor you can 
		# estimate the motors torque using the following relationship: 
		# Torque [N.m] = 8.27 * Current [A] / KV.
		KV = 100
		current = (torque * KV / 8.27) / self.gearRatio
		return current
		
		
		
		
	def _currentToTorque(self, current):
		""" Converts current to torque
		
			Parameters:
			current (float): current value in Amps
			
			Returns:
			(float): value of torque in Newton-meters
		"""
		# Using the motor current and the known KV of your motor you can 
		# estimate the motors torque using the following relationship: 
		# Torque [N.m] = 8.27 * Current [A] / KV.
		KV = 100
		torque = (8.27 * current / KV) * self.gearRatio
		return torque	

	def _torqueMode(self):
		"""Method to activate the Profile Torque or torque profile.
		
			Parameters:
			None
			
			Returns:
			None
		"""
		self.axis.controller.config.control_mode = CTRL_MODE_CURRENT_CONTROL
		self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
		self.controlMode = ControlMode.Torque
		return
	
	def _angularVelocityMode(self):
		"""Method to activate the angular velocity control
		
			Parameters:
			None
			
			Returns:
			None
		"""
		self.axis.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL
		self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
		self.controlMode = ControlMode.AngularVelocity
		return
		
	def _angularPositionMode(self):
		"""Method to activate the angular position control
			
			Parameters:
			None
			
			Returns:
			None
		"""
		# use closed loop control
		self.axis.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
		self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
		self.controlMode = ControlMode.AngularPosition
		return			
	
	@staticmethod
	def _boundAngle(angle):
		""" Bounds an angle into the range 0.0 - 360.0 degrees
		
			Parameters:
			angle (float): angle to bound, must be in degrees
			
			Returns:
			(float): bounded angle in range 0.0 - 360.0 degrees
		"""
		degreesPerRotation = 360.0
		angPos = angle
		if angPos >= 360.0:
			divisor = int(angPos/degreesPerRotation)
			angPos = angPos - divisor*degreesPerRotation
		if angPos < 0.0:
			divisor = int( angPos/degreesPerRotation ) - 1
			angPos = angPos - divisor*degreesPerRotation
		return angPos
		
	
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
	pass # do nothing


if __name__ == "__main__":
	main()



