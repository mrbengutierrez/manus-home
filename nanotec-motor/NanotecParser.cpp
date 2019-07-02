/**
 * This cpp file is definitions of the parser interface for the NanotecParser.h
 * 
 * @author Benjamin Gutierrez (bengutie@mit.edu)
 * @date June 28, 2019
 * 
 */

#include "NanotecParser.h"

//-----------------------------------------------------------------------------------------------------

/** Converts a string to a double
 * 
 * @param stringToConvert string to convert into double
 */ 
double NanotecParser::stringToDouble(std::string stringToConvert) {
	return std::stod(stringToConvert);
}

/** Converts a string to an int
 * 
 * @param stringToConvert string to convert into int
 */ 
int NanotecParser::stringToInt(std::string stringToConvert) {
	return std::stoi(stringToConvert);
}

/** Converts a string to a char* 
 * Creates a new dynamic memory pointer that must be deleted when
 * done with using in order to prevent memory leaks
 * 
 * @param stringToConvert string to convert into char*
 */ 
char* NanotecParser::stringToCharPointer(std::string stringToConvert) {
	char* stringPointer = &stringToConvert[0u];
	char* stringPointerCopy = new char[stringToConvert.length()+1];
	strcpy(stringPointerCopy, stringPointer);
	return stringPointerCopy;
	
}
		
/** Converts a double to a string
 * 
 * @param doubleToConvert double to convert into string
 */ 	
std::string NanotecParser::doubleToString(double doubleToConvert) {
	const int maxBufferSize = 32;
	char charBuffer[maxBufferSize];
	snprintf(charBuffer, sizeof(charBuffer), "%g", doubleToConvert);
	std::string convertedString(charBuffer);
	return convertedString;
}

/** Converts a int to a string
 * 
 * @param intToConvert int to convert into string
 */
std::string NanotecParser::intToString(int intToConvert) {
	const char baseString[] = "";
	const int maxBufferSize = 32;
	char charBuffer [maxBufferSize];
	int number = 123;
	sprintf(charBuffer, "%s%d", baseString, intToConvert);
	std::string convertedString(charBuffer);
	return convertedString;
}

/** Converts a char* to a string
 * 
 * @param charPointerToConvert char* to convert into string
 */
std::string NanotecParser::charPointerToString(char* charPointerToConvert) {
	std::string convertedString( charPointerToConvert);
	return convertedString;
}

//-----------------------------------------------------------------------------------------------------


//-----------------------------------------------------------------------------------------------------
// Begin string manipulation functions
/** Returns the number of delimiters in a char* sequence
 * 
 * @param delimiter delimiter to find
 * @param sequencePointer sequence to find delimiters, 
 * @param sequenceLength length of sequence to check for delimiters
 * 
 */
int NanotecParser::countDelimiters(const char delimiter, char * const sequencePointer, const int sequenceLength){
	char* currentCharPointer = sequencePointer; // keep track of the current character
	
	int numDelimiters = 0; // initialize number of delimiters to zero
	for(int i=0; i < sequenceLength; i++){ // for each character in sequence
		if ( *currentCharPointer == delimiter) {
			numDelimiters++;  // increment numDelimiters if character is a delimiters
		}
		currentCharPointer++; // increment current character pointer
	}
	return numDelimiters;
}


/** Splits a string based on delimiters and stores splitted elements is a vector
 * Does not modify input string.
 * 
 * @param stringToSplit Pointer to a sequence of characters terminated with '\0'
 * @param delimiter to use to split string
 */
std::vector<std::string> NanotecParser::splitString(std::string stringToSplit, std::string delimiter)
{
	// initialize return vector for splitted strings
	std::vector<std::string> splittedStringVector;
	
	int curr = 0; 
	int next = stringToSplit.find(delimiter,curr); 
	// string::npos is a constant (probably -1) representing a non-position.
	// It is returned by find when a pattern is not found.
	while (next != string::npos) 
	{ 
		std::string currentString = stringToSplit.substr(curr, next-curr); // Get substring
		splittedStringVector.emplace_back( currentString); // Add substring
		curr = next + delimiter.length();
		next = stringToSplit.find(delimiter, curr); 
	}
	
	// Add last substring
	splittedStringVector.emplace_back( stringToSplit.substr(curr,next) );
	
	return splittedStringVector;	
}

// Begin type conversion functions
/** Joins of a vector of strings using a deliminator.
 * 
 * @param stringVector vector strings to be joined
 * @param deliminator deliminator to be placed inbetween strings
 */
std::string NanotecParser::stringJoiner( std::vector<std::string> stringVector, std::string deliminator ) {
	std::string outputString = ""; // initialize empty output string 
	for( int i = 0; i != stringVector.size(); i++ ) {
		if (i > 0) { outputString = outputString + deliminator; }
		outputString = outputString + stringVector.at( i );
	}
	return outputString;
}

// End string manipulation functions
//-----------------------------------------------------------------------------------------------------



//-----------------------------------------------------------------------------------------------------
// Begin nanotec motor calling functions

/** Calls NanotecMotor.NanotecMotor using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.NanotecMotor
 */
std::string NanotecParser::nanotecMotor(std::vector<std::string> argumentVector) {

	// initialize variables for _motorMap
	std::string serialPortString = argumentVector.at(1);
	
	if ( _motorContainerPointer->contains(serialPortString) == true ) {
		cout << "NanotecParser Error: Motor using serial port " << serialPortString << " already exists " << endl;
		throw;
	}

	char* serialPort = NanotecParser::stringToCharPointer( argumentVector.at(1) );
	int ID = NanotecParser::stringToInt( argumentVector.at(2) );
	NanotecMotor* motorPointer = new NanotecMotor(serialPort,ID);  // will throw exception if motor already exists
	_motorContainerPointer->insert(motorPointer);
	delete serialPort; // free char* memory
	
	return serialPortString;
}

/** Calls NanotecMotor.getID using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.getID
 */
std::string NanotecParser::getID(std::vector<std::string> argumentVector) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);

	int ID = motorPointer->getID();
	return NanotecParser::intToString( ID );
}

/** Calls NanotecMotor.getSerialPort using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.getSerialPort
 */
std::string NanotecParser::getSerialPort(std::vector<std::string> argumentVector) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);

	char* serialPortCharPointer = motorPointer->getSerialPort();
	std::string serialPortString = NanotecParser::charPointerToString( serialPortCharPointer );
	delete serialPortCharPointer;
	return serialPortString;
}

/** Calls NanotecMotor.torqueMode using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.torqueMode
 */		
std::string NanotecParser::torqueMode( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	
	int torque = stringToInt( argumentVector.at(2));
	int maxTorque = stringToInt(argumentVector.at(3));
	int maxCurr = stringToInt(argumentVector.at(4));
	int nomCurr = stringToInt(argumentVector.at(5));
	int slope = stringToInt(argumentVector.at(6));
	
	motorPointer->torqueMode(torque,maxTorque,maxCurr,nomCurr,slope);
	return "";
}

/** Calls NanotecMotor.angularVelocityMode using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.angularVelocityMode
 */		
std::string NanotecParser::angularVelocityMode( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	int angVel = stringToInt( argumentVector.at(2));
	motorPointer->angularVelocityMode(angVel);
	return "";
}

/** Calls NanotecMotor.angularPositionMode using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.angularPositionMode
 */	
std::string NanotecParser::angularPositionMode( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	int angPos = stringToDouble( argumentVector.at(2));
	int angVel = stringToInt( argumentVector.at(3));
	motorPointer->angularPositionMode(angPos, angVel);
	return "";
}


/** Calls NanotecMotor.setTorque using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.setTorque
 */			
std::string NanotecParser::setTorque( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	int torque = stringToInt( argumentVector.at(2));
	motorPointer->setTorque(torque);
	return "";
}

/** Calls NanotecMotor.setAngularVelocity using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.setAngularVelocity
 */	
std::string NanotecParser::setAngularVelocity( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	int angVel = stringToInt( argumentVector.at(2));
	motorPointer->setAngularVelocity(angVel);
	return "";
}

/** Calls NanotecMotor.setRelativeAngularPosition using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.setRelativeAngularPosition
 */	
std::string NanotecParser::setRelativeAngularPosition( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	int angPos = stringToDouble( argumentVector.at(2) );
	int angVel = stringToInt( argumentVector.at(3));
	motorPointer->setRelativeAngularPosition(angPos, angVel);
	return "";
}

/** Calls NanotecMotor.setAbsoluteAngularPosition using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.setAbsoluteAngularPosition
 */	
std::string NanotecParser::setAbsoluteAngularPosition( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	int angPos = stringToDouble( argumentVector.at(2) );
	int angVel = stringToInt( argumentVector.at(3));
	motorPointer->setAbsoluteAngularPosition(angPos, angVel);
	return "";
}

/** Calls NanotecMotor.etAbsoluteAngularPositionShortestPath using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.etAbsoluteAngularPositionShortestPath
 */	
std::string NanotecParser::setAbsoluteAngularPositionShortestPath( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	int angPos = stringToDouble( argumentVector.at(2) );
	int angVel = stringToInt( argumentVector.at(3));
	motorPointer->setAbsoluteAngularPositionShortestPath(angPos, angVel);
	return "";
}

/** Calls NanotecMotor.stop using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.stop
 */	
std::string NanotecParser::stop( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	motorPointer->stop();
	return "";
}

/** Calls NanotecMotor.getTorque using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.getTorque
 */			
std::string NanotecParser::getTorque( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	int torque = motorPointer->getTorque();
	return intToString(torque);
}

/** Calls NanotecMotor.getAngularVelocity using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.getAngularVelocity
 */			
std::string NanotecParser::getAngularVelocity( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	int angVel = motorPointer->getAngularVelocity();
	return intToString(angVel);
}

/** Calls NanotecMotor.getAbsoluteAngularPosition using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.getAbsoluteAngularPosition
 */	
std::string NanotecParser::getAbsoluteAngularPosition( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	double angPos = motorPointer->getAbsoluteAngularPosition();
	return doubleToString(angPos);
}

/** Calls NanotecMotor.readPhysicalEncoder using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.readPhysicalEncoder
 */			
std::string NanotecParser::readPhysicalEncoder( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	int encoderValue = motorPointer->readPhysicalEncoder();
	return intToString(encoderValue);
}

/** Calls NanotecMotor.closePort using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 * If "function_name represents an instance of a nanotec motor, 
 * "arg1" must be the serial port of that motor
 * 
 * @return string representation of return value from NanotecMotor.closePort
 */			
std::string NanotecParser::closePort( std::vector<std::string> argumentVector ) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorContainerPointer->getMotor(serialPort);
	
	motorPointer->closePort();
	return "";
}



// End nanotec motor calling functions
//-----------------------------------------------------------------------------------------------------



	
/** Executes a string using the NanotecMotor.h interface
 * 
 * @param stringToExecute string representation of the instruction to be execute
 * 			format: function_name, arg1, arg2, ...
 * 			The first argument (arg1) will be an object pointer if calling a function that is an instance of a class.
 * 
 * @return string representation of return value if there was a valid instruction in shared
 *              and the instruction was executed successfully
 */
std::string NanotecParser::execute(std::string stringToExecute) {
	// Parse the string by splitting into strings
	std::string delimiter = ",";
	std::vector<std::string> splittedStringVector = NanotecParser::splitString(stringToExecute, delimiter);
	
	// get function name
	std::string funcName = splittedStringVector.at(0); // first element is function name
	
	

	int numArguments = splittedStringVector.size() -1;		
	
	// check if funcName is one a valid function defined in the function map
	if (_functionMap.count(funcName) == 1) {
		// call the function.
		functionPointerType functionPointer = _functionMap.at(funcName); // get function pointer
		return (this->*functionPointer)(splittedStringVector); // call function using function pointer
	}
	
	// if lookup map is too slow, can you a series of if statements to call functions
	/*
	int isEqual = 0;
	if (funcName.compare("NanotecMotor") == isEqual) {
		return NanotecParser::nanotecMotor(splittedStringVector);
	}
	
	if (funcName.compare("getID") == isEqual) {
		return NanotecParser::getID(splittedStringVector);
	}
	*/
	std::string parserError = "NANOTEC PARSER ERROR";
	return parserError;
}





/**
 * Default Constructor
 * 
 * 
 */
NanotecParser::NanotecParser() {
	
	// initialize motor container
	_motorContainerPointer = new NanotecMotorContainer();

	
	// Initialize function map with all fo the NanotecParser functions
	// that are used to call the NanotecMotor.h functions
	
	_functionMap["NanotecMotor"] = &NanotecParser::nanotecMotor;
	_functionMap["getID"] = &NanotecParser::getID;
	_functionMap["getSerialPort"] = &NanotecParser::getSerialPort;
	
	_functionMap["torqueMode"] = &NanotecParser::torqueMode;
	_functionMap["angularVelocityMode"] = &NanotecParser::angularVelocityMode;
	_functionMap["angularPositionMode"] = &NanotecParser::angularPositionMode;
	
	_functionMap["setTorque"] = &NanotecParser::setTorque;
	_functionMap["setAngularVelocity"] = &NanotecParser::setAngularVelocity;
	_functionMap["setRelativeAngularPosition"] = &NanotecParser::setRelativeAngularPosition;
	_functionMap["setAbsoluteAngularPosition"] = &NanotecParser::setAbsoluteAngularPosition;
	_functionMap["setAbsoluteAngularPositionShortestPath"] = &NanotecParser::setAbsoluteAngularPositionShortestPath;
	_functionMap["stop"] = &NanotecParser::stop;
	
	_functionMap["getTorque"] = &NanotecParser::getTorque;
	_functionMap["getAngularVelocity"] = &NanotecParser::getAngularVelocity;
	_functionMap["getAbsoluteAngularPosition"] = &NanotecParser::getAbsoluteAngularPosition;
	_functionMap["readPhysicalEncoder"] = &NanotecParser::readPhysicalEncoder;
	
	_functionMap["closePort"] = &NanotecParser::closePort;
	
	
}














// Uncomment to test the NanotecParser
/*
// For testing Parser
void printMotorInformation(NanotecParser* Parser, std::string serialPort) {
	
	std::string instruction;
	
	cout << endl;
	instruction = "getSerialPort," + serialPort;
	cout << "serialPort: " << Parser->execute(instruction) << endl;
	
	instruction = "getID," + serialPort;
	cout << "Motor ID: " << Parser->execute(instruction) << endl;
	
	instruction = "readPhysicalEncoder," + serialPort;
	cout << "encoder value: " << Parser->execute(instruction) << endl;
	
	instruction = "getAbsoluteAngularPosition," + serialPort;
	cout << "anglular position: " << Parser->execute(instruction) << endl;
	
	instruction = "getAngularVelocity," + serialPort;
	cout << "angular velocity: " << Parser->execute(instruction) << endl;
	
	instruction = "getTorque," + serialPort;
	cout << "torque: " << Parser->execute(instruction) << endl;
	
	cout << endl;
	return;
}

// For testing Parser
void printMotorsInformation(NanotecParser* Parser, std::vector<std::string> serialPortVector) {
	sleep(1);
	
	for (int i = 0; i != serialPortVector.size(); i++) {
		std::string serialPort = serialPortVector.at(i);
		printMotorInformation(Parser,serialPort);
	}
	return;
}


/**
 * Main function performs tests to test parser. Requires a nanotec motor to be connected.
 * 
 * 
 */
int main() 
{
    std::string instruction;
    std::vector<std::string> stringVector;
    std::string delimiter = ",";
    
    NanotecParser* Parser = new NanotecParser();
	
	
	// initialize motors
	instruction	= "NanotecMotor,/dev/ttyACM0,12";
	std::string serialPort1 = Parser->execute(instruction);
	instruction	= "NanotecMotor,/dev/ttyACM1,13";
	std::string serialPort2 = Parser->execute(instruction);
	std::vector<std::string> serialPortVector;
	serialPortVector.push_back(serialPort1);
	serialPortVector.push_back(serialPort2);
	
	// check ID
	stringVector.clear();
	stringVector.push_back("getID");
	stringVector.push_back(serialPort1);
	instruction = NanotecParser::stringJoiner( stringVector, delimiter );
	std::string ID1 = Parser->execute(instruction);
	cout << "getID1 (actual): " << ID1 << ", expected1: " << 12 << endl;
	
	instruction = "getID," + serialPort2;
	std::string ID2 = Parser->execute(instruction);
	cout << "getID2 (actual): " << ID2 << ", expected2: " << 13 << endl;
	
  
  
	int sleepTime = 5;
  
	// Read initial configuration
	cout << "Initial Configuration" << endl;
	printMotorsInformation(Parser,serialPortVector);
	
	
	// Test angular position methods
	cout << "setAngularPosition" << endl;
	
	instruction = "angularPositionMode," + serialPort1 + ",0.0" + ",200";
	Parser->execute(instruction);
	instruction = "angularPositionMode," + serialPort2 + ",0.0" + ",200";
	Parser->execute(instruction);
	printMotorsInformation(Parser,serialPortVector);
	sleep(sleepTime);
	
	instruction = "setAbsoluteAngularPosition," + serialPort1 + ",-180.0" + ",200";
	Parser->execute(instruction);
	instruction = "setAbsoluteAngularPosition," + serialPort2 + ",-180.0" + ",200";
	Parser->execute(instruction);
	printMotorsInformation(Parser,serialPortVector);
	sleep(sleepTime);
	
	instruction = "setRelativeAngularPosition," + serialPort1 + ",90.0" + ",200";
	Parser->execute(instruction);
	instruction = "setRelativeAngularPosition," + serialPort2 + ",90.0" + ",200";
	Parser->execute(instruction);
	printMotorsInformation(Parser,serialPortVector);
	sleep(sleepTime);
	
	instruction = "setAbsoluteAngularPositionShortestPath," + serialPort1 + ",0" + ",200";
	Parser->execute(instruction);
	instruction = "setAbsoluteAngularPositionShortestPath," + serialPort2 + ",-0" + ",200";
	Parser->execute(instruction);
	printMotorsInformation(Parser,serialPortVector);
	sleep(sleepTime);
	
	
	// Test angular velocity methods
	cout << "setAngularVelocity" << endl;	
	
	instruction = "angularVelocityMode," + serialPort1 + ",0";
	Parser->execute(instruction);
	instruction = "angularVelocityMode," + serialPort2 + ",0";
	Parser->execute(instruction);
	printMotorsInformation(Parser,serialPortVector);
	sleep(sleepTime);
	
	instruction = "setAngularVelocity," + serialPort1 + ",150";
	Parser->execute(instruction);
	instruction = "setAngularVelocity," + serialPort2 + ",150";
	Parser->execute(instruction);
	printMotorsInformation(Parser,serialPortVector);
	sleep(sleepTime);
	
	instruction = "setAngularVelocity," + serialPort1 + ",-50";
	Parser->execute(instruction);
	instruction = "setAngularVelocity," + serialPort2 + ",-50";
	Parser->execute(instruction);
	printMotorsInformation(Parser,serialPortVector);
	sleep(sleepTime);
	
	// Test torque methods
	cout << "setTorque" << endl;
	
	instruction = "torqueMode," + serialPort1 + ",0,1000,1800,1800,1000";
	Parser->execute(instruction);
	instruction = "torqueMode," + serialPort2 + ",0,1000,1800,1800,1000";
	Parser->execute(instruction);
	printMotorsInformation(Parser,serialPortVector);
	sleep(sleepTime);
	
	instruction = "setTorque," + serialPort1 + ",100";
	Parser->execute(instruction);
	instruction = "setTorque," + serialPort2 + ",100";
	Parser->execute(instruction);
	printMotorsInformation(Parser,serialPortVector);
	sleep(sleepTime);
	
	instruction = "setTorque," + serialPort1 + ",-50";
	Parser->execute(instruction);
	instruction = "setTorque," + serialPort2 + ",-50";
	Parser->execute(instruction);
	printMotorsInformation(Parser,serialPortVector);
	sleep(sleepTime);
	

	
	
	// stop motors and close ports
	instruction = "stop," + serialPort1;
	Parser->execute(instruction);
	instruction = "stop," + serialPort2;
	Parser->execute(instruction);
	
	instruction = "closePort," + serialPort1;
	Parser->execute(instruction);
	instruction = "closePort," + serialPort2;
	Parser->execute(instruction);
  
    return 0; 
} 
*/






