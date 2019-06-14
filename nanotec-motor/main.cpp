/**
 * Main program to control a Nanotec PD2-C motor through USB in a Linux
 * computer.
 *
 * @author Moises Alencastre-Miranda
 * @author Benjamin Gutierrez
 * @date 06/10/2019
 * @version 1.6
 */

#include "NanotecMotor.h"
#include "unistd.h"


void printMotorInformation(NanotecMotor *motor) {
	sleep(1);
	cout << endl;
	cout << "Motor ID: " << motor->getID() << endl;
	cout << "encoder value: " << motor->readPhysicalEncoder() << endl;
	cout << "anglular position: " << motor->getAbsoluteAngularPosition() << endl;
	cout << "angular velocity: " << motor->getAngularVelocity() << endl;
	cout << "torque: " << motor->getTorque() << endl;
	cout << endl;
}

/**
 * Main program.
 */ 
int main ( int argc, char **argv ) {


  const char *serialPort0 = "/dev/ttyACM0";
  const int ID0 = 1;
  NanotecMotor *firstMotor = new NanotecMotor(serialPort0,ID0);
  //const char *serialPort1 = "/dev/ttyACM1";
  //const int ID1 = 2;
  //NanotecMotor *secondMotor = new NanotecMotor(serialPort1,ID1);
  
  
  int sleepTime = 5;
  
  // Read initial configuration
  cout << "Initial Configuration" << endl;
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  
  // angular position
  cout << "setAngularPosition" << endl;
  
  firstMotor->angularPositionMode();
  //secondMotor->angularPositionMode();
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  
  firstMotor->setAbsoluteAngularPosition(180.0);
  //secondMotor->setAbsoluteAngularPosition(180.0);
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  sleep(sleepTime);
  
  firstMotor->setAbsoluteAngularPosition(360.0,100);
  //secondMotor->setAbsoluteAngularPosition(360.0,100);
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  sleep(sleepTime);
  
  firstMotor->setAbsoluteAngularPosition(-180.0);
  //secondMotor->setAbsoluteAngularPosition(-180.0);
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  sleep(sleepTime);
  
  firstMotor->setAbsoluteAngularPosition(0.0);
  //secondMotor->setAbsoluteAngularPosition(0.0);
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  sleep(sleepTime);
  
  // angular velocity
    cout << "setAngularVelocity" << endl;
  
  //secondMotor->angularVelocityMode();
  firstMotor->angularVelocityMode();
  
  //secondMotor->setAngularVelocity(100);
  firstMotor->setAngularVelocity(100);
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  sleep(sleepTime);
  
  //secondMotor->setAngularVelocity(-100);
  firstMotor->setAngularVelocity(-100);
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  sleep(sleepTime);
  
  //secondMotor->setAngularVelocity(0);
  firstMotor->setAngularVelocity(0);
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  sleep(sleepTime);
  
  // torque
    cout << "setTorque" << endl;  
  firstMotor->torqueMode();
  //secondMotor->torqueMode();
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  
  firstMotor->setTorque(50);
  //secondMotor->setTorque(50);
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  sleep(sleepTime);
  
  firstMotor->setTorque(-50);
  //secondMotor->setTorque(-50);
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  sleep(sleepTime);
  
  firstMotor->setTorque(0);
  //secondMotor->setTorque(0);
  printMotorInformation(firstMotor);
  //printMotorInformation(secondMotor);
  sleep(sleepTime);
  
  // stop motors
  firstMotor->stop();
  firstMotor->closePort();
  //secondMotor->stop();
  //secondMotor->closePort();
  cout << "Motors should stop now." << endl;

  
  
  
  
  return 1;
}








  /*
  // angular velocity
  firstMotor->torqueMode();
  firstMotor->setTorque(200);
  sleep(2);
  cout << "Angular Torque0: " << firstMotor->getTorque() << endl;
  sleep(4);
  firstMotor->setTorque(100);
  sleep(2);
  cout << "Angular Torque1: " << firstMotor->getTorque() << endl;
  sleep(4);
  firstMotor->setTorque(28);
  sleep(2);
  cout << "Angular Torque2: " << firstMotor->getTorque() << endl;
  sleep(4);  
  firstMotor->setTorque(-100);
  sleep(1);
  cout << "Angular Torque3: " << firstMotor->getTorque() << endl;
  sleep(4);
  firstMotor->setTorque(0);
  sleep(2);
  cout << "Angular Torque4: " << firstMotor->getTorque() << endl;
  sleep(4);
  */
  




/*
  while(1){
	  cout << "encoder: " << firstMotor->readEncoder() << endl;
	  cout << "angle: " << firstMotor->getAbsoluteAngularPosition() << endl;
	  sleep(1);
  }*/
  
  /*
  // angular position
  firstMotor->angularPositionMode();
  firstMotor->setRelativeAngularPosition(180.0);
  printPositionInformation(firstMotor);
  sleep(3);
  firstMotor->setRelativeAngularPosition(360.0,100);
  printPositionInformation(firstMotor);
  sleep(3);
  firstMotor->setRelativeAngularPosition(-180.0);
  printPositionInformation(firstMotor);
  sleep(3);
  firstMotor->setRelativeAngularPosition(0.0);
  printPositionInformation(firstMotor);
  sleep(3);
  
  // angular velocity
  firstMotor->angularVelocityMode();
  firstMotor->setAngularVelocity(100);
  sleep(2);
  firstMotor->setAngularVelocity(-100);
  sleep(3);
  firstMotor->setAngularVelocity(0);
  sleep(3);
  
  // torque  
  firstMotor->torqueMode();
  firstMotor->setTorque(50);
  sleep(3);
  firstMotor->setTorque(-50);
  sleep(3);
  firstMotor->setTorque(0);
  
  
  // absolute position
  cout << endl << endl;
  firstMotor->angularPositionMode();
  firstMotor->setAbsoluteAngularPosition(0.0);
  printPositionInformation(firstMotor);
  sleep(3);
  firstMotor->setAbsoluteAngularPosition(90.0,100);
  printPositionInformation(firstMotor);
  sleep(3);
  firstMotor->setAbsoluteAngularPosition(-175.0,100);
  printPositionInformation(firstMotor);
  sleep(3);
  firstMotor->setAbsoluteAngularPosition(0.0);
  printPositionInformation(firstMotor);
  sleep(3);  
  */








  /*
  const char *serialPort0 = "/dev/ttyACM0";
  NanotecMotor *firstMotor = new NanotecMotor(serialPort0);
  const char *serialPort1 = "/dev/ttyACM1";
  NanotecMotor *secondMotor = new NanotecMotor(serialPort1);
  
  // angular position
  firstMotor->angularPositionMode();
  secondMotor->angularPositionMode();
  firstMotor->changeAngularPosition(180.0);
  secondMotor->changeAngularPosition(180.0);
  cout << "angle: " << firstMotor->readPosition() << endl;
  sleep(3);
  firstMotor->changeAngularPosition(360.0,100);
  secondMotor->changeAngularPosition(360.0,100);
  cout << "angle: " << firstMotor->readPosition() << endl;
  sleep(3);
  firstMotor->changeAngularPosition(-180.0);
  secondMotor->changeAngularPosition(-180.0);
  cout << "angle: " << firstMotor->readPosition() << endl;
  sleep(3);
  firstMotor->changeAngularPosition(0.0);
  secondMotor->changeAngularPosition(0.0);
  cout << "angle: " << firstMotor->readPosition() << endl;
  sleep(3);
  
  // angular velocity
  secondMotor->angularVelocityMode();
  secondMotor->changeAngularVelocity(400);
  
  firstMotor->angularVelocityMode();
  firstMotor->changeAngularVelocity(100);
  sleep(3);
  firstMotor->changeAngularVelocity(-100);
  sleep(3);
  firstMotor->changeAngularVelocity(0);
  secondMotor->changeAngularVelocity(0);
  sleep(3);
  
  // torque
  secondMotor->torqueMode();
  secondMotor->changeTorque(100);
   
  firstMotor->torqueMode();
  firstMotor->changeTorque(50);
  sleep(3);
  firstMotor->changeTorque(-50);
  sleep(3);
  firstMotor->changeTorque(0);
  secondMotor->changeTorque(0);
  
  // stop motors
  firstMotor->stop();
  firstMotor->closePort();
  secondMotor->stop();
  secondMotor->closePort();
  cout << "Motor should stop now." << endl;
  */
