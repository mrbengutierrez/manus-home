/**
 * 
 * This file is responsible for calibrating the nanotec motors.
 * This file must exist because of the gearboxes attached to the nanotec motors.
 * Without calibration it would be impossible to know where the robot end effector is.
 * 
 * Convention
 * ID = 0, leftMotorCalibration.txt
 * ID = 1, rightMotorCalibration.txt
 * 
 * @author Benjamin Gutierrez
 * @date 08/23/2019
 * 
 */
 
 #include "NanotecMotor.h"
 
 int main() {
	 
	 // set up calibration for right motor
	 int ID0 = 0;
	 const char* serialPort0 = "/dev/ttyACM0";
	 NanotecMotor* rightMotorPointer = new NanotecMotor(serialPort0,ID0);
	 std::string rightMotorFile = "rightMotorCalibration.txt";
	 double rightMotorCalibrationAngle = 0.0;
	 rightMotorPointer->setCalibration(rightMotorCalibrationAngle,rightMotorFile);
	 rightMotorPointer->closePort();
	 
	 // set up calibration for right motor
	 int ID1 = 1;
	 const char* serialPort1 = "/dev/ttyACM1";
	 NanotecMotor* leftMotorPointer = new NanotecMotor(serialPort1,ID1);
	 std::string leftMotorFile = "leftMotorCalibration.txt";
	 double leftMotorCalibrationAngle = 90.0;
	 leftMotorPointer->setCalibration(leftMotorCalibrationAngle,leftMotorFile);
	 leftMotorPointer->closePort();
	 
	 return 0;
 }
