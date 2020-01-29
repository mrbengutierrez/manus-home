sudo apt-get install gedit # basic code editor
sudo apt-get install geany # better code editor
sudo apt-get install python3-pyqt5   # for python3
sudo apt-get install python-pyqt5    # for python2
sudo apt-get install libopencv-dev python3-opencv
sudo apt-get install python-dev   # for sysv_ipc install
sudo apt-get install python3-dev # for sysv_ipc install

sudo apt-get install python3-numpy # for arm controller
sudo apt-get install python3-scipy # for arm controller
sudo apt-get install python3-matplotlib # for arm controller

# Have to build Nanotec c++ libraries
cd robot_control/nanotec_motor/
sudo bash BuildAllNanotecFiles.sh

# Note: also have to install sysv_ipc located in nanotec-motor

cd sysv_ipc-1.0.0/
sudo python setup.py install
sudo python3 setup.py install



