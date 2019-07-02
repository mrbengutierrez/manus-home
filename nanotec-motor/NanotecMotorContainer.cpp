		
/**
 * This cpp file is responsible for managing multiple NanotecMotor.h objects
 * 
 * @author Benjamin Gutierrez (bengutie@mit.edu)
 * @date July 2, 2019
 * 
 */


#include "NanotecMotorContainer.h"		

NanotecMotorContainer::NanotecMotorContainer() {
	int maxNumElements = 100;
	_serialPortVector.reserve(maxNumElements);
	_nanotecMotorVector.reserve(maxNumElements);
}
		
/** Inserts a nanotec motor into a nanotec motor container
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 * 		  serialPort 
 * @param motor NanotecMotor object that is used by the Nanotec motor
 */
void NanotecMotorContainer::insert(std::string serialPort, NanotecMotor* motor) {
	_serialPortVector.push_back(serialPort);
	_nanotecMotorVector.push_back(*motor);
	return;
}

/** Returns true if the container contains a motor with the serialPort specified, else returns false
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 */		
bool NanotecMotorContainer::contains(std::string serialPort) {
	for(int i = 0; i != _serialPortVector.size(); i++) {
		if ( _serialPortVector.at(i).compare(serialPort) == 0 ) {
			true;
		}
	}
	return false;
}


/** Returns the NanotecMotor using the serialport
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 *        serialPort must be in the NanotecMotorContainer
 */		
NanotecMotor* NanotecMotorContainer::getMotor(std::string serialPort) {
	cout << "Inside Container" << endl;  // TESTING
	for(int i = 0; i != _serialPortVector.size(); i++) {
		if ( _serialPortVector.at(i).compare(serialPort) == 0 ) {
			cout << "Motor found" << endl;  // TESTING
			_nanotecMotorVector.at(i);
			cout << "_nanotecMotorVector.at(i)"  << endl;  // TESTING
			//cout << "_nanotecMotorVector.at(i): " << _nanotecMotorVector.at(i) << endl; // TESTING
			//cout << "_nanotecMotorVector.at(i)->getID(): " << _nanotecMotorVector.at(i)->getID() << endl;
			NanotecMotor* motorPointer =  &_nanotecMotorVector.at(i);
			cout << "motorPointer variable assigned" << endl;  // TESTING
			return motorPointer;
		}
	}
	cout << "Error motor using serialport " << serialPort << " not in nanotec motor container" << endl;
	throw;
}


/** Removes the NanotecMotor using the serialport
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 *        serialPort must be in the NanotecMotorContainer
 */		
void NanotecMotorContainer::removeMotor(std::string serialPort) {
	for(int i = 0; i != _serialPortVector.size(); i++) {
		if ( _serialPortVector.at(i).compare(serialPort) == 0 ) {
			_serialPortVector.erase(_serialPortVector.begin() + i);
			_nanotecMotorVector.erase(_nanotecMotorVector.begin() + i);
			return;
		}
	}
	cout << "Error motor using serialport " << serialPort << " not in nanotec motor container" << endl;
	throw;
}
