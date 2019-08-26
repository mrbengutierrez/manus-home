
# build shared library
sudo bash BuildNanotecSharedLibrary.sh

# build NanotecNetworkServer
g++ NanotecNetworkServer.cpp NanotecParser.cpp NanotecMotorContainer.cpp NanotecMotor.cpp CommunicationNT.cpp -o NanotecNetworkServer

# build NanotecSharedMemory
g++ NanotecSharedMemory.cpp SharedMemory.cpp NanotecParser.cpp NanotecMotorContainer.cpp NanotecMotor.cpp CommunicationNT.cpp -o NanotecSharedMemory

# build calibration file
g++ calibrateMotors.cpp NanotecMotor.cpp CommunicationNT.cpp -o calibrateMotors
