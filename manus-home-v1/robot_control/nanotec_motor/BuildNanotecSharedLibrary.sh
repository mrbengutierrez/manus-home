
# A simple shell script to generate
# NanotecMotor.o, CommunicationNT.o, and NanotecMotor.so

g++ -c -fPIC NanotecMotor.cpp -o NanotecMotor.o
g++ -c -fPIC CommunicationNT.cpp -o CommunicationNT.o
g++ -shared NanotecMotor.o CommunicationNT.o -o NanotecMotor.so
echo "Generated NanotecMotor.o, CommunicationNT.o, and NanotecMotor.so"
