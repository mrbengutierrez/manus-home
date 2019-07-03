


import sysv_ipc # shared memory module
import time


class NanotecSharedMemoryClient:
	
	def __init__(self):
		"""Initializes the status and data memory"""
		self.dataMemory = sysv_ipc.SharedMemory(65)
		self.statusMemory = sysv_ipc.SharedMemory(88)
		return
	
	@staticmethod
	def readMemory(memory): # static method
		"""Reads a shared memory location
		
		Parameters:
		memory (sysv_ipc.SharedMemory): shared memory object
		
		Returns:
		(string): string representation of the data in the shared memory location
		"""
		# Read value from shared memory
		memoryValue = memory.read()
		# Find the 'end' of the string and strip
		i = memoryValue.find(ord('\0'))
		if i != -1:
			memoryValue = memoryValue[:i]
		else:
			errorMessage = "i: " + str(i) + " should be -1 to have read \0 in memory location"
			raise ValueError(errorMessage)
		return str(memoryValue.decode('ascii'))
	
	@staticmethod
	def writeMemory(memory,message): # static method
		"""Writes to a shared memory location
		
		Parameters:
		memory (sysv_ipc.SharedMemory): shared memory object
		message (string): message to write to shared memory
		
		Returns:
		None
		"""
		message += chr(0)
		bytesMessage = message.encode('ascii')
		memory.write(bytesMessage)
		return
		
	def sendInstruction(self,instruction):
		"""Sends an instruction using shared memory
		
			Parameters:
			instruction (string): instruction to be sent
									Format: "function_name,arg1,arg2,..." 
  									If "function_name" represents an instance of a nanotec motor, 
									"arg1" must be the serial port of that motor
			
			Return:
			(string): string representation of return value from the corresponding function in NanotecMotor
		"""
		startMessage = "start"
		endMessage = "end"
		
		NanotecSharedMemoryClient.writeMemory(self.dataMemory,instruction)
		NanotecSharedMemoryClient.writeMemory(self.statusMemory,startMessage)
		
		# wait for instruction to be executed
		currentStatus = NanotecSharedMemoryClient.readMemory(self.statusMemory)
		while ( currentStatus != endMessage):
			currentStatus = NanotecSharedMemoryClient.readMemory(self.statusMemory)
			#time.sleep(1)
			#print("currentStatus: " + currentStatus)
			#print("currentData: " + NanotecSharedMemoryClient.readMemory(self.dataMemory))
			#print("")
			
			 
		
		returnString = NanotecSharedMemoryClient.readMemory(self.dataMemory)
		return returnString
		
		
	
		











def testNanotecSharedMemory():
	"""Method to test NanotecSharedMemory.h"""
	
	memoryClient = NanotecSharedMemoryClient()
	
	
	
	serialPort1 = memoryClient.sendInstruction("NanotecMotor,/dev/ttyACM0,17")
	
	ID1 = memoryClient.sendInstruction("getID," + serialPort1)
	print("ID1 (actual): " + ID1 + ", expected: 17")
	print("")
	
	startTime = time.time()
	numCalls = 1000
	for _ in range(numCalls):
		ID1 = memoryClient.sendInstruction("getID," + serialPort1)
	endTime = time.time()
	print("total time: " + str(endTime-startTime))
	print("ID1 (actual): " + ID1 + ", expected: 17")
	return
	


def main():
	testNanotecSharedMemory()
	return


if __name__ == "__main__":
	main();
