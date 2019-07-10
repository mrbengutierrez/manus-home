# nanotec

### Contributors
* Benjamin Gutierrez (mrbengutierrez@gmail.com)
  * Starting to figure out how to control multiple motors
  * Worked on python & c++ position, velocity, and torque set & get functions
* Moises Alencastre-Miranda (alencastre@gmail.com)
  * Developed a torque control user interface
  * Developed program to read relative angle in degrees


### About
The purpose of this repository is to control multiple nanotec motors. The type of nanotec motor that was used was PD2-C4118L1804-E-01. This motor package includes a stepper motor along with a hardware closed loop position, speed, and torque controller. To interface with the motors, a serial USB interface is used.


#### File Management
* BuildNanotecSharedLibrary.sh
  * Helper library to create object code and a shared libary
  * Converting: NanotecMotor.cpp, CommunicationNT.cpp
  * Into: NanotecMotor.o, CommunicationNT.o, and NanotecMotor.so
* CommunicationNT.cpp
  * C++ source code to manage communication with nanotec motors
* Communication.h
  * C++ header file for Communication.cpp
* Communication.o
  * C++ object file for Communication.o
* main.cpp
  * C++ source code to test NanotecMotor.cpp
  * Can be used to run program using NanotecMotor.h
* NanotecLibrary.py
  * Python file to interface with nanotec motors
  * Acts as a python wrapper to NanotecMotor.cpp
  * More specifically NanotecLibrary.py(NanotecMotorWrapper.h(NanotecMotor.cpp)))
* NanotecMotor.cpp
  * C++ Source code that provide position, velocity, & torque commands for nanotec motors
* NanotecMotor.h
  * C++ header file for NanotecMotor.cpp
* NanotecMotor.o
  * C++ object file for NanotecMotor.cpp
* NanotecMotor.so
  * C++ shared library file for NanotecMotor.cpp
* NanotecMotorWrapper.h
  * Provides a C wrapper for NanotecMotor.cpp
* testNanotec.py
  * Python file to test if NanotecLibrary.py is working properly


#### Speed Tests

Date Conducted: July 8, 2019  
Number of function calls: 100  
Processor: Intel(R) Core(TM) i7-3840QM 2.8GHz   


| Function Name                           | NanotecWrapper | NanotecSharedMemory | NanotecNetwork |
| --------------------------------------- | -------------- | ------------------- | -------------- |
| getID                                   | 0.5 us         | 12 us               | 27 us          |
| getSerialPort                           | 0.8 us         | 11 us               | 24 us          |
| setTorque                               | 3 ms           | 3 ms                | 3 ms           |
| setAngularVelocity                      | 24 ms          | 24 ms               | 24 ms          |
| setRelativeAngularPosition              | 46 ms          | 46 ms               | 46 ms          |
| setAbsoluteAngularPosition              | 49 ms          | 49 ms               | 49 ms          |
| setAbsoluteAngularPositionShortestPath  | 49 ms          | 49 ms               | 49 ms          |
| stop                                    | 6 ms           | 6 ms                | 6 ms           |
| getTorque                               | 6 ms           | 6 ms                | 6 ms           |
| getAngularVelocity                      | 3 ms           | 3 ms                | 3 ms           |
| getAbsoluteAngularPosition              | 3 ms           | 3 ms                | 3 ms           |
| readPhysicalEncoder                     | 3 ms           | 3 ms                | 3 ms           |







#### Updates by Benjamin Gutierrez
v1.6 12/June/19 
The following functions were implemented for the Nanotec motor class:
* setTorque(...)
* setAngularVelocity(...)
* setRelativeAngle(...) 
* setAbsoluteAngularPosition(...)
* setAbsoluteAngularPosition(...)
* setAbsoluteAngularPositionShortestPath(...)
* stop()
* getTorque()
* getAngularVelocity()
* getAbsoluteAngularPosition()
* closePort()

Observations:
* Torque
  * There seems to a lower value of torque in which the motor shaft does not move.
  * When measuring the torque using the function NanotecMotor::getTorque(), if there is no load of the shaft, the return values seem a bit random.
    But they seem to all be small than the torque command if the motor is in torque mode.
* Angular velocity
  * Seems to work as expected. Tested and works for values below 400 rpm. Further tests should be done for higher values.
* Angular Position
  * Also seems to work as expected. There is a noticable audible vibration sound when the motor is hold a position.
    This may be due to the values for internal PI position controller in the motor. A possible fix may be to lower these values.



#### Previous Updates by Moises Alencastre-Miranda
v1.5 17/May/18 Adjustments: The value to map the torque force to percentage was
               increased to be always inside of the angle range. If the torque
               is less or equal than 1% in both cases (positive or negative) is
               considered a torque value of 1.1%. It seems that the positive
               torque (clockwise) has less force, this was incremented in 20%.
               Display of the torque. Measure processing time.

v1.4 17/May/18 The program has a GUI to display and see the angle of the motor.
               The code was improved separating the control in other class.

v1.3 17/May/18 The motor has a problem found for torque values +9 and +10. The
               program is skipping those values. Small corrections. Now the
               basic control is working, maintaining a zero torque in a range of
               angles and pushing into this range if the angle is out of range.

v1.2 17/May/18 This version includes a function to mantain a zero torque in a
               given range of angles and a spring simulation pushing with a
               force to come back if you go out of the range.

v1.1 16/May/18 A single control of the torque value with fixed values was added
               depending on the angle.

v1.0 15/May/18 Corrections to the way of calculate the angle when the value
               change around 0 and 16^8.

v0.9 14/May/18 Correction of the size of the arrays for sprintf when te program
               is compiled with -O3. Correction to start with torque value zero
               and then it can be changed (in this case works for the HBot).

v0.8 11/May/18 Now it includes more options in the menu to change the torque.

v0.7 10/May/18 Now also contains the reading of the current position (in angle).

v0.6 10/May/18 It includes a function to change in real time the torque value
               and control this value which keys in the executable program.

v0.5 10/May/18 It includes an automatic way to build the array of bytes with
               hexadecimal values to activate the torque mode and stop it.
