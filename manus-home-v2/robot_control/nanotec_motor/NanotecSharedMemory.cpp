/**
 * This cpp file is definitions of the shared memory interface for the NanotecSharedMemory.h
 * 
 * @author Benjamin Gutierrez (bengutie@mit.edu)
 * @date June 26, 2019
 * 
 */

#include "NanotecSharedMemory.h"



NanotecSharedMemory::NanotecSharedMemory()
{
	

	
	int dataKey = DATA_KEY; // Beware of collisions, check terminal: "ipcs -m"
	_dataSharedMemory = new SharedMemory(dataKey);
	
	int statusKey = STATUS_KEY; // Beware of collisions, check terminal: "ipcs -m"
	_statusSharedMemory = new SharedMemory(statusKey);
	
	
	// Write empty empty sequence
    _dataSharedMemory->writeMemory("EMPTY_DATA");
    _statusSharedMemory->writeMemory("EMPTY_STATUS");
    
    cout << "Initial _dataSharedMemory: " << _dataSharedMemory->readMemory() << endl; 
    cout << "Initial _statusSharedMemory: " << _statusSharedMemory->readMemory() << endl;
    
    _Parser = new NanotecParser();
	
}

NanotecSharedMemory::~NanotecSharedMemory()
{
	//delete shared memory  
    delete _dataSharedMemory;
    delete _statusSharedMemory;
    delete _Parser;
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



/**
 * Starts a "server" that waits for instructions to be sent in the shared memory locations.
 * Never terminates.
 * 
 * Waits for status memory to read "start".
 * Reads the data memory location, and executes the instruction located there
 * Writes result into the data memory location.
 * Writes "end" into the status memory
 * Repeats
 */
void NanotecSharedMemory::start() {
	std::string startMessage = "start";
	std::string endMessage = "end";
	
	// infinite loop to execute instruction over and over again.
	while(true) {
		/* Print out for debugging.
		cout << endl;
		cout << "_dataSharedMemory: " << _dataSharedMemory->readMemory() << endl; 
		cout << "_statusSharedMemory: " << _statusSharedMemory->readMemory() << endl;
		*/ 
		
		std::string statusString = _statusSharedMemory->readMemory(); // read status memory
		
		// if status string is equal to start message, execute instruction
		if (statusString.compare(startMessage) == 0) {
			std::string instruction = _dataSharedMemory->readMemory(); // read instruction in data register
			std::string result = _Parser->execute(instruction);
			_dataSharedMemory->writeMemory(result); // write result into data memory
			_statusSharedMemory->writeMemory(endMessage); // write end message into status register to let client 
			                                              // know we are done executing the instruction.
		}
	}
}


	


/*
std::string printAndExecute(std::string stringToPrint,NanotecSharedMemory* memObjPointer) {
		
		memObjPointer->writeData(stringToPrint);
		
		cout << endl;
		std::string outputString = memObjPointer->executeMemory();
		cout << "dataRead: " << memObjPointer->readData() << endl;
		cout << "statusRead: " << memObjPointer->readStatus()  << endl;
		return outputString;
		
}
*/

int main() 
{ 
	NanotecSharedMemory* memObjPointer = new NanotecSharedMemory();
	memObjPointer->start();
} 

