import sys, subprocess, os, select

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

winWidth = 500
winHeight = 500
scene = None

nc_cmd = 'netcat localhost 1234'
process = subprocess.Popen(nc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)


class gamewindow(QGraphicsView, QWidget):
    def __init__( self, parent = None ):
        super(gamewindow, self).__init__(parent)
        global winWidth, winHeight, process
        self.value = 100
        self.setGeometry(250, 100, winWidth, winHeight)
        self.setMaximumSize(winWidth, winHeight)
        self.setMinimumSize(winWidth, winHeight)
        self.setWindowTitle("Maze")

        timer2 = QTimer(self)
        timer2.timeout.connect(self.reading)
        timer2.start(10)

    def reading(self):
        poll_obj = select.poll()
        poll_obj.register(process.stdout, select.POLLIN)
        poll_result = poll_obj.poll(0)
        if(poll_result):
            line = str(process.stdout.readline()).rstrip('\n')
            if('wrist' in line):
                print(line)
            else:
                print('no')
            

    def keyPressEvent(self, hoge):
        global process
        if hoge.key() == Qt.Key_Z:
            process.stdin.write(str(self.value)+'\n')


def main():
    global winWidth, winHeight, scene, process
    app = QApplication(sys.argv)
    scene = QGraphicsScene( 0, 0, winWidth, winHeight)

    view = gamewindow(scene)
    view.show()
    view.raise_()

    app.exec_()


if __name__ == '__main__':
    main()
    sys.exit()