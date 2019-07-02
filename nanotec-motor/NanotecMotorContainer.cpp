		
/**
 * This cpp file is responsible for managing multiple NanotecMotor.h objects
 * 
 * @author Benjamin Gutierrez (bengutie@mit.edu)
 * @date July 2, 2019
 * 
 */


#include "NanotecMotorContainer.h"		

NanotecMotorContainer::NanotecMotorContainer() {
	_numMotors = 0;
}
		
/** Inserts a nanotec motor into a nanotec motor container
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 * 		  serialPort 
 * @param motor NanotecMotor object that is used by the Nanotec motor
 */
void NanotecMotorContainer::insert(NanotecMotor* motor) {
	cout << "Inserted at _numMotors = " <<  _numMotors << endl;  // TESTING
	_nanotecMotorArray[_numMotors] = motor;
	_numMotors++;
	return;
}


/** Returns the NanotecMotor using the serialport, if nanotec motor does not exist returns -1
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 * 
 */		
int NanotecMotorContainer::getMotorIndex(std::string serialPort) {
	for(int i = 0; i != _numMotors; i++) { // for each motor
		char* currentSerialPortPointer = _nanotecMotorArray[i]->getSerialPort(); // get char* serial port, returns copy of char*
		std::string currentSerialPort( currentSerialPortPointer ); // get string serial port
		if ( currentSerialPort.compare(serialPort) == 0 ) {
			delete currentSerialPortPointer; // free char* memory
			return i;
		}
		delete currentSerialPortPointer; // free char* memory
	}
	return -1;
}


/** Returns true if the container contains a motor with the serialPort specified, else returns false
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 */		
bool NanotecMotorContainer::contains(std::string serialPort) {
	if (getMotorIndex(serialPort) != -1 ) {
		return true;
	}
	return false;
}


/** Returns the NanotecMotor using the serialport
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 *        serialPort must be in the NanotecMotorContainer
 */		
NanotecMotor* NanotecMotorContainer::getMotor(std::string serialPort) {
	int index = getMotorIndex(serialPort);
	
	// if nanotec motor does not exist throw exception
	if (index == -1) {
		cout << "Error motor using serialport " << serialPort << " not in nanotec motor container" << endl;
		throw;
	}
	return _nanotecMotorArray[index];
}


/** Removes the NanotecMotor using the serialport
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 *        serialPort must be in the NanotecMotorContainer
 */		
void NanotecMotorContainer::removeMotor(std::string serialPort) {
	int index = getMotorIndex(serialPort);
	
	// if nanotec motor does not exist throw exception
	if (index == -1) { 
		cout << "Error motor using serialport " << serialPort << " not in nanotec motor container" << endl;
		throw;
	}
	
	// shift all elements left into the deleted entry
	for (int i = index; i < _numMotors; ++i) {
		_nanotecMotorArray[i] = _nanotecMotorArray[i + 1]; // copy next element left
	}
	_numMotors--; // decrement num of motors by 1
	return;
}



/**
 * Main function performs tests to test NanotecMotorContainer. Requires a nanotec motor to be connected.
 * 
 * 
 */
 
int main() 
{

	std::string serialPort1 = "/dev/ttyACM0";
	std::string serialPort2 = "/dev/ttyACM1";
    NanotecMotor* motorPointer1 = new NanotecMotor("/dev/ttyACM0",25);
    NanotecMotor* motorPointer2 = new NanotecMotor("/dev/ttyACM1",26);
    
    NanotecMotorContainer* motorContainerPointer = new NanotecMotorContainer();
    
    cout << "Before Insertion" << endl;
    cout << "contains(motor1): " << motorContainerPointer->contains(serialPort1) << endl;
    cout << "contains(motor2): " << motorContainerPointer->contains(serialPort2) << endl;
    cout << endl;
    
    
    motorContainerPointer->insert(motorPointer1);
    cout << "Insert motor1" << endl;
    cout << "contains(motor1): " << motorContainerPointer->contains(serialPort1) << endl;
    cout << "contains(motor2): " << motorContainerPointer->contains(serialPort2) << endl;
    cout << endl;
    
    motorContainerPointer->insert(motorPointer2);
    cout << "Insert motor2" << endl;
    cout << "contains(motor1): " << motorContainerPointer->contains(serialPort1) << endl;
    cout << "contains(motor2): " << motorContainerPointer->contains(serialPort2) << endl;
    cout << endl;
    
    cout << "Test getMotor" << endl;
    cout << "motor1 ID: " << motorContainerPointer->getMotor(serialPort1)->getID() << endl;
    cout << "motor2 ID: " << motorContainerPointer->getMotor(serialPort2)->getID() << endl;
    cout << endl;
    
    motorContainerPointer->removeMotor(serialPort1);
    cout << "Remove motor1" << endl;
    cout << "contains(motor1): " << motorContainerPointer->contains(serialPort1) << endl;
    cout << "contains(motor2): " << motorContainerPointer->contains(serialPort2) << endl;
    cout << endl;
    
    motorContainerPointer->removeMotor(serialPort2);
    cout << "Remove motor2" << endl;
    cout << "contains(motor1): " << motorContainerPointer->contains(serialPort1) << endl;
    cout << "contains(motor2): " << motorContainerPointer->contains(serialPort2) << endl;
    cout << endl;
    return 0; 
} 

