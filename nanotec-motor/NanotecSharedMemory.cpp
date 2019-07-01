/**
 * This cpp file is definitions of the shared memory interface for the NanotecSharedMemory.h
 * 
 * @author Benjamin Gutierrez (bengutie@mit.edu)
 * @date June 26, 2019
 * 
 */

#include "NanotecSharedMemory.h"





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



NanotecSharedMemory::NanotecSharedMemory()
{
	

	
	int dataKey = 65; // Beware of collisions, check terminal: "ipcs -m"
	_dataSharedMemory = new SharedMemory(dataKey);
	
	int statusKey = 88; // Beware of collisions, check terminal: "ipcs -m"
	_statusSharedMemory = new SharedMemory(statusKey);
	
	
	// Write empty empty sequence
    _dataSharedMemory->writeMemory("EMPTY_DATA");
    _statusSharedMemory->writeMemory("EMPTY_STATUS");
    
    cout << "Initial _dataSharedMemory: " << _dataSharedMemory->readMemory() << endl; 
    cout << "Initial _statusSharedMemory: " << _statusSharedMemory->readMemory() << endl;
	
}

NanotecSharedMemory::~NanotecSharedMemory()
{
	//delete shared memory  
    delete _dataSharedMemory;
    delete _statusSharedMemory;
}

/**
* Returns a copy of the string in the data shared memory location
*/
std::string NanotecSharedMemory::readData()
{
	return _dataSharedMemory->readMemory();
}

/**
* Returns a copy of the string in the status shared memory location
*/
std::string NanotecSharedMemory::readStatus()
{
	return _statusSharedMemory->readMemory();
}

/** Writes a string of characters to the data shared memory location
 * 
 * @param stringToWrite string to write to data shared memory location
 */
void NanotecSharedMemory::writeData(std::string stringToWrite)
{
	_dataSharedMemory->writeMemory(stringToWrite);
	return;
}

/** Writes a string of characters to the status shared memory location
 * 
 * @param stringToWrite string to write to status shared memory location
 */
void NanotecSharedMemory::writeStatus(std::string stringToWrite)
{
	_statusSharedMemory->writeMemory(stringToWrite);
	return;
}


/** Returns the number of delimiters in a char* sequence
 * 
 * @param delimiter delimiter to find
 * @param sequencePointer sequence to find delimiters, 
 * @param sequenceLength length of sequence to check for delimiters
 * 
 */
int NanotecSharedMemory::countDelimiters(const char delimiter, char * const sequencePointer, const int sequenceLength){
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
std::vector<std::string> NanotecSharedMemory::splitString(std::string stringToSplit, std::string delimiter)
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

bool NanotecSharedMemory::callFunctionUsingVector(std::vector<std::string> splittedStringVector){
	std::string funcName = splittedStringVector.at(0);
	int numArguments = splittedStringVector.size() - 1;
	cout << "numArguments: " << numArguments << endl; // TESTING
	
	// printDog function call
	if ( funcName.compare("printDog") == 0) {
		std::string dogNameString = splittedStringVector.at(1);
		char* dogName =  &dogNameString[0u];
		
		int dogAge = std::stoi( splittedStringVector.at(2) );
		
		printDog(dogName, dogAge);
		return true;
	}
	
	
	// printCat function call
	if (funcName.compare("printCat") == 0) {
		std::string catNameString = splittedStringVector.at(1);
		char* catName =  &catNameString[0u];
		
		if (numArguments == 1) {
			printCat(catName);
			return true;
		} 
		// numArguments = 2
		double catAge = std::stod( splittedStringVector.at(2) );
			
		printCat(catName,catAge);
		return true;
	}
	
	// NanotecMotor function call
	if (funcName.compare("NanotecMotor") == 0) {
		std::string serialPortString = splittedStringVector.at(1);
		char* serialPort = &serialPortString[0u];
		
		if (numArguments == 1) {
			NanotecMotor* motor = new NanotecMotor(serialPort);
			const char* motorCharPointer = reinterpret_cast<const char*>(&motor);
			std::string motorString( motorCharPointer);
			this->writeStatus(motorString);
			return true;
		}
		// numArguments == 2
		int ID = std::stoi( splittedStringVector.at(2) );
		NanotecMotor* motor = new NanotecMotor(serialPort,ID);
		const char* motorCharPointer = reinterpret_cast<const char*>(&motor);
		std::string motorString( motorCharPointer);
		this->writeStatus(motorString);
		return true;
		
	}
	return false;
}
	
/** Reads the shared memory location, and executes the instruction located there
 * 
 * @return true if there was a valid instruction in the shared memory location
 *              and the instruction was executed successfully, else return false/
 */
bool NanotecSharedMemory::executeMemory() {
	// Read the memory
	std::string memoryString = this->readData(); // data memory
	
	// Parse the memory by splitting into strings
	std::string delimiter = ",";
	std::string stringToSplit = memoryString;
	std::vector<std::string> splittedStringVector = NanotecSharedMemory::splitString(stringToSplit, delimiter);
	
	for (int i = 0; i != splittedStringVector.size(); i++)
	{
		cout << "  Split: " << splittedStringVector.at(i) << endl;
		
	}
	
	// executed the parsed instruction
	return NanotecSharedMemory::callFunctionUsingVector(splittedStringVector);
}


std::string printAndExecute(std::string stringToPrint,NanotecSharedMemory* memObjPointer) {
		
		memObjPointer->writeData(stringToPrint);
		
		cout << endl;
		std::string outputString = memObjPointer->executeMemory();
		cout << "dataRead: " << memObjPointer->readData() << endl;
		cout << "statusRead: " << memObjPointer->readStatus()  << endl;
		return outputString;
		
}

int main() 

{ 
    
    NanotecSharedMemory *memObjPointer = new NanotecSharedMemory();
    
		printAndExecute("hello",memObjPointer);
		sleep(2);
		
		printAndExecute("printCat,kit,4",memObjPointer);
		sleep(2);
		
		printAndExecute("NanotecMotor,/dev/ttyACM0,12",memObjPointer);
		sleep(2);

	
	delete memObjPointer;
  
    return 0; 
} 

