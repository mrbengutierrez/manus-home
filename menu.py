#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, subprocess, csv
import os
os.chdir("/home/mrbengutierrez/Desktop/RehabGame")

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

winWidth = 1200
winHeight = 900
scene = None


##-------------------------------------------
#    character setting


class Frame(QGraphicsItem):
    def __init__(self):
        super(Frame, self).__init__()
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setup()


class Game1(Frame):
    def setup(self):
        self.image = QImage("./picture/menu/clock.png")
    def boundingRect(self):
        return QRectF( 0, 0, self.image.width(), self.image.height())
    def paint(self, painter, option, widget):
        painter.drawImage( 0, 0, self.image)
    def mousePressEvent(self, event):
        subprocess.call("python 1-Clock.py", shell=True)


class Game2(Frame):
    def setup(self):
        self.image = QImage("./picture/menu/maze.png")
    def boundingRect(self):
        return QRectF( 0, 0, self.image.width(), self.image.height())
    def paint(self, painter, option, widget):
        painter.drawImage( 0, 0, self.image)
    def mousePressEvent(self, event):
        subprocess.call("python 2-Maze.py", shell=True)


class Game3(Frame):
    def setup(self):
        self.image = QImage("./picture/menu/pick.png")
    def boundingRect(self):
        return QRectF( 0, 0, self.image.width(), self.image.height())
    def paint(self, painter, option, widget):
        painter.drawImage( 0, 0, self.image)
    def mousePressEvent(self, event):
        subprocess.call("python 3-Pick.py", shell=True)


class Game4(Frame):
    def setup(self):
        self.image = QImage("./picture/menu/pong.png")
    def boundingRect(self):
        return QRectF( 0, 0, self.image.width(), self.image.height())
    def paint(self, painter, option, widget):
        painter.drawImage( 0, 0, self.image)
    def mousePressEvent(self, event):
        subprocess.call("python 4-Pong.py", shell=True)

class Game5(Frame):
    def setup(self):
        self.image = QImage("./picture/menu/race.png")
    def boundingRect(self):
        return QRectF( 0, 0, self.image.width(), self.image.height())
    def paint(self, painter, option, widget):
        painter.drawImage( 0, 0, self.image)
    def mousePressEvent(self, event):
        subprocess.call("python 5-Race.py", shell=True)


class Game6(Frame):
    def setup(self):
        self.image = QImage("./picture/menu/squeegee.png")
    def boundingRect(self):
        return QRectF( 0, 0, self.image.width(), self.image.height())
    def paint(self, painter, option, widget):
        painter.drawImage( 0, 0, self.image)
    def mousePressEvent(self, event):
        subprocess.call("python 6-Squeegee.py", shell=True)




##-------------------------------------------
#    window setting


class gamewindow(QGraphicsView, QWidget):
    def __init__( self, parent = None ):
        super(gamewindow, self).__init__(parent)
        global winWidth, winHeight
        self.setGeometry(250, 100, winWidth, winHeight)
        self.setWindowTitle("Menu")
        self.setBackgroundBrush(QColor( 248, 220, 133))
        self.initData()
        self.initScreen()

    def initData(self):
        f = open("patientID.csv", "r")        # csv file loading
        Reader1 = csv.reader(f)
        list1 = [ e for e in Reader1]
        f.close()
        self.textA = "{0:8s}".format( list1[ int(list1[0][7]) ][0] )

        f = open("therapist.csv", "r")        # csv file loading
        Reader2 = csv.reader(f)
        list2 = [ e for e in Reader2]
        f.close()
        self.textB = "{0:8s}".format( list2[ int(list2[0][1]) ][0] )

    def initScreen(self):
        exit = QPushButton("   BACK   ",self)
        exit.move( 900, 800)
        exit.setFont(QFont('Norasi',20))
        exit.setStyleSheet("background-color:rgb( 237, 125, 49); color:rgb( 255, 255, 255)");
        exit.clicked.connect(self.ExitClick)

        title = QLabel(self)                  # show title
        title.setFont(QFont('Norasi', 40))
        title.setStyleSheet("color:rgb( 189, 32, 49)")
        title.setText('MAIN MENU')
        title.move(80, 50)

        frame = QPixmap('./picture/menu/frame.png')
        pic = QLabel(self)
        pic.setPixmap(frame)
        pic.move(550, 20)
        label1 = QLabel(self)                 # show editer PATIONT ID
        label1.setFont(QFont('Norasi',20))
        label1.setText('Patient ID :')
        label1.move( 600, 40)
        label2 = QLabel(self)                 # show editer PATIONT ID
        label2.setFont(QFont('Norasi',20))
        label2.setText(self.textA)
        label2.move( 850, 40)
        label3 = QLabel(self)                 # show editer PATIONT ID
        label3.setFont(QFont('Norasi',20))
        label3.setText('Therapist  :')
        label3.move( 600, 82)
        label4 = QLabel(self)                 # show editer PATIONT ID
        label4.setFont(QFont('Norasi',20))
        label4.setText(self.textB)
        label4.move( 850, 82)

    def ExitClick(self):
        QApplication.quit()




class SceneSet:
    def setting(self):
        scale = 0.28
        game1 = Game1()
        game1.setPos(50, 180)
        game1.setTransform(QTransform.fromScale( scale, scale), True)
        scene.addItem(game1)
        game2 = Game2()
        game2.setPos(430, 180)
        game2.setTransform(QTransform.fromScale( scale, scale), True)
        scene.addItem(game2)
        game3 = Game3()
        game3.setPos(810, 180)
        game3.setTransform(QTransform.fromScale( scale, scale), True)
        scene.addItem(game3)
        game4 = Game4()
        game4.setPos(50, 500)
        game4.setTransform(QTransform.fromScale( scale, scale), True)
        scene.addItem(game4)
        game5 = Game5()
        game5.setPos(430, 500)
        game5.setTransform(QTransform.fromScale( scale, scale), True)
        scene.addItem(game5)
        game6 = Game6()
        game6.setPos(810, 500)
        game6.setTransform(QTransform.fromScale( scale, scale), True)
        scene.addItem(game6)




##-------------------------------------------
#    game setting


def main():
    app = QApplication(sys.argv)
    global scene, winWidth, winHeight
    scene = QGraphicsScene(0, 0, winWidth, winHeight)

    sceneset = SceneSet()
    sceneset.setting()

    view = gamewindow(scene)
    view.show()
    view.raise_()
    sys.exit(app.exec_())

if __name__== '__main__':
    main()
