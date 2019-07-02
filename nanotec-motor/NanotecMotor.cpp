/**
 * Class NanotecMotor, code file with constructors and all methods.
 *
 * Class to control a Nanotec PD2-C motor through USB in Linux.
 *
 * @author Moises Alencastre-Miranda
 * @author Benjamin Gutierrez
 * @date 06/10/2019
 * @version 1.6
 */

#include "NanotecMotor.h"
#include "NanotecMotorWrapper.h"

// enumeration to keep track of motor mode types
//enum _motorModeType {NONE, TORQUE, ANGULAR_VELOCITY, ANGULAR_POSITION};


/** Default constructor for initializing containers
 * 
 * does nothing, DO NOT CALL
 */
 /*
NanotecMotor::NanotecMotor() {
}
*/

NanotecMotor& NanotecMotor::operator=(const NanotecMotor &oldNanotecMotor) {
	cout << "Nanotec Motor is being assigned. This is not allowed." << endl;
	throw;
}

NanotecMotor::NanotecMotor(const NanotecMotor &oldNanotecMotor) {
	cout << "Nanotec Motor is being copied. This is not allowed." << endl;
	throw;
}


/**
 * Default Constructor.
 * 
 * @param serialPort name of the port that the motor is connected to
 * @param ID (optional) a unique number to identify the motor.
 */
NanotecMotor::NanotecMotor(const char *serialPort, const int ID)
{
  _nanotec = new CommunicationNT(serialPort);
  
  _ID = ID;
  
  // restart port
  stop();
  closePort();
  delete _nanotec;
  _nanotec = new CommunicationNT(serialPort);
  
  _motorMode = NONE;
  
  // initialize virtual encoder resolution
  // virtual encoder position resolution = encoder increments / motor revolutions
  // set encoder increments = VIRTUAL_TICKS_PER_REV
  _nanotec->writeCommand( (unsigned char *)"\x60\x8F\x01", 4, VIRTUAL_TICKS_PER_REV );
  
  // set motor revolutions = 1;
  _nanotec->writeCommand( (unsigned char *)"\x60\x8F\x02", 4, 1 );
}


/**
 * Default Destructor.
 */
NanotecMotor::~NanotecMotor()
{
  delete _nanotec;
}

/*
 * Returns the name of the motor
 * 
 */
int NanotecMotor::getID() {
	return _ID;
}



/**
 * Method to activate the Profile Torque or torque profile.
 *
 * @param torque  Torque value in percentage (decimal value 0-1000=100%)
 * @param maxTorque  Maximum torque in percentage (decimal value 0-1000=100%)
 * @param maxCurr  Maximum current, commonly 1800 mA
 * @param nomCurr  Nominal current, commonly 1800 mA
 * @param slope  Slope to arrive to the torque, 1000 means go directly
 */
void NanotecMotor::torqueMode( int torque, int maxTorque, int maxCurr, int nomCurr, int slope )
{	
  // Restart motor
  stop();
  
  // Set the profile torque.
  _nanotec->writeCommand( (unsigned char *)"\x60\x60\x00", 1, 4 );

  // Set the torque value.
  _nanotec->writeCommand( (unsigned char *)"\x60\x71\x00", 2, torque );

  // Set the maximum current.
  _nanotec->writeCommand( (unsigned char *)"\x20\x31\x00", 4, maxCurr );

  // Set the nominal current.
  _nanotec->writeCommand( (unsigned char *)"\x20\x3B\x01", 4, nomCurr );

  // Set the maximum torque.
  _nanotec->writeCommand( (unsigned char *)"\x60\x72\x00", 2, maxTorque );

  // Set the slope.
  _nanotec->writeCommand( (unsigned char *)"\x60\x87\x00", 4, slope );

  // Enable voltage.
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 6 );

  // Switch on.
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 7 );

  // Enable operation.
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 15 );
  
   //motor is in torque mode
  _motorMode = TORQUE;	
}


/**
 * Method to change the torque value in real time.
 *
 * @param torque  Torque value in percentage (decimal value 0-1000=100%)
 */
void NanotecMotor::setTorque( int torque )
{

  // make sure motor is in torque mode
  if (_motorMode != TORQUE) {
	  torqueMode();
  }

  // Negatives case. -1 is FFFF, -2 FFFE, ...
  if ( torque < 0 ) {torque += 65536;} // negative torque + FFFF + 1
  
  // Set the torque value.
  _nanotec->writeCommand( (unsigned char *)"\x60\x71\x00", 2, torque );
}



/**
 * Method to activate the angular velocity control
 *
 * @param angVel  angular velocity value in rpm
 * 
 */
void NanotecMotor::angularVelocityMode(int angVel){

  // Restart motor
  stop();
	
  // Set to velocity mode
  _nanotec->writeCommand( (unsigned char *)"\x60\x60\x00", 1, 2 );
  
  // Set angular velocity
  _nanotec->writeCommand( (unsigned char *)"\x60\x42\x00", 2, angVel );

  // Enable voltage.
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 6 );  
  
  // Switch on.
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 7 );
  
  // Enable operation.
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 15 );
  
}


/**
 * Method to change the angular velocity value in real time.
 *
 * @param angVel  Angular velocity value in rpm
 */
void NanotecMotor::setAngularVelocity( int angVel )
{
  // make sure motor is in angular velocity mode
  if (_motorMode != ANGULAR_VELOCITY) {
	  angularVelocityMode();
  }
  
  // Negatives case. -1 is FFFF, -2 FFFE, ...
  if ( angVel < 0 ) {angVel += 65536;} // negative vel + FFFF + 1

  // Set angular velocity
  _nanotec->writeCommand( (unsigned char *)"\x60\x42\x00", 2, angVel );
}  



/**
 * Method to activate the angular position control
 *
 * @param angPos  angular position value (negative to reverse direction)
 *                (-360.0 <= angPos <= 360.0)
 * @param angVel  angular velocity value in rpm (must always be positive)
 * 
 */
void NanotecMotor::angularPositionMode(double angPos, int angVel){

  // convert degrees to encoderTics
  int angPosTicks = degreesToVirtualEncoderTicks(angPos);
  
  // Restart motor
  stop();
	
	
  // Set to profile angular position mode
  _nanotec->writeCommand( (unsigned char *)"\x60\x60\x00", 1, 1 );
  
  // Set profile angular velocity
  _nanotec->writeCommand( (unsigned char *)"\x60\x81\x00", 4, angVel );
  
  // Set profile target angular position
  _nanotec->writeCommand( (unsigned char *)"\x60\x7A\x00", 4, angPosTicks );
  
  // Enable voltage.
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 6 );  
  
  // Switch on.
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 7 );
  
  // Enable operation. , target position relative
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 0x4F );
  
  // Start operation.
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 0x5F );
  
}


/**
 * Method to change the relative angular position value in real time. 
 * The position is set using the current position as the zero position
 *
 * @param angPos  angular position value in degrees (negative to reverse direction)
 *                (-360.0 <= angPos <= 360.0)
 * @param angVel  angular velocity value in rpm (must always be positive)
 */
void NanotecMotor::setRelativeAngularPosition( double angPos, int angVel )
{

  // make sure motor is in angular velocity mode
  if (_motorMode != ANGULAR_POSITION) {
	  angularPositionMode();
  }
  
  // convert degrees to encoderTicks
  int angPosTicks = degreesToVirtualEncoderTicks(angPos);

  // Negatives case. -1 is FFFF, -2 FFFE, ...
  if ( angVel < 0 ){ angVel += 65536; } // negative vel + FFFF + 1

  if (angPosTicks < 0) { 
	  angPosTicks = -angPosTicks;
	  // Reverse direction of rotation
	  _nanotec->writeCommand( (unsigned char *)"\x60\x7E\x00", 1, 0x80 );  
  } else {
	  // Do NOT reverse direction of rotation
	  _nanotec->writeCommand( (unsigned char *)"\x60\x7E\x00", 1, 0x00 ); 
  }
   
   // Set profile target angular position
  _nanotec->writeCommand( (unsigned char *)"\x60\x7A\x00", 4, angPosTicks );
   
  // Set profile angular velocity
  _nanotec->writeCommand( (unsigned char *)"\x60\x81\x00", 4, angVel );
  
  // reset start bit 4, new target position must be acknowledged as new set point immediately(Bit 5)
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 0x2F );  
  
  // starts the absolute positioning
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 0x2F );  
  
   //Start operation.
   _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 0x5F );
}  

/**
 * Method to change the absolute angular position value in real time with ability to control direction.
 *
 * @param angPos  angular position value in degrees (negative to reverse direction)
 *                (-360.0 <= angPos <= 360.0)
 * @param angVel  angular velocity value in rpm (must always be positive)
 */
void NanotecMotor::setAbsoluteAngularPosition( double angPos, int angVel ) {
	const double currentPosition = getAbsoluteAngularPosition();
	const double degreesPerRevolution = 360.0;
	
	const double positiveAngularPosition = angPos * sign(angPos);
	
	// deltaPosition is the difference between target position and current position
	double deltaPosition = (positiveAngularPosition - currentPosition) * sign(angPos);
	if (deltaPosition < 0.0) { deltaPosition += degreesPerRevolution;} // make sure deltaPosition < 360.0 degrees
	deltaPosition *= sign(angPos); // account for direction of rotation
	
	setRelativeAngularPosition( deltaPosition, angVel );	
}

/**
 * Method to change the absolute angular position value in real time. 
 * Motor rotates in the shortest path to new target angular position
 *
 * @param angPos  angular position value in degrees (must always be positive)
 *                (0.0 <= angPos <= 360.0)
 * @param angVel  angular velocity value in rpm (must always be positive)
 */
void NanotecMotor::setAbsoluteAngularPositionShortestPath( double angPos, int angVel ) {
	const double currentPosition = getAbsoluteAngularPosition();
	const double deltaPosition = angPos - currentPosition;
	setRelativeAngularPosition(deltaPosition);
}


/**
 * Returns 1.0 if value >= 0.0, else returns -1.0
 * 
 * @param value value to take sign of
 */
double NanotecMotor::sign (double value){
	if (value >= 0.0) {return 1.0;}
	return -1.0;
}

/**
 * Converts degrees to the number of virtual encoder ticks
 * 
 * @param degrees number of degrees (0 <= degrees <= 360) 
 */
int NanotecMotor::degreesToVirtualEncoderTicks(double degrees) {
	double degreesPerRev = 360.0;
	double encoderTicks = degrees / degreesPerRev * (double) VIRTUAL_TICKS_PER_REV;
	return (int) encoderTicks;
}

/**
 * Converts degrees to the number of physical encoder ticks
 * 
 * @param degrees number of degrees (0 <= degrees <= 360) 
 */
int NanotecMotor::degreesToPhysicalEncoderTicks(double degrees) {
	double degreesPerRev = 360.0;
	double encoderTicks = degrees / degreesPerRev * (double) PHYSICAL_TICKS_PER_REV;
	return (int) encoderTicks;
}



/**
 * Reads the value of the encoder
 * 
 * @return value of the encoder (0 <= value <= 4095)
 */
int NanotecMotor::readPhysicalEncoder() {
		
  // Read the encoder.
  const int position = (int) _nanotec->readCommand( (unsigned char *)"\x60\x63\x00", 0, 0 );
  
  return position%PHYSICAL_TICKS_PER_REV;
}

/**
 * Returns the current angular velocity in rpm
 */
 int NanotecMotor::getAngularVelocity() {
 
  // Read the angular velocity.
  return (int) _nanotec->readCommand( (unsigned char *)"\x60\x6C\x00", 0, 0 );
}

/**
 * Returns the torque as thousandths of the torque, 
 * 
 * @return value of the angular torque as thousandths of the torque, 
 * e.g., the value "500" means "50%" of the rated torque;
 * (0 <= value <= 1000)
 */
 int NanotecMotor::getTorque() {
 
   // Read the angular velocity. //  TESTING
  const int velocity = (int)_nanotec->readCommand( (unsigned char *)"\x60\x6C\x00", 0, 0 ); //  TESTING
 
  // Read the torque.
  const int torque = (int) _nanotec->readCommand16bit( (unsigned char *)"\x60\x77\x00", 0, 0 );
  
  return torque;
}
 
 
/**
 * Returns the absolute angular position of the motor shaft in degrees
 * 
 */
double NanotecMotor::getAbsoluteAngularPosition() {
	const double degreesPerRevolution = 360.0;
	return (double) readPhysicalEncoder() * degreesPerRevolution / PHYSICAL_TICKS_PER_REV;
}


/**
 * Method that sends the commands to stop the motor.
 */
void NanotecMotor::stop()
{
    // Switch off. 
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 0 );//(unsigned char *)"\x00\x02",  (unsigned char *)"\x07\x00" );

  // Disable voltage. 
  _nanotec->writeCommand( (unsigned char *)"\x60\x40\x00", 2, 0 );//(unsigned char *)"\x00\x02",  (unsigned char *)"\x06\x00" );
}

/**
 * Method to close the port of the serial communication.
 */
void NanotecMotor::closePort()
{
  _nanotec->closePort();
}






	

