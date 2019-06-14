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
 * Default Constructor.
 */
NanotecMotor::~NanotecMotor()
{
  free( _nanotec);
  
}

/*
 * Returns the name of the motor
 * 
 */
int NanotecMotor::getID() {
	return _ID;
}

/**
 * Method that manage the main menu with options to control and test the motor.
 */
void NanotecMotor::menu()
{
  int torque = 0, c = 0;
  message(); // Display menu options.
  // Initialize in zero torque, 100% of maximum torque and slope and 1.8A of
  // maximum and nominal current.
  torqueMode( 0, 1000, 1800, 1800, 1000 );

  while ( c != 27 )
  {
    c = getchar();
    switch ( c )
    {
      case 100: // 'd' decrease -100
        if ( torque > -1000 )
        {
          torque -= 100;
          setTorque( torque );
          printf("set torque=%d, %d%c\n", torque, torque/10, 37 );
        }
        else
          printf("minimum torque -1000 = -100%c\n", 37);
        break;
      case 105: // 'i' increase +100
        if ( torque < 1000 )
        {
          torque += 100;
          setTorque( torque );
          printf("set torque=%d, %d%c\n", torque, torque/10, 37 );
        }
        else
          printf("maximum torque 1000 = 100%c\n", 37);
        break;
      case 122: // 'z' zero.
          torque = 0;
          setTorque( torque );
          printf("set torque=%d\n", torque );
        break;
      case 109: // 'm' minimum -1000
          torque = -1000;
          setTorque( torque );
          printf("set torque=%d\n", torque );
        break;
      case 77: // 'M' maximum +1000
          torque = 1000;
          setTorque( torque );
          printf("set torque=%d\n", torque );
        break;
      case 112: // 'p' position.
          cout << "angle: " << getAbsoluteAngularPosition() << endl;
        break;
      case 97: // 'a' torque controlled by an arc or angle.
          torqueControlByAngleRange( -50, 50 );
          c = 27;
        break;
      case 116: // 't' test specific torque values.
          setTorque( 100 ); // Problems in 9, 10, 
        break;
    }
  }
  stop();
  closePort();
}


/**
 * Method to display the menu options.
 */
void NanotecMotor::message()
{
  cout << "torque = 0\n"
  "Press: 'd' to decrease in 100 less the torque (counterclockwise)\n"
  "       'i' to increase in 100 more the torque (clockwise)\n"
  "       'z' to put the torque to zero\n"
  "       'm' to put the torque to the minimum -1000\n"
  "       'M' to put the torque to the maximum 1000\n"
  "       'p' to read the actual position (angle with respect to the initial)\n"
  "       'a' to enter to the torque controlled by angle\n"
  "       't' to test an specific torque value\n"
  "       'ESC' or 'q' to exit\n" << endl;
}


/**
 * Method to control the torque depending on the angle. If the angle is between
 * minA and maxA the torque will be zero, if the angle is less than minAng
 * or greater than maxAng then the torque value will push in the oposite
 * direction to mantain the angle inside of the limits with torque zero.
 *
 * @param minAng  Minimum angle to mantain the torque in zero
 * @param maxAng  Maximum angle to mantain the torque in zero
 */
void NanotecMotor::torqueControlByAngleRange( double minA, double maxA )
{
  double angle = 0.0, dif = 0.0; // Actual angle and difference with minA & maxA
  char c = 'A';
  int torque = 0;

  // Loop to read the angle.
  while ( c != 'q' )
  {
    angle = getAbsoluteAngularPosition();
    if ( _lastAng != angle )
      cout << "angle: " << angle << endl;

    if ( angle > maxA ) // Positive side of the range.
    {
      dif = maxA - angle; // Negative difference.
      // Negative torque, counterclockwise.
      torque = 0;//calculateSpringForce( dif );
    }
    else if ( angle < minA ) // Negative side of the range.
    {
      dif = minA - angle; // Positive difference.
      // It seems that the positive torque (clockwise) has less force, this was 
      //incremented in 20%.  Display of the torque. Measure processing time.
      // Positive torque, clockwise.
      torque = 0;//calculateSpringForce( dif )*1.2;
    }
    else
      torque = 0;

    // Checking special cases.
    if ( torque > 1000 ) torque = 1000; // The maximum.
    // If the torque is less or equal than 1% (10) in both cases (positive or
    // negative) is considered a torque value of 1.1% (11).
    //if ( torque == 9 || torque == 10 ) torque = 11; // Problem with that motor
    if ( torque > 0 && torque < 11 ) torque = 11; // Problem with that motor.
    if ( torque < 0 && torque > -11 ) torque = -11; // Problem with that motor.

    // Sending the torque value.
    setTorque( torque );
/*
    if ( _lastDif != dif )
      cout << "dif: " << dif << endl;
    if ( _lastTor != torque )
      cout << "torque: " << torque << endl;
*/
    _lastAng = angle;
    _lastTor = torque;
    _lastDif = dif;
  }
}


/**
 * Function to simulate a spring, calculating the needed force to have an
 * specific displacement in radians.
 * F = k * x Force is equal to the stiffness times the displacement in m
 * T = K * r Torque is equal to the stiffness times the displacement in radians
 *
 * @param dif  Displacement of the angle in degrees
 *
 * @return  Torque value as a integer (decimal) percentage (1000=100%)
 */
int NanotecMotor::calculateSpringForce( double disAng )
{
  // Convert the displacement to radians and calculate the force (rounded to the
  // closest integer).
  return round( STIFF * VALMAP * disAng * M_PI / 180.0);
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






	

