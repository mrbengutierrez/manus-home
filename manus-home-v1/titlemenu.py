#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, subprocess, csv
import os
os.chdir("/home/mrbengutierrez/Desktop/RehabGame")


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


winWidth = 900
winHeight = 650
scene = None


##-------------------------------------------
#    window setting


class gamewindow(QGraphicsView, QWidget):
    def __init__( self, parent = None ):
        super(gamewindow, self).__init__(parent)
        global winWidth, winHeight
        self.mouseX = 0
        self.mouseY = 0
        self.wx = winWidth
        self.wy = winHeight
        self.timing = 0
        self.gamespeed = 20
        self.ID = 0
        self.thera = 0
        self.initUI()

    def initUI(self):
        global winWidth, winHeight, scene, patientID, therapist
        self.setGeometry(250, 100, winWidth, winHeight)
        self.setBackgroundBrush(QColor( 248, 220, 133))
        self.setWindowTitle("Title menu")

        title = QLabel(self)                  # show title
        title.setFont(QFont('Norasi', 40))
        title.setStyleSheet("color:rgb( 189, 32, 49)")
        title.setText('Welcome to Rehab Game!!')
        title.move(80, 50)

        label1 = QLabel(self)                 # show editer PATIONT ID
        label1.setFont(QFont('Norasi',20))
        label1.setText('PATIENT  ID')
        label1.move( 80, 200)
        self.edit1 = QLineEdit(self)
        self.edit1.setFont(QFont('Norasi',20))
        self.edit1.move( 80, 240)

        label2 = QLabel(self)                 # show editer THERAPIST NAME
        label2.setFont(QFont('Norasi',20))
        label2.setText('THERAPIST  NAME')
        label2.move( 80, 350)
        self.edit2 = QLineEdit(self)
        self.edit2.setFont(QFont('Norasi',20))
        self.edit2.move( 80, 390)

        enter = QPushButton(" ENTER ",self)   # set button
        enter.move( 80, 500)
        enter.setFont(QFont('Norasi',20))
        enter.setStyleSheet("background-color:rgb( 68, 114, 196); color:rgb( 255, 255, 255)");
        enter.clicked.connect(self.EnterClick)
        exit = QPushButton("   EXIT   ",self)
        exit.move( 230, 500)
        exit.setFont(QFont('Norasi',20))
        exit.setStyleSheet("background-color:rgb( 237, 125, 49); color:rgb( 255, 255, 255)");
        exit.clicked.connect(self.ExitClick)

        f = open("patientID.csv", "r")        # csv file loading
        Reader1 = csv.reader(f)
        patientID = [ e for e in Reader1]
        f.close()

        f = open("therapist.csv", "r")        # csv file loading
        Reader2 = csv.reader(f)
        therapist = [ e for e in Reader2]
        f.close()

    def EnterClick(self):
        global patientID, therapist, IDtext, Theratext

        IDtext = self.edit1.text()
        find1 = False                         # searching your entered name
        for num in range(len(patientID)):
            if IDtext == patientID[num][0]:
                find1 = True
                patientID[0][7] = num
                break
            else:
                find1 = False

        Theratext = self.edit2.text()
        find2 = False                         # searching your entered name
        for num in range(len(therapist)):
            if Theratext == therapist[num][0]:
                find2 = True
                therapist[0][1] = num
                break
            else:
                find2 = False

        if (find2 == True):                   # whether it can find it or not
            if (find1 == True):
                f = open('patientID.csv', 'w')
                writer = csv.writer(f)
                writer.writerows(patientID)
                f.close()

                f = open('therapist.csv', 'w')
                writer = csv.writer(f)
                writer.writerows(therapist)
                f.close()
                subprocess.call("python menu.py", shell=True)
            else:
                confirm = confirmWindow()
                confirm.show()
                confirm.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Attention")
            msg.setText("Please check therapist name.")
            msg.setStandardButtons(QMessageBox.Ok)
            ret = msg.exec_()
            if ret == QMessageBox.Ok:
                self.close

    def ExitClick(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Attention")
        msg.setText("Do you really want to exit from Reha Game?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msg.exec_()
        if ret == QMessageBox.Yes:
            QApplication.quit()
        elif ret == QMessageBox.No:
            self.close


class confirmWindow(QDialog):
    def __init__(self, parent=None):
        super(confirmWindow, self).__init__(parent)
        self.setGeometry(500, 300, 300, 200)
        self.setMaximumSize( 300, 200)
        self.setMinimumSize( 300, 200)
        self.setWindowTitle("confirm")

        text1 = QLabel(self)
        text1.setFont(QFont('Norasi', 15))
        text1.setText("Is this a new patient?")
        text1.move( 40, 30)
        text2 = QLabel(self)
        text2.setFont(QFont('Norasi', 11))
        text2.setText("Click yes to register now.")
        text2.move( 40, 65)
        text3 = QLabel(self)
        text3.setFont(QFont('Norasi', 11))
        text3.setText("If already registrated,\nplease doublecheck your input.")
        text3.move( 40, 90)

        Ybutton = QPushButton(" YES ",self)
        Ybutton.move( 50, 145)
        Ybutton.clicked.connect(self.Registration)
        Nbutton = QPushButton(" NO ",self)
        Nbutton.move( 160, 145)
        Nbutton.clicked.connect(self.close)

    def Registration(self):
        global patientID, therapist, IDtext, Theratext
        patientID.append([ IDtext, 0, 0, 0, 0, 0, 0])
        patientID[0][7] = len(patientID) - 1
        f = open('patientID.csv', 'w')
        writer = csv.writer(f)
        writer.writerows(patientID)
        f.close()
        self.close()
        subprocess.call("python menu.py", shell=True)


##-------------------------------------------
#    game setting


def main():
    app = QApplication(sys.argv)
    global scene, winWidth, winHeight
    scene = QGraphicsScene(0, 0, winWidth, winHeight)

    MitBeaver = QGraphicsPixmapItem(QPixmap('./picture/menu/mitbeaver.png'))
    MitBeaver.setPos(480, 150)
    MitBeaver.setTransform(QTransform.fromScale( 1.79, 1.79), True)
    scene.addItem(MitBeaver)

    view = gamewindow(scene)
    view.show()
    view.raise_()
    sys.exit(app.exec_())


if __name__== '__main__':
    main()
