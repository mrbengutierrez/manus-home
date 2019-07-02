		
/**
 * This cpp file is responsible for managing multiple NanotecMotor.h objects
 * 
 * @author Benjamin Gutierrez (bengutie@mit.edu)
 * @date July 2, 2019
 * 
 */


#include "NanotecMotorContainer.h"		
		
/** Inserts a nanotec motor into a nanotec motor container
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 * 		  serialPort 
 * @param motor NanotecMotor object that is used by the Nanotec motor
 */
void NanotecMotorContainer::insert(std::string serialPort, NanotecMotor motor) {
	pair<std::string,NanotecMotor> keyValuePair(serialPort,motor);
	_motorMap.insert(keyValuePair);
	return;
}

/** Returns true if the container contains a motor with the serialPort specified, else returns false
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 */		
bool NanotecMotorContainer::contains(std::string serialPort) {
	if (_motorMap.count(serialPort) == 1) { 
		return true;
	}
	return false;	
}

/** Returns the NanotecMotor using the serialport
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 *        serialPort must be in the NanotecMotorContainer
 */		
NanotecMotor NanotecMotorContainer::getMotor(std::string serialPort) {
	return _motorMap.at(serialPort);
}


/** Removes the NanotecMotor using the serialport
 * 
 * @param serialPort name of the serialport that the nanotec motor is using
 *        serialPort must be in the NanotecMotorContainer
 */		
void NanotecMotorContainer::removeMotor(std::string serialPort) {
	_motorMap.erase(serialPort);
	return;
}
