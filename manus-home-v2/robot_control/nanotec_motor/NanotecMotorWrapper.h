
/*
 * C wrapper around the C++ code – since the ctypes system cannot use C++ code
 * This wrapper is meant for a python wrapper that uses ctypes which 
 * is in the standard python library.
 */

// The extern "C" {} statement tells the C++ compiler to use the C style name mangling 
// so a C compiler will find the correct symbols in the object file later.
extern "C" 
{
	NanotecMotor* NanotecMotor_new(const char *serialPort, const int ID) 
	{
		return new NanotecMotor(serialPort, ID);
	}
	
	// method to get the ID number of the motor
	int NanotecMotor_getID( NanotecMotor* motor) 
	{
		return motor->getID();
	}
	// method to get the serial port of the motor
	char* NanotecMotor_getSerialPort( NanotecMotor* motor) 
	{
		return motor->getSerialPort();
	}
	
	// Modes of Operation
	void NanotecMotor_torqueMode(NanotecMotor* motor, int torque, int maxTorque, int maxCurr, int nomCurr, int slope)
	{
		return motor->torqueMode(torque, maxTorque, maxCurr, nomCurr, slope);
	}
	void NanotecMotor_angularVelocityMode(NanotecMotor* motor, int angVel)
	{
		return motor->angularVelocityMode(angVel);
	}
	void NanotecMotor_angularPositionMode(NanotecMotor* motor, double angPos, int angVel)
	{
		return motor->angularPositionMode(angPos, angVel);
	}
	
	// Methods to control the motor
	void NanotecMotor_setTorque(NanotecMotor* motor, int torque)
	{
		return motor->setTorque(torque);
	}
	void NanotecMotor_setAngularVelocity(NanotecMotor* motor, int angVel)
	{
		return motor->setAngularVelocity(angVel);
	}
	void NanotecMotor_setRelativeAngularPosition(NanotecMotor* motor, double angPos, int angVel)
	{
		return motor->setRelativeAngularPosition(angPos, angVel);
	}
	void NanotecMotor_setAbsoluteAngularPosition(NanotecMotor* motor, double angPos, int angVel)
	{
		return motor->setAbsoluteAngularPosition(angPos, angVel);
	}
	void NanotecMotor_setAbsoluteAngularPositionShortestPath(NanotecMotor* motor, double angPos, int angVel)
	{
		return motor->setAbsoluteAngularPositionShortestPath(angPos, angVel);
	}
	void NanotecMotor_stop(NanotecMotor* motor)
	{
		return motor->stop();
	}
	
	// Methods to get information from the motor
	int NanotecMotor_getTorque(NanotecMotor* motor)
	{
		return motor->getTorque();
	}
	int NanotecMotor_getAngularVelocity(NanotecMotor* motor)
	{
		return motor->getAngularVelocity();
	}
	double NanotecMotor_getAbsoluteAngularPosition(NanotecMotor* motor)
	{
		return motor->getAbsoluteAngularPosition();
	}
	int NanotecMotor_readPhysicalEncoder(NanotecMotor* motor)
	{
		return motor->readPhysicalEncoder();
	}
	
	// Method to close the serial port connection
	void NanotecMotor_closePort(NanotecMotor* motor)
	{
		return motor->closePort();
	}
		
	
}
