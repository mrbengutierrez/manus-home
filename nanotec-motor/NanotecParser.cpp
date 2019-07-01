/**
 * This cpp file is definitions of the parser interface for the NanotecParser.h
 * 
 * @author Benjamin Gutierrez (bengutie@mit.edu)
 * @date June 28, 2019
 * 
 */

#include "NanotecParser.h"

//-----------------------------------------------------------------------------------------------------
// Being TESTING functions

// TESTING TESTING TESTING
void printDog(char* dogName, int dogAge)
{
	cout << "printDog, name: " << dogName << ", age: " << dogAge << endl;
}
// TESTING TESTING TESTING
void printCat(char* catName, double catAge = 12.5)
{
	cout << "printCat, name: " << catName << ", age: " << catAge << endl;
}

// End TESTING functions
//-----------------------------------------------------------------------------------------------------


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

/** Converts a string to a void*
 * 
 * @param stringToConvert string to convert into void*
 */ 
void* NanotecParser::stringToVoidPointer(std::string stringToConvert) {	
	
	// convert address to base 16
    int hexAddress = stoi(stringToConvert, 0, 16);
    // make a new pointer 
    void * voidPointer = (void *) hexAddress;
    
    return voidPointer;
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

/** Converts a void* to a string
 * 
 * @param voidPointerToConvert void* to convert into string
 */
std::string NanotecParser::voidPointerToString(void* voidPointerToConvert) {
    ostringstream addressStringStream;
    addressStringStream << voidPointerToConvert;
    std::string addressString =  addressStringStream.str(); 
    
    /*
    const void * address = static_cast<const void*>(this);
	std::stringstream ss;
	ss << address;  
	std::string name = ss.str(); 
	*/
    return addressString;
}
// End type conversion functions
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

/** Calls NanotecMotor using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 */
std::string NanotecParser::nanotecMotor(std::vector<std::string> argumentVector) {

	// initialize variables for _motorMap
	std::string serialPortString = argumentVector.at(1);

	
	// make sure motor is not already in use
	if ( _motorMap->count(serialPortString) == 1 ) { // BUG HERE
		cout << "here001" << endl;  // TESTING
		cout << "Error: Motor using serial port " << serialPortString << " already exists." << endl;
		throw;
	}
	
	
	cout << "here1" << endl;  // TESTING
	char* serialPort = NanotecParser::stringToCharPointer( argumentVector.at(1) );
	
	cout << "here2" << endl;  // TESTING
	int numArguments = argumentVector.size() - 1;
	if (numArguments == 1) {
		NanotecMotor* motor = new NanotecMotor(serialPort);
		(*_motorMap)[serialPortString] = motor; // and motor to motor map
		delete serialPort; // free char* memory
		
	} else { // numArguments == 2
		int ID = NanotecParser::stringToInt( argumentVector.at(2) );
		cout << "here4" << endl;  // TESTING
		NanotecMotor* motor = new NanotecMotor(serialPort,ID);
		cout << "here5" << endl;  // TESTING
		pair<std::string,NanotecMotor*> keyValuePair(serialPortString,motor);
		cout << "serialPortString: " << serialPortString << endl;
		cout << "motorID: " << motor->getID() << endl;
		_motorMap->insert(keyValuePair);
		//(*_motorMap)[serialPortString] = motor; // and motor to motor map
		cout << "here6" << endl;  // TESTING
		delete serialPort; // free char* memory
	}
	cout << "here7" << endl;  // TESTING
	return serialPortString;
}

/** Calls getID using parsed instruction vector
 * 
 * @param argumentVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...> 
 */
std::string NanotecParser::getID(std::vector<std::string> argumentVector) {
	std::string serialPort = argumentVector.at(1);
	NanotecMotor* motorPointer = _motorMap->at(serialPort);
		
	cout << "here2" << endl;  // TESTING
	int ID = motorPointer->getID();
	cout << "ID: " << ID << endl;  // TESTING
	return NanotecParser::intToString( ID );
}
		
std::string NanotecParser::torqueMode( std::vector<std::string> argumentVector ) {
}

std::string NanotecParser::angularVelocityMode( std::vector<std::string> argumentVector ) {
}

std::string NanotecParser::angularPositionMode( std::vector<std::string> argumentVector ) {
}

		
std::string NanotecParser::setTorque( std::vector<std::string> argumentVector ) {
}

std::string NanotecParser::setAngularVelocity( std::vector<std::string> argumentVector ) {
}

std::string NanotecParser::setRelativeAngularPosition( std::vector<std::string> argumentVector ) {
}

std::string NanotecParser::setAbsoluteAngularPosition( std::vector<std::string> argumentVector ) {
}

std::string NanotecParser::setAbsoluteAngularPositionShortestPath( std::vector<std::string> argumentVector ) {
}

std::string NanotecParser::stop( std::vector<std::string> argumentVector ) {
}

		
std::string NanotecParser::getTorque( std::vector<std::string> argumentVector ) {
}

std::string NanotecParser::getAngularVelocity( std::vector<std::string> argumentVector ) {
}

std::string NanotecParser::getAbsoluteAngularPosition( std::vector<std::string> argumentVector ) {
}

std::string NanotecParser::readPhysicalEncoder( std::vector<std::string> argumentVector ) {
}
		
std::string NanotecParser::closePort( std::vector<std::string> argumentVector ) {
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
	
	// TESTING
	cout << endl;
	int numArguments = splittedStringVector.size() -1;
	cout << "numArguments: " << numArguments << endl; // TESTING
	
	// TESTING
	for (int i = 0; i != splittedStringVector.size(); i++)
	{
		cout << "  Split: " << splittedStringVector.at(i) << endl;	
	}
	
	
	
	// printDog function call
	if ( funcName.compare("printDog") == 0) 
	{
		std::string stringToConvert( splittedStringVector.at(1) );
		char* dogName =  NanotecParser::stringToCharPointer( stringToConvert );
		
		cout << "dogName: " << dogName << endl; // TESTING
		for (int i = 0; i != splittedStringVector.size(); i++) { cout << "    Split: " << splittedStringVector.at(i) << endl;} // TESTING
		
		std::string stringToConvert2( splittedStringVector.at(2) );
		int dogAge = NanotecParser::stringToInt( stringToConvert2 );
		
		cout << "dogName: " << dogName << endl; // TESTING
		for (int i = 0; i != splittedStringVector.size(); i++) { cout << "    Split: " << splittedStringVector.at(i) << endl;} // TESTING
		printDog(dogName, dogAge);
		
		delete dogName;
		return "";
	}
	
	// printCat function call
	if (funcName.compare("printCat") == 0) 
	{
		char* catName =  NanotecParser::stringToCharPointer( splittedStringVector.at(1) );
		cout << "catName: "<< catName << endl;
		
		if (numArguments == 1) {
			printCat(catName);
			return "";
		} 
		// numArguments = 2
		double catAge = NanotecParser::stringToDouble( splittedStringVector.at(2) );
			
		cout << "catName: "<< catName << endl;
		printCat(catName,catAge);
		return "";
	}
	
	/*
	// check if funcName is one a valid function defined in the function map
	if (_functionMap.count(funcName) == 1) {
		void* functionPointer = _functionMap[funcName]; // get function pointer
		return (*functionPointer)(splittedStringVector); // call function using function pointer
	}
	*/
	int isEqual = 0;
	if (funcName.compare("NanotecMotor") == isEqual) {
		return NanotecParser::nanotecMotor(splittedStringVector);
	}
	
	if (funcName.compare("getID") == isEqual) {
		return NanotecParser::getID(splittedStringVector);
	}
	
	

	std::string parserError = "NANOTEC PARSER ERROR";
	return parserError;
}





/**
 * Default Constructor
 * 
 * 
 */
NanotecParser::NanotecParser() {
	
	// initialize the motor map
	_motorMap = new map<std::string,NanotecMotor*>();
	
	// Initialize function map with all fo the NanotecParser functions
	// that are used to call the NanotecMotor.h functions
	_functionMap["nanotecMotor"] = &NanotecParser::nanotecMotor;
	_functionMap["getID"] = &NanotecParser::getID;


	
	
	
	/*
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
	_functionMap["getAngularPosition"] = &NanotecParser::getAbsoluteAngularPosition;
	_functionMap["readEncoder"] = &NanotecParser::readPhysicalEncoder;
	
	_functionMap["closePort"] = &NanotecParser::closePort;
	*/
	
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
    
    NanotecParser* Parser;
    
    Parser->execute("printDog,pup,4");
	sleep(1);
		
	Parser->execute("printCat,kit,3.5");
	sleep(1);
	
	instruction	= "NanotecMotor,/dev/ttyACM0,12";
	std::string motor1 = Parser->execute(instruction);
	sleep(1);
		
	stringVector.clear();
	stringVector.push_back("getID");
	stringVector.push_back(motor1);
	instruction = NanotecParser::stringJoiner( stringVector, delimiter );
	std::string ID = Parser->execute(instruction);
	cout << "getID: " << ID << endl;
	
  
    return 0; 
} 























/** Uses a parsed vector of strings to call a function in NanotecMotor.h
 * 
 * @param splittedStringVector vector of strings that contains all the information for a 
 * function call to NanotecMotor.h
 * Format: <"function_name","arg1","arg2",...>
 *        
 * @return string representation of return value from NanotecMotor.h
 */
 
 /*
std::string NanotecParser::callFunctionUsingVector(std::vector<std::string> splittedStringVector){
	
	std::string funcName = splittedStringVector.at(0); // first element is function name
	
	cout << endl;
	int numArguments = splittedStringVector.size() -1;
	cout << "numArguments: " << numArguments << endl; // TESTING
	
	// TESTING
	for (int i = 0; i != splittedStringVector.size(); i++)
	{
		cout << "  Split: " << splittedStringVector.at(i) << endl;	
	}
	
	
	
	// printDog function call
	if ( funcName.compare("printDog") == 0) 
	{
		std::string stringToConvert( splittedStringVector.at(1) );
		char* dogName =  NanotecParser::stringToCharPointer( stringToConvert );
		
		cout << "dogName: " << dogName << endl; // TESTING
		for (int i = 0; i != splittedStringVector.size(); i++) { cout << "    Split: " << splittedStringVector.at(i) << endl;} // TESTING
		
		std::string stringToConvert2( splittedStringVector.at(2) );
		int dogAge = NanotecParser::stringToInt( stringToConvert2 );
		
		cout << "dogName: " << dogName << endl; // TESTING
		for (int i = 0; i != splittedStringVector.size(); i++) { cout << "    Split: " << splittedStringVector.at(i) << endl;} // TESTING
		printDog(dogName, dogAge);
		
		delete dogName;
		return "";
	}
	
	// printCat function call
	if (funcName.compare("printCat") == 0) 
	{
		char* catName =  NanotecParser::stringToCharPointer( splittedStringVector.at(1) );
		cout << "catName: "<< catName << endl;
		
		if (numArguments == 1) {
			printCat(catName);
			return "";
		} 
		// numArguments = 2
		double catAge = NanotecParser::stringToDouble( splittedStringVector.at(2) );
			
		cout << "catName: "<< catName << endl;
		printCat(catName,catAge);
		return "";
	}
	
	// check if funcName is one a valid function defined in the function map
	if (_functionMap.count(funcName) == 1) {
		void* functionPointer = _functionMap[funcName]; // get function pointer
		return (*functionPointer)(splittedStringVector); // call function using function pointer
	}

	std::string parserError = "NANOTEC PARSER ERROR";
	return parserError;
}
*/




