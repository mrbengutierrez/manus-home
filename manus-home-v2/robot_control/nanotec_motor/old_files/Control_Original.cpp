/**
 * Class Control, code file with constructors and all methods.
 *
 * Class to control a Nanotec PD2-C motor through USB in Linux.
 *
 * @author Moises Alencastre-Miranda
 * @date 05/17/2018
 * @version 1.5
 */

#include "Control.h"


/**
 * Default Constructor.
 */
Control::Control()
{
  _nanotec = new CommunicationNT();
}


/**
 * Default Constructor.
 */
Control::~Control()
{
  free( _nanotec);
}


/**
 * Method that manage the main menu with options to control and test the motor.
 */
void Control::menu()
{
  int torque = 0, c = 0;
  message(); // Display menu options.
  // Initialize in zero torque, 100% of maximum torque and slope and 1.8A of
  // maximum and nominal current.
  _nanotec->torqueMode( 0, 1000, 1800, 1800, 1000 );

  while ( c != 27 )
  {
    c = getchar();
    switch ( c )
    {
      case 100: // 'd' decrease -100
        if ( torque > -1000 )
        {
          torque -= 100;
          _nanotec->changeTorque( torque );
          printf("set torque=%d, %d%c\n", torque, torque/10, 37 );
        }
        else
          printf("minimum torque -1000 = -100%c\n", 37);
        break;
      case 105: // 'i' increase +100
        if ( torque < 1000 )
        {
          torque += 100;
          _nanotec->changeTorque( torque );
          printf("set torque=%d, %d%c\n", torque, torque/10, 37 );
        }
        else
          printf("maximum torque 1000 = 100%c\n", 37);
        break;
      case 122: // 'z' zero.
          torque = 0;
          _nanotec->changeTorque( torque );
          printf("set torque=%d\n", torque );
        break;
      case 109: // 'm' minimum -1000
          torque = -1000;
          _nanotec->changeTorque( torque );
          printf("set torque=%d\n", torque );
        break;
      case 77: // 'M' maximum +1000
          torque = 1000;
          _nanotec->changeTorque( torque );
          printf("set torque=%d\n", torque );
        break;
      case 112: // 'p' position.
          cout << "angle: " << _nanotec->readPosition( 0 ) << endl;
        break;
      case 97: // 'a' torque controlled by an arc or angle.
          torqueControlByAngleRange( -50, 50 );
          c = 27;
        break;
      case 116: // 't' test specific torque values.
          _nanotec->changeTorque( 723 ); // Problems in 9, 10, 
        break;
    }
  }
  _nanotec->stop();
  _nanotec->closePort();
}


/**
 * Method to display the menu options.
 */
void Control::message()
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
void Control::torqueControlByAngleRange( double minA, double maxA )
{
  double angle = 0.0, dif = 0.0; // Actual angle and difference with minA & maxA
  char c = 'A';
  int torque = 0;

  // Loop to read the angle.
  while ( c != 'q' )
  {
    angle = _nanotec->readPosition( 0 );
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
    _nanotec->changeTorque( torque );
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
int Control::calculateSpringForce( double disAng )
{
  // Convert the displacement to radians and calculate the force (rounded to the
  // closest integer).
  return round( STIFF * VALMAP * disAng * M_PI / 180.0);
}


