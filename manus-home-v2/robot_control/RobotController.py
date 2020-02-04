"""
This file constructs an arm simulator for the cheaper MIT MANUS

Author: Benjamin Gutierrez
email: mrbengutierrez@gmail.com
"""


import time # for print functions


import numpy as np
import matplotlib.pylab as plt
import scipy as sp

# import python library to control nanotec motors
from OdriveMotor import OdriveController
from OdriveMotor import OdriveMotor

	
class Graphics:

	def __init__(self):
		"""Constructor for Graphics object"""
		pass

	def plotPosition(x,y):
		""" plots the position of the robot on the screen"""
		pass



		


class Kinematics:
	def __init__(self):
		inchesToMeters = 0.0254;
		self.l1 = 13.25 * inchesToMeters
		self.l2 = 13.25 * inchesToMeters
		self.l3 = 15.5 * inchesToMeters
		self.l4 = 15.5 * inchesToMeters
		self.d = 3 * inchesToMeters
		
		self.gearRatio = 10

	def forwardKinematics(self,q):
		"""converts joint angles to end effector position
		Parameters:
		q (numpy.array of floats)
			q[0] (float): left joint angle
			q[1] (float): right joint angle
		Returns:
		(np.array of floats): np.array([x,y]) The end effector position
		"""
		q1 = q[0]
		q2 = q[1]
		
		x_d = self.l2*np.cos(q2) + self.d
		y_d = self.l2*np.sin(q2)
		x_c = self.l1*np.cos(q1) - self.d
		y_c = self.l1*np.sin(q1)

		psi = np.arctan2(y_d - y_c, x_d - x_c)
		
		h = np.sqrt( (y_d - y_c)**2 + (x_d - x_c)**2 )
		delta = np.arccos( (self.l3**2 + h**2 - self.l4**2) / (2*self.l3*h) )

		theta3 = delta + psi
		
		x = x_c + self.l3*np.cos(theta3)
		y = y_c + self.l3*np.sin(theta3)

		return np.array([x,y])

	def inverseKinematics(self,r):
		"""converts end effector position to joint angles
		Parameters:
		r (numpy.array of floats)
			r[0] (float): x end effector position in meters
			r[1] (float): y end effector position in meters
		Returns:
		(np.array of floats): np.array([x,y]) The joint parameters
		"""
		x = r[0]
		y = r[1]

		# x,y --> q1
		alpha1 = np.arctan2(y,x+self.d)
		r1 = np.sqrt((x+self.d)**2 + y**2)
		gamma1 = np.arccos( (self.l1**2 + r1**2 - self.l3**2) / (2*self.l1*r1) )
		q1 = alpha1 + gamma1

		# x,y --> q2
		alpha2 = np.arctan2(y,x-self.d)
		r2 = np.sqrt((x-self.d)**2 + y**2)
		gamma2 = np.arccos( (r2**2 + self.l2**2 - self.l4**2) / (2 * self.l2 * r2) )
		q2 =  alpha2 - gamma2

		return np.array([q1,q2])

	def jacobian(self,q):
		"""Returns the Jacobian matrix for a given set of joint angles
		Parameters:
		q (numpy.array of floats)
			q[0] (float): left joint angle in radians
			q[1] (float): right joint angle in radians
		Returns:
		(2x2 numpy.array): the Jacobian matrix
		"""
		return self.computeActualJacobian(q)

	def computeActualJacobian(self,q):
		"""Returns the Jacobian matrix for a given set of joint angles
			using the actual Jacobian
			
		Parameters:
		q (numpy.array of floats)
			q[0] (float): left joint angle in radians
			q[1] (float): right joint angle in radians
		
		Returns:
		(2x2 numpy.array): the Jacobian matrix
		"""
		q1 = q[0]
		q2 = q[1]
		
		l1 = self.l1
		l2 = self.l2
		l3 = self.l3
		l4 = self.l4
		d = self.d
		cos = np.cos
		sin = np.sin
		acos = np.arccos
		atan2 = np.arctan2
		real = lambda x: x.real
		imag = lambda x: x.imag

		dXdQ1 = - l1*sin(q1) + l3*sin(atan2(l2*sin(q2) - l1*sin(q1), 2*d - l1*cos(q1) + l2*cos(q2)) + acos(((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2))))*(((2*l1*sin(q1)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l1*cos(q1)*(l1*sin(q1) - l2*sin(q2)))/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2)) - ((2*l1*sin(q1)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l1*cos(q1)*(l1*sin(q1) - l2*sin(q2)))*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2))/(4*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(3/2)))/(1 - ((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)**2/(4*l3**2*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)))**(1/2) + (((real(l1*cos(q1)) - imag(l1*sin(q1)))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2))) + ((real(l1*sin(q1)) + imag(l1*cos(q1)))*(real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2))))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)*(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)/((real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2)))**2 + (2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2))
		dXdQ2 = -l3*sin(atan2(l2*sin(q2) - l1*sin(q1), 2*d - l1*cos(q1) + l2*cos(q2)) + acos(((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2))))*(((2*l2*sin(q2)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l2*cos(q2)*(l1*sin(q1) - l2*sin(q2)))/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2)) - ((2*l2*sin(q2)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l2*cos(q2)*(l1*sin(q1) - l2*sin(q2)))*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2))/(4*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(3/2)))/(1 - ((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)**2/(4*l3**2*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)))**(1/2) + (((real(l2*cos(q2)) - imag(l2*sin(q2)))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2))) + ((real(l2*sin(q2)) + imag(l2*cos(q2)))*(real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2))))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)*(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)/((real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2)))**2 + (2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2))
		dYdQ1 = l1*cos(q1) - l3*cos(atan2(l2*sin(q2) - l1*sin(q1), 2*d - l1*cos(q1) + l2*cos(q2)) + acos(((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2))))*(((2*l1*sin(q1)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l1*cos(q1)*(l1*sin(q1) - l2*sin(q2)))/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2)) - ((2*l1*sin(q1)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l1*cos(q1)*(l1*sin(q1) - l2*sin(q2)))*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2))/(4*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(3/2)))/(1 - ((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)**2/(4*l3**2*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)))**(1/2) + (((real(l1*cos(q1)) - imag(l1*sin(q1)))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2))) + ((real(l1*sin(q1)) + imag(l1*cos(q1)))*(real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2))))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)*(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)/((real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2)))**2 + (2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2))
		dYdQ2 = l3*cos(atan2(l2*sin(q2) - l1*sin(q1), 2*d - l1*cos(q1) + l2*cos(q2)) + acos(((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2))))*(((2*l2*sin(q2)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l2*cos(q2)*(l1*sin(q1) - l2*sin(q2)))/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2)) - ((2*l2*sin(q2)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l2*cos(q2)*(l1*sin(q1) - l2*sin(q2)))*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2))/(4*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(3/2)))/(1 - ((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)**2/(4*l3**2*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)))**(1/2) + (((real(l2*cos(q2)) - imag(l2*sin(q2)))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2))) + ((real(l2*sin(q2)) + imag(l2*cos(q2)))*(real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2))))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)*(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)/((real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2)))**2 + (2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2))
		return np.array([[dXdQ1,dXdQ2],[dYdQ1,dYdQ2]])

	def computeApproximateJacobian(self,q):
		"""Returns the approximate Jacobian matrix for a given set of joint angles
		
		Parameters:
		q (numpy.array of floats)
			q[0] (float): left joint angle in radians
			q[1] (float): right joint angle in radians
		
		Returns:
		(2x2 numpy.array): the Jacobian matrix
		"""
		jacobianSize = (2,2)
		eps = 0.0001 # precision
		q1 = q[0]
		q2 = q[1]
		
		biggerQ1 = forwardKinematics(q1+eps,q2)
		smallerQ1 = forwardKinematics(q1-eps,q2)
		biggerQ2 = forwardKinematics(q1,q2+eps)
		smallerQ2 = forwardKinematics(q1,q2-eps)
		
		dXdQ1 = (biggerQ1[0] - smallerQ1[0]) / (2*eps)
		dXdQ2 = (biggerQ2[0] - smallerQ2[0]) / (2*eps)
		dYdQ1 = (biggerQ1[1] - smallerQ1[1]) / (2*eps)
		dYdQ2 = (biggerQ2[1] - smallerQ2[1]) / (2*eps)
		return np.array([[dXQ1,dXQ2],[dYdQ1,dYdQ2]])
		


	def torqueToForce(self,t,q):
		"""Converts joint torques to endpoint forces
		Parameters:
		t (numpy.array of floats)
			t[0] (float): left joint torque in newton-meters
			t[1] (float): right joint angle in newton-meters
		q (numpy.array of floats)
			q[0] (float): left joint angle in radians
			q[1] (float): right joint angle in radians
		Returns:
		(numpy.array of floats): numpy.array([fx,fy]) the end effector forces
		"""
		jacobianTranspose = np.transpose(self.jacobian(q))
		jacobianTransposeInverse = np.linalg.inv(jacobianTranspose)
		force = np.dot(jacobianTransposeInverse,t)
		return force

	def forceToTorque(self,f,q):
		"""Converts endpoint forces to joint torques
		Parameters:
		f (numpy.array of floats)
			f[0] (float): x endpoint force in newtons
			f[1] (float): y endpoint force in newtons
		q (numpy.array of floats)
			q[0] (float): left joint angle in radians
			q[1] (float): right joint angle in radians
		Returns:
		(numpy.array of floats): (t1,t2) the joint torques
		"""
		jacobianTranspose = np.transpose(self.jacobian(q))
		torque = np.dot(jacobianTranspose,f)
		return torque

	def angularVelocityToVelocity(self,qDot,q):
		"""Converts joint angular velocities to end effector velocity
		Parameters:
		qDot (numpy.array of floats)
			qDot[0] (float): left joint angular velocity in radians per second
			qDot[1] (float): right joint angular velocity in radians per second
		q (numpy.array of floats)
			q[0] (float): left joint angle in radians
			q[1] (float): right joint angle in radians
		Returns:
		(numpy.array of floats): numpy.array([vx,vy]) the end effector velocity
		"""
		velocity = np.dot(self.jacobian(q), qDot)
		return velocity
		

	def velocityToAngularVelocity(self,v,q):
		"""Converts the end effector velocity to joint angular velocities
		Parameters:
		v (numpy.array of floats)
			v[0] (float): x endpoint velocity
			v[1] (float): y endpoint velocity
		q (numpy.array of floats)
			q[0] (float): left joint angle in radians
			q[1] (float): right joint angle in radians
		Returns:
		(numpy.array of floats): numpy.array([qDot1,qDot2]) the joint angular velocities
		"""
		inverseJacobian = np.linalg.inv(self.jacobian(q))
		angularVelocity = np.dot(inverseJacobian,v)
		return angularVelocity  
		
		
	
	
	
class ArmController(Kinematics):
	"""This class is responsible for directly controlling the whole robot arm.
		It inherits a kinematics class which describes the kinematics of the robot arm
	"""
	def __init__(self):
		#initialize kinematics
		super().__init__()
		
		# calibrate motors before starting
		
		
		#initialize motors
		self.motorController = OdriveController()
		#motorController.calibrate()
		[self.leftMotor,self.rightMotor] = self.motorController.getMotors()
		
		# calibrate motors before starting
		leftInitialAngle = 180.0 # degrees
		self.leftMotor.calibrateAngularPosition(leftInitialAngle)
		rightInitialAngle = 90.0 # degrees
		self.rightMotor.calibrateAngularPosition(rightInitialAngle)		
		
		
	def calibratePosition(self, angles=[180.0, 90.0], delayTime=5, calibrateMotors=False):
		"""Use to calibrate that absolute angular position of the nanotec-motor with the robot arm
			
			Mount the robot arm in the configuration specified by the prompt given.
			
			Parameters:
			angles (list of floats):
				angles[0]: left joint angle in degrees
				angles[1]: right joint angle in degrees
			delayTime (int): time in seconds to give user to calibrate motors
			calibrateMotors (bool): if True calibrate motors, else skip this calibration
			Returns:
			None
		"""
		leftAngle = angles[0]
		rightAngle = angles[1]
		
		self.stop()
		print("You have " + str(delayTime) + " seconds to completed the following:")
		print("Place left motor angle at " + str(leftAngle) + " degrees")
		print("Place right motor angle at " + str(rightAngle) + " degrees")
		time.sleep(delayTime)
		
		print("Calibrating...")
		if calibrateMotors == True:
			self.motorController.calibrate()
			[self.leftMotor,self.rightMotor] = self.motorController.getMotors()
			
		self.leftMotor.calibrateAngularPosition(leftAngle)
		self.rightMotor.calibrateAngularPosition(rightAngle)
		print("Motors calibrated")
		return
		
	def printPositionInformation(self):
		"""Prints the position information for the robot"""
		rightAngleInDegrees = self.rightMotor.getAbsoluteAngularPosition()
		leftAngleInDegrees = self.leftMotor.getAbsoluteAngularPosition()
		print("Right Motor: " + str(rightAngleInDegrees))
		print("Left Motor: " + str(leftAngleInDegrees))
		
		position = self.getPosition()
		print("x: " +  str(position[0]) + ", y: " + str(position[1]))
		print("")   

		
	def printPositionInformationContinuously(self):
		"""prints the angle of each motor in degrees
		"""
		while(True):
			self.printPositionInformation()
			time.sleep(1)

	def stop(self):
		"""Method that sends the commands to stops the motors.
		
			Returns:
			None    
		"""
		# Disable motor PWM and do nothing
		self.leftMotor.stop()
		self.rightMotor.stop()
		return
	
	def getJointAngles(self):
		"""Returns the joint angles of the robot arm in radians
		
		Returns
		(numpy.array of floats)
			result[0]: left joint angle in radians
			result[1]: right joint angle in radians
		"""
		leftAngleInDegrees = self.leftMotor.getAbsoluteAngularPosition()
		rightAngleInDegrees = self.rightMotor.getAbsoluteAngularPosition()
		
		degreesToRadians = np.pi / 180.0
		
		leftAngleInRadians = leftAngleInDegrees * degreesToRadians
		rightAngleInRadians = rightAngleInDegrees * degreesToRadians
		q1 = leftAngleInRadians
		q2 = rightAngleInRadians
		q = np.array([q1,q2])
		return q

	def getPosition(self):
		"""Returns the position of the robot arm in meters
		
			Returns:
			(numpy.array of floats)
				result[0] (float): x end effector position in meters
				result[1] (float): y end effector position in meters
		"""
		q = self.getJointAngles()	
		position = self.forwardKinematics(q)
		return position
		
	def setPosition(self,r,speed=30):
		"""moves robot arm to a particular position
		
		Parameters:
		r (numpy.array of floats)
			r[0] (float): x end effector position in meters
			r[1] (float): y end effector position in meters
		speed (float): speed for actuators to move in rpm (This will be changed later)
		
		Returns:
		None
		"""
		jointAngles = self.inverseKinematics(r)
		
		radiansToDegrees = 180.0 / np.pi
		leftAngleInDegrees = jointAngles[0] * radiansToDegrees
		rightAngleInDegrees = jointAngles[1] * radiansToDegrees
		self.rightMotor.setAbsoluteAngularPositionShortestPath(rightAngleInDegrees,speed)
		self.leftMotor.setAbsoluteAngularPositionShortestPath(leftAngleInDegrees,speed)
	
	def getVelocity(self):
		"""Returns the velocity of the robot arm in meters per second
		
			Returns:
			(numpy.array of floats)
				result[0] (float): x end effector velocity in meters per second
				result[1] (float): y end effector velocity in meters per second
		"""
		rpmToRadPerSec = np.pi/30 # to convert rpm to radians per second
		leftAngVel = self.leftMotor.getAngularVelocity() * rpmToRadPerSec
		rightAngVel = self.rightMotor.getAngularVelocity() * rpmToRadPerSec
		
		# scale angular velocities to account for gear ratio
		leftAngVel = leftAngVel / self.gearRatio
		rightAngVel = rightAngVel / self.gearRatio
		
		qDot = np.array([leftAngVel,rightAngVel])
		q = self.getJointAngles()
		velocity = self.angularVelocityToVelocity(qDot,q)
		return velocity
	
	def setVelocity(self,v):
		"""moves robot arm at a particular velocity
		
		Parameters:
		v (numpy.array of floats)
			v[0] (float): x end effector velocity in meters per second
			v[1] (float): y end effector velocity in meters per second
		
		Returns:
		None
		"""
		radPerSecToRPM = 30 / np.pi
		q = self.getJointAngles()
		angularVelocity = self.velocityToAngularVelocity(v,q)
		angularVelocityRPM = angularVelocity * radPerSecToRPM
		angularVelocityScaled = angularVelocityRPM * self.gearRatio # account for gear ratio
		
		# set motor angular velocity in rpms using ints
		self.leftMotor.setAngularVelocity(int( angularVelocityScaled[0] )) 
		self.rightMotor.setAngularVelocity(int( angularVelocityScaled[1] ))   
		
	
	def getForce(self):
		"""Returns the force of the robot arm in Newtons
		
			Returns:
			(numpy.array of floats)
				result[0] (float): x end effector force in Newtons
				result[1] (float): y end effector force in Newtons
		"""
		ratedCurrentToNm = 0.5/1000 # 0.1% rated current to holding torque Nm
		leftTorque = self.leftMotor.getTorque() * ratedCurrentToNm
		rightTorque = self.rightMotor.getTorque() * ratedCurrentToNm
		
		# scale torque to account for gear ratio
		leftTorque = leftTorque * self.gearRatio
		rightTorque = rightTorque * self.gearRatio
		
		torque = np.array([leftTorque,rightTorque])
		q = self.getJointAngles()
		force = self.torqueToForce(torque,q)
		return force
	
	def setForce(self,f):
		"""
		moves robot arm at a particular force
		
		Parameters:
		v (numpy.array of floats)
			f[0] (float): x end effector force in Newtons
			f[1] (float): y end effector force in Newtons
		
		Returns:
		None
		"""
		NmToRatedCurrent = 1000/0.5 # holding torque Nm to 0.1% rated current
		q = self.getJointAngles()
		# minus sign because robot arm is opposing force
		torque = -self.forceToTorque(f,q) * NmToRatedCurrent # units of rated current
		torque = torque / self.gearRatio # account for gear ratio
		
		# perform type conversion to int and set maximum threshold value
		maxTorquePercent = 1000
		torque[0] = min(torque[0],maxTorquePercent)
		torque[1] = min(torque[1],maxTorquePercent)
		torque[0] = max(torque[0],-maxTorquePercent)
		torque[1] = max(torque[1],-maxTorquePercent)
		
		# perform type conversion to int and set torque
		leftTorque = int(round(torque[0],-2))
		rightTorque = int(round(torque[1],-2))
		#print("torque: " + str([leftTorque,rightTorque]))
		maxAngVel = 30 # rpm, make sure motor does not spin too fast
		self.leftMotor.setTorque(leftTorque, maxAngVel)
		self.rightMotor.setTorque(rightTorque, maxAngVel)
	
	def setImpedance(self,impedanceMatrix,referencePosition,referenceVelocity=0):
		"""
		moves robot arm at a particular impedance about a particular position
		
		Parameters:
		impedanceMatrix (numpy.array of numpy.arrays of floats): numpy.array([[kx,bx],[ky,by]])
			kx is the x end effector springyness in Newtons per meter
			ky is the y end effector springyness in Newtons per meter
			bx is the x end effector damping in Newtons per (meters per second)
			by is the y end effector damping in Newtons per (meters per second)     
		referencePosition (numpy.array of floats)
			position[0] (float): x end effector position in meters
			position[1] (float): y end effector position in meters
			
		Returns:
		None
		"""
		currentPosition = self.getPosition()
		deltaPosition = currentPosition - referencePosition
		
		currentVelocity = self.getVelocity()
		deltaVelocity = currentVelocity - referenceVelocity
		
		# extract impedance parameters
		kx = impedanceMatrix[0][0]
		ky = impedanceMatrix[1][0]
		bx = impedanceMatrix[0][1]
		by = impedanceMatrix[1][1]
		
		# impedance control equations
		fx = kx*deltaPosition[0] + bx*deltaVelocity[0]
		fy = ky*deltaPosition[1] + by*deltaVelocity[1]
		f = np.array([fx,fy])
		
		self.setForce(f)
		
	def setImpedanceAlongPath(path,impedanceFunction,epsilon):
		""" Sets and impedance profile along a path
			
			Parameters:
			path (list of numpy.arrays of floats)
				path[0]: start position of path
				path[1]: end position of path
			impedanceFunction (function): function that returns an impedance matrix (numpy.array or numpy.arrays of floats) when called
											This function can depend on both time and position and can take path as an argument.
			epsilon: distance to path end that user
		"""
		K = impedanceFunction(path)
		currentPosition = self.getPosition()
		
		# if reference position is below starting position
		raise NotImplementedError
		



		
	
		
		






def main():
	arm = ArmController()
	#arm.printPositionInformationContinuously()
	
	#import testKinematics
	#testKinematics.main()
	
	#import testPositionControl
	#testPositionControl.main()

if __name__ == "__main__":
	main()

