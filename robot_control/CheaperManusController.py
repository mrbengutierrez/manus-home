"""
This file constructs an arm simulator for the cheaper MIT MANUS

Author: Benjamin Gutierrez
email: bengutie@mit.edu
"""


import time # for print functions


import numpy as np
import matplotlib.pylab as plt
import scipy as sp

# import python library to control nanotec motors
from robot_control.NanotecLibrary import NanotecWrapper as NanotecMotor

class Graphics:

	def __init__(self):
		"""Constructor for Graphics object"""
		pass

	def plotPosition(x,y):
		""" plots the position of the robot on the screen"""
		pass



		


	
		
		
	
class ArmController:
	def __init__(self):
		inchesToMeters = 0.0254;
		self.l1 = 13.25 * inchesToMeters
		self.l2 = 13.25 * inchesToMeters
		self.l3 = 15.5 * inchesToMeters
		self.l4 = 15.5 * inchesToMeters
		self.d = 3 * inchesToMeters
		
		serialPort0 = "/dev/ttyACM0"
		ID0 = 0
		self.rightMotor = NanotecMotor(serialPort0,ID0)
		
		serialPort1 = "/dev/ttyACM1"
		ID1 = 1
		self.leftMotor = NanotecMotor(serialPort1,ID1)

	def forwardKinematics(self,q1,q2):
		"""converts joint angles to end effector position

		Parameters:
		q1 (float): left joint angle
		q2 (float): right joint angle

		Returns:
		(tuple of floats): (x,y) The end effector position
		"""
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

		return (x,y)

	def inverseKinematics(self,x,y):
		"""converts end effector position to joint angles

		Parameters:
		x (float): x end effector position in meters
		y (float): y end effector position in meters

		Returns:
		(tuple of floats): (x,y) The joint parameters
		"""

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

		return (q1,q2)

	def Jacobian(self,q1,q2):
		"""Returns the Jacobian matrix for a given set of joint angles

		Parameters:
		q1 (float): left joint angle in radians
		q2 (float): right joint angle in radians

		Returns:
		(numpy.matrix): the Jacobian matrix
		"""
		pass

	def computeActualJacobian(self,q):
		"""Returns the Jacobian matrix for a given set of joint angles
			using the actual Jacobian

		Parameters:
		q (tuple of floats): joint angles in radians, q[0] is left, q[1] is right

		Returns:
		(2x2 numpy.array): the Jacobian matrix
		"""
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
		return np.array([[dXQ1,dXQ2],[dYdQ1,dYdQ2]])


	def torqueToForce(self,t1,t2):
		"""Converts joint torques to enpoint forces

		Parameters:
		t1 (float): left joint torque in newton-meters
		t2 (float): right joint angle in newton-meters

		Returns:
		(tuple of floats): (fx,fy) the end effector forces
		"""
		# TODO
		return (0,0)

	def forceToTorque(self,fx,fy):
		"""Converts endpoint forces to joint torques

		Parameters:
		fx (float): x endpoint force in newtons
		fy (float): y endpoint force in newtons

		Returns:
		(tuple of floats): (t1,t2) the joint torques
		"""
		# TODO
		return (0,0)

	def angularVelocityToVelocity(self,qDot1,qDot2):
		"""Converts joint angular velocities to end effector velocity

		Parameters:
		qDot1 (float): left joint angular velocity in radians per second
		qDot2 (float): right joint angular velocity in radians per second

		Returns:
		(tuple of floats): (vx,vy) the end effector velocity
		"""
		# TODO
		return (0,0)

	def velocityToAngularVelocity(self,vx,vy):
		"""Converts the end effector velocity to joint angular velocities

		Parameters:
		vx (float): x endpoint velocity
		vy (float): y endpoint velocity

		Returns:
		(tuple of floats): (qDot1,qDot2) the joint angular velocities
		"""
		# TODO
		return (0,0)      

	def setPosition(self,x,y,speed=10):
		"""moves robot arm simulator to position
		
		Parameters:
		x (float): x end effector position in meters
		y (float): y end effector position in meters
		speed (float): speed for actuators to move in rpm (This will be changed later)
		
		Returns:
		None
		"""
		jointAngles = self.inverseKinematics(x,y)
		
		radiansToDegrees = 180.0 / np.pi
		leftAngleInDegrees = jointAngles[0] * radiansToDegrees
		rightAngleInDegrees = jointAngles[1] * radiansToDegrees
		self.rightMotor.setAbsoluteAngularPositionShortestPath(rightAngleInDegrees,speed)
		self.leftMotor.setAbsoluteAngularPositionShortestPath(leftAngleInDegrees,speed)
		

	def moveAngle(q1,q2):
		"""moves robot arm simulator to angle"""
		return
	
	def calibratePosition(self):
		"""Use to calibrate that absolute angular position of the nanotec-motor with the robot arm
			
			Mount the robot arm in the configuration specified by the prompt given.
		"""
		self.rightMotor.setAbsoluteAngularPositionShortestPath(90.0)
		self.leftMotor.setAbsoluteAngularPositionShortestPath(180.0)
		time.sleep(1)
		self.printPositionInformation()
		time.sleep(5)
		self.rightMotor.stop()
		self.leftMotor.stop()
		
	def printPositionInformation(self):
		"""Prints the position information for the robot"""
		rightAngleInDegrees = self.rightMotor.getAbsoluteAngularPosition()
		leftAngleInDegrees = self.leftMotor.getAbsoluteAngularPosition()
		print("Right Motor: " + str(rightAngleInDegrees))
		print("Left Motor: " + str(leftAngleInDegrees))
		
		position = self.getPosition()
		print("x: " +  str(position[0]) + "y: " + str(position[1]))
		print("")	

		
	def printPositionInformationContinuously(self):
		"""prints the angle of each motor in degrees"""
		while(True):
			self.printPositionInformation()
			time.sleep(1)
		
	def getPosition(self):
		"""Returns the position of the robot arm in meters"""
		rightAngleInDegrees = self.rightMotor.getAbsoluteAngularPosition()
		leftAngleInDegrees = self.leftMotor.getAbsoluteAngularPosition()
		
		degreesToRadians = np.pi / 180.0
		
		rightAngleInRadians = rightAngleInDegrees * degreesToRadians
		leftAngleInRadians = leftAngleInDegrees * degreesToRadians
		q1 = leftAngleInRadians
		q2 = rightAngleInRadians
		
		position = self.forwardKinematics(q1,q2)
		return position
		
		






def main():
	arm = ArmController()
	arm.printPositionInformationContinuously()

if __name__ == "__main__":
	main()

