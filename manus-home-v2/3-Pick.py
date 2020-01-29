#! /usr/bin/env python
# -*- coding: utf-8 -*-

import NanotecLibrary as NT # import python library to control nanotec motors

import sys, math, random, subprocess, re, select
import os
os.chdir("../rehab-games")

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


nc_cmd = 'netcat 192.168.1.12 3333'
process = subprocess.Popen(nc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)



#----------Global variable definition-----------------------------------

# Window size
winWidth = 1300
winHeight = 900

item = [0 for i in range(60)]
RandomPlace = [0 for i in range(60)]
RandomColor = [0 for i in range(60)]

# Initial value of matrix number
row = 4
column = 9




#---------layout------------------------------------------------------
# screen setting
class Backscreen(QGraphicsObject):
	def boundingRect(self):
		global winWidth, winHeight
		return QRectF(0, 0, winWidth, winHeight)

	def paint(self, painter, option, widget=None):
		painter.setPen(QPen(QColor( 167, 107, 223), 2))
		painter.setBrush(QColor( 167, 107, 223))
		painter.drawRect(0, 0, 50, 900)                 # left border
		painter.drawRect(1250, 0, 50, 900)              # right border
		painter.drawRect(50, 0, 1200, 250)              # upper border
		painter.drawRect(50, 850, 1200, 50)             # lower border

		painter.setPen(QPen(QColor( 243, 213, 26), 2))
		painter.setBrush(QColor( 243, 213, 26))
		painter.drawRect(45, 250, 5, 600)               # left yellow frame
		painter.drawRect(45, 245, 1210, 5)              # upper yellow frame
		painter.drawRect(1250, 250, 5, 600)             # right yellow frame
		painter.drawRect(45, 850, 1210, 5)              # lower yellow frame

class Score(QGraphicsItem):
	def __init__(self):
		super(Score, self).__init__()
		self.target = 0
		self.Number_of_Shape( 0, 0, 0, 0, 0, 0, 0, 0)
		self.shape = [ u"\u25cb", u"\u00d7", u"\u25a1", u"\u25b3", " a", " A", u"\u3042"," 1"]

	def boundingRect(self):
		return QRectF(0, -250, 600, 500)

	def Number_of_Shape(self, circle, cross, rect, tri, a, A, kana, Num):
		self.GT = [circle, cross, rect, tri, a, A, kana, Num]        # GT get target

	def TotalNum_of_Shape(self, Tcircle, Tcross, Trect, Ttri, Ta, TA, Tkana, Tnum):
		# total target
		self.TT = [Tcircle, Tcross, Trect, Ttri, Ta, TA, Tkana, Tnum]

	def loadvalue(self, target):
		self.target = target

	def paint(self, painter, option, widget):        # bellow makes score frame
		painter.setPen(Qt.red)
		painter.setFont(QFont('Norasi',32))
		painter.drawText(   5,  0, " TARGET")
		painter.setPen(Qt.blue)
		painter.setFont(QFont('Norasi',32))
		painter.drawText( 325,  5, self.shape[self.target])
		painter.setPen(Qt.red)
		painter.setFont(QFont('Norasi',32))
		painter.drawText(  30, 80, "SCORE")
		painter.setPen(Qt.black)
		painter.setFont(QFont('Norasi',32))
		painter.drawText( 310, 80, "{0}/{1}".format( self.GT[self.target], self.TT[self.target]))




#---------button------------------------------------------------------
# button setting
class Button_Flame(QGraphicsItem):
	def __init__(self):
		super(Button_Flame, self).__init__()
		self.r = 55
		self.setAcceptedMouseButtons(Qt.LeftButton)

	def boundingRect(self):
		return QRectF(0, 0, self.r, self.r)


class Quit_Button(Button_Flame):
	def paint(self, painter, option, widget):
		painter.setPen(QPen(QColor( 230, 115, 80), 3))        #draw outframe circle
		painter.setBrush(QColor( 248, 168, 133))
		painter.drawEllipse(0, 0, self.r, self.r)
		painter.setPen(QPen(QColor( 204, 0, 0), 8))           #draw cross in the circle
		painter.setBrush(QColor( 204, 0, 0))
		painter.drawLine(15, 15, 40, 40)
		painter.drawLine(15, 40, 40, 15)

	def mousePressEvent(self, event):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setWindowTitle("Attention")
		msg.setText("Do you really want to quit this game ?")
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		ret = msg.exec_()
		if ret == QMessageBox.Yes:
			QApplication.quit()
		elif ret == QMessageBox.No:
			event.ignore()


class Start_Button(Button_Flame):
	def paint(self, painter, option, widget):
		painter.setPen(QPen(QColor( 80, 116, 62), 3))       #draw outframe circle
		painter.setBrush(QColor( 157, 216, 140))
		painter.drawEllipse(0, 0, self.r, self.r)
		painter.setPen(QPen(QColor( 40, 163, 11), 3))       #draw triangle in the circle
		painter.setBrush(QColor( 40, 163, 11))
		self.aside = 15
		self.pgn = QPolygonF()
		for i in range(3):
			x = self.aside * math.cos(math.radians(120*i+0))
			y = self.aside * math.sin(math.radians(120*i+0))
			self.pgn.append(QPointF( self.aside + x + 11, self.aside + y + 12))
		painter.drawPolygon(self.pgn)

	def mousePressEvent(self, event):                       # connect Layout.reset() if start button is clicked
		global scene, item
		lay = Layout()
		lay.reset()
		scene.clear()
		lay.SceneSet()


class Settings_Button(Button_Flame):
	def paint(self, painter, option, widget):
		painter.setPen(QPen(QColor( 40, 96, 163), 3))       #draw outframe circle
		painter.setBrush(QColor( 116, 169, 214))
		painter.drawEllipse(0, 0, self.r, self.r)
		painter.setPen(QColor( 52, 38, 89))                 #draw S in the circle
		painter.setFont(QFont('Norasi',30))
		painter.drawText( 14, 42, str("S"))

	def mousePressEvent(self, event):                       # connect class SubWindow if setting button is clicked
		subWindow = SubWindow()
		subWindow.show()
		subWindow.exec_()




class SubWindow(QDialog):                                   # open the configuration window
	def __init__(self, parent=None):
		global row, column
		super(SubWindow, self).__init__(parent)
		self.setGeometry(500, 300, 300, 200)
		self.setMaximumSize( 300, 200)
		self.setMinimumSize( 300, 200)
		self.setWindowTitle("Settings")

		label1 = QLabel()
		label1.setFont(QFont('Norasi',20))
		label1.setText('row')
		self.sp1 = QSpinBox()                               # make a spin box and configure bellow
		self.sp1.setFont(QFont('Norasi',20))
		self.sp1.setRange( 1, 6)
		self.sp1.setValue(row)
		self.sp1.valueChanged.connect(self.valuechange1)    # this line works when the number of the spin box is changed

		label2 = QLabel()
		label2.setFont(QFont('Norasi',20))
		label2.setText('column')
		self.sp2 = QSpinBox()                               # make a spin box and configure bellow
		self.sp2.setFont(QFont('Norasi',20))
		self.sp2.setRange( 2, 10)
		self.sp2.setValue(column)
#        self.sp2.setSingleStep(2)                           # this line can control the step of the number of the spin box
		self.sp2.valueChanged.connect(self.valuechange2)    # this line works when the number of the spin box is changed

		layout = QGridLayout()                              # placement settings
		layout.addWidget(   label1, 0, 0)
		layout.addWidget( self.sp1, 0, 1)
		layout.addWidget(   label2, 1, 0)
		layout.addWidget( self.sp2, 1, 1)
		self.setLayout(layout)

	def valuechange1(self):                                 # if the number of row is changed
		global row
		row = self.sp1.value()

	def valuechange2(self):                                 # if the number of column is changed
		global column
		column = self.sp2.value()




class Select_Flame(QGraphicsItem):
	def __init__(self):
		super(Select_Flame, self).__init__()
		self.aside = 20
		self.target = 0
		self.setAcceptedMouseButtons(Qt.LeftButton)

	def boundingRect(self):
		return QRectF(0, 0, self.aside*2, self.aside*2)


class Select_Right(Select_Flame):                            # making target select button
	def paint(self, painter, option, widget):
		painter.setPen(QPen(QColor( 109, 154, 74), 1))
		painter.setBrush(QColor( 109, 154, 74))
		self.pgn = QPolygonF()
		for i in range(3):
			x = self.aside * math.cos(math.radians(120*i+0))
			y = self.aside * math.sin(math.radians(120*i+0))
			self.pgn.append(QPointF( self.aside + x, self.aside + y))
		painter.drawPolygon(self.pgn)

	def loadvalue(self, target):
		self.target = target

	def mousePressEvent(self, target):                       # target is connected to class 'Score'
		global score, left, scene
		if self.target == 7:
			self.target = 0
		else:
			self.target += 1
		score.loadvalue(self.target)
		left.loadvalue(self.target)
		scene.update()


class Select_Left(Select_Flame):                            # making target select button
	def paint(self, painter, option, widget):
		painter.setPen(QPen(QColor( 109, 154, 74), 1))
		painter.setBrush(QColor( 109, 154, 74))
		self.pgn = QPolygonF()
		for i in range(3):
			x = self.aside * math.cos(math.radians(120*i+180))
			y = self.aside * math.sin(math.radians(120*i+180))
			self.pgn.append(QPointF( self.aside + x, self.aside + y))
		painter.drawPolygon(self.pgn)

	def loadvalue(self, target):
		self.target = target

	def mousePressEvent(self, event):                       # target is connected to class 'Score'
		global score, right, scene
		if self.target == 0:
			self.target = 7
		else:
			self.target -= 1
		score.loadvalue(self.target)
		right.loadvalue(self.target)
		scene.update()


#---------------------------------------------------------------
# character setting


'''
 Bellow making each characters.
 These are called at class Layout.SceneSet().
 When these are called, they get identification number as self.number.
 If it is clicked, they gives self.number to global variable ID, and this ID
 use for acquisition judge at class gamewindow.Judge().
'''


class Characters(QGraphicsItem):                            # the frame composing main fuction about characters
	def __init__(self, num):
		super(Characters, self).__init__()
		self.number = num
		self.r = 80
		self.RandChara = qrand() % 7                        # self.RandChara use at making character of alpha, ALPHA, kana number
		self.setAcceptedMouseButtons(Qt.LeftButton)
		self.setFlag(QGraphicsItem.ItemIsMovable)
		self.Color = [ 0, Qt.red, Qt.blue, Qt.green, Qt.yellow, Qt.magenta]

	def mousePressEvent(self, event):
		global view
		view.loadvalue(self.number)


class circle(Characters):
	def boundingRect(self):
		return QRectF(0, 0, self.r, self.r)

	def paint(self, painter, option, widget):
		global RandomColor
		painter.setPen(QPen( self.Color[RandomColor[self.number]], 1))
		painter.setBrush( self.Color[RandomColor[self.number]])
		painter.drawEllipse(0, 0, self.r, self.r)


class circle_hollow(Characters):
	def boundingRect(self):
		return QRectF(0, 0, self.r, self.r)

	def paint(self, painter, option, widget):
		global RandomColor
		painter.setPen(QPen( self.Color[RandomColor[self.number]], 5))
		painter.setBrush(Qt.NoBrush)
		painter.drawEllipse(0, 0, self.r - 5, self.r - 5)


class cross(Characters):
	def boundingRect(self):
		return QRectF(15, 15, 95, 95)

	def paint(self, painter, option, widget):
		global RandomColor
		painter.setPen(QPen( self.Color[RandomColor[self.number]], 10))
		painter.setBrush( self.Color[RandomColor[self.number]])
		painter.drawLine(25, 25, 85, 85)
		painter.drawLine(25, 85, 85, 25)


class plus(Characters):
	def boundingRect(self):
		return QRectF(5, 5, 95, 95)

	def paint(self, painter, option, widget):
		global RandomColor
		painter.setPen(QPen( self.Color[RandomColor[self.number]], 10))
		painter.setBrush( self.Color[RandomColor[self.number]])
		painter.drawLine(15, 55, 90, 55)
		painter.drawLine(55, 15, 55, 90)


class rect(Characters):
	def boundingRect(self):
		return QRectF(0, 0, self.r, self.r)

	def paint(self, painter, option, widget):
		global RandomColor
		painter.setPen(QPen( self.Color[RandomColor[self.number]], 1))
		painter.setBrush( self.Color[RandomColor[self.number]])
		painter.drawRect(0, 0, self.r, self.r)


class rect_hollow(Characters):
	def boundingRect(self):
		return QRectF(0, 0, self.r, self.r)

	def paint(self, painter, option, widget):
		global RandomColor
		painter.setPen(QPen( self.Color[RandomColor[self.number]], 4))
		painter.setBrush(Qt.NoBrush)
		painter.drawRect(0, 0, self.r, self.r)


class triangle(Characters):
	def boundingRect(self):
		self.tri = 40
		self.ofsetx = -12
		return QRectF(self.ofsetx, 0, self.tri*2, self.tri*2)

	def paint(self, painter, option, widget):
		global RandomColor
		painter.setPen(QPen( self.Color[RandomColor[self.number]], 1))
		painter.setBrush( self.Color[RandomColor[self.number]])
		self.pgn = QPolygonF()
		for i in range(3):
			x = self.tri * math.cos(math.radians(120*i+30))
			y = self.tri * math.sin(math.radians(120*i+30))
			self.pgn.append(QPointF(self.tri+self.ofsetx+x, self.tri+y))
		painter.drawPolygon(self.pgn)


class triangle_hollow(Characters):
	def boundingRect(self):
		self.tri = 40
		self.ofsetx = -12
		return QRectF(self.ofsetx, 0, self.tri*2, self.tri*2)

	def paint(self, painter, option, widget):
		global RandomColor
		painter.setPen(QPen( self.Color[RandomColor[self.number]], 5))
		painter.setBrush(Qt.NoBrush)
		self.pgn = QPolygonF()
		for i in range(3):
			x = self.tri * math.cos(math.radians(120*i+30))
			y = self.tri * math.sin(math.radians(120*i+30))
			self.pgn.append(QPointF(self.tri+self.ofsetx+x, self.tri+y))
		painter.drawPolygon(self.pgn)


class alphabet(Characters):
	def boundingRect(self):
		return QRectF(0, -self.r, self.r, self.r+15)

	def paint(self, painter, option, widget):
		global RandomColor
		a_list = [ "a", "b", "c", "d", "e", "f", "g"]
		painter.setPen( self.Color[RandomColor[self.number]])
		painter.setFont(QFont('Norasi',70))
		painter.drawText(0, 0, str(a_list[self.RandChara]))


class ALPHABET(Characters):
	def boundingRect(self):
		return QRectF(0, -self.r, self.r, self.r)
	def paint(self, painter, option, widget):
		global RandomColor
		A_list = [ "A", "B", "C", "D", "E", "F", "G"]
		painter.setPen( self.Color[RandomColor[self.number]])
		painter.setFont(QFont('Norasi',70))
		painter.drawText(0, 0, str(A_list[self.RandChara]))


class kana(Characters):
	def boundingRect(self):
		return QRectF(0, -self.r, self.r, self.r+10)

	def paint(self, painter, option, widget):
		global RandomColor
		kana_list = [ u"\u3042", u"\u304b", u"\u3055", u"\u305f", u"\u306a", u"\u306f", u"\u307e"]
		painter.setPen( self.Color[RandomColor[self.number]])
		painter.setFont(QFont('Norasi',55))
		painter.drawText(0, 0, kana_list[self.RandChara])


class Number(Characters):
	def boundingRect(self):
		return QRectF(0, -self.r, self.r, self.r)

	def paint(self, painter, option, widget):
		global RandomColor
		painter.setPen( self.Color[RandomColor[self.number]])
		painter.setFont(QFont('Norasi',60))
		painter.drawText(0, 0, str("{0}".format(self.RandChara)))


#---------------------------------------------------------------
# drawing main window

class gamewindow(QGraphicsView):
	def __init__( self, parent = None ):
		super(gamewindow, self).__init__(parent)
		global winWidth, winHeight
		self.s = 0
		self.ID = 0
		self.value_init()

		#Offset depend on each character when acquisition determination
		#              circle  cross  rect  triangle  alpha  ALPHA  kana  Num
		self.ofset = [(   -75,   -90,  -80,      -60,   -40,   -65,  -70,  -30),     #ofset X cordinate left  side
					  (     0,   -20,    0,        0,    -5,   -10,  -10,  -10),     #ofset X cordinate right side
					  (   -55,   -65,  -55,      -35,    20,    25,   20,   25),     #ofset Y cordinate upper side
					  (   -20,   -45,  -30,      -25,    30,    55,   45,   40)]     #ofset Y cordinate lower side
		self.setGeometry(250, 100, winWidth, winHeight)
		self.setMaximumSize(winWidth, winHeight)
		self.setMinimumSize(winWidth, winHeight)
		self.setBackgroundBrush(QColor( 0, 0, 0))
		self.setWindowTitle("pick")
		fps = 50
		refresh_period = 1000/fps 
		timer = QTimer(self)
		timer.timeout.connect(self.Judge)
		timer.start(refresh_period)         # Judge() is called per fps
		self.ManusSetting()
		
		# initialize motors
		serialPort1 = "/dev/ttyACM0"
		ID1 = 1
		self.motor1 = NT.NanotecMotor(serialPort1,ID1)
		
		serialPort2 = "/dev/ttyACM1"
		ID2 = 2
		self.motor2 = NT.NanotecMotor(serialPort2,ID2)

	def ManusSetting(self):
		self.cursorX = 0        # cordinate of MIT - Manus X
		self.cursorY = 0        # cordinate of MIT - Manus Y
		self.R = 30             # cursor radius
		self.switch = 1         # load MIT - Manus values (aa and fe)

		pen   = QPen(Qt.red)
		brush = QBrush(pen.color())
		self.player = scene.addEllipse(self.cursorX - int(self.R/2), self.cursorY - int(self.R/2), self.R, self.R, pen, brush)    # MIT - Manus cursor

		timer1 = QTimer(self)
		timer1.timeout.connect(self.reading)    # load values from MIT - Manus
		timer1.start(10)

	def reading(self):
		global process, winWidth, winHeight

		if(self.switch == 1):
			aa_pos_360 = self.motor1.getAbsoluteAngularPosition() # command for load wrist aa_pos value
			aa_pos = (aa_pos_360 - 180.0)/ 360.0 # convert degrees [0,360.0) to [-1,1)
			if(aa_pos < 0):
				value_aa = float(aa_pos) * 10.0            # scaling
			else:
				value_aa = float(aa_pos) * 4.0             # scaling
			self.cursorY = int( (winHeight / 2) - ((winHeight / 2) * value_aa))
			self.switch = - self.switch
		else:
			fe_pos_360 = self.motor2.getAbsoluteAngularPosition() # command for load wrist fe_pos value
			fe_pos = (fe_pos_360 - 180.0)/ 360.0 # convert degrees [0,360.0) to [-1,1)
			value_fe = float(fe_pos) * 2.0
			self.cursorX = int( (winWidth / 2) + ((winWidth / 2) * value_fe))
			self.switch = - self.switch
		self.player.setRect(self.cursorX - int(self.R/2), self.cursorY - int(self.R/2), self.R, self.R)    # show player cursor

	def value_init(self):        # Variables for storing acquisition number
		self.circle = 0
		self.cross = 0
		self.rect = 0
		self.tri = 0
		self.alpha = 0
		self.ALPHA = 0
		self.kana = 0
		self.num = 0

	def loadvalue(self, ID):
		self.ID = ID

	def Judge(self):
		global RandomPlace, score
		pos = item[self.ID].pos()                                # get each character's position relate to ID
		x = pos.x()
		y = pos.y()
		self.ofset_select()                                 # set ofset about each characters

		# judgement whether the holding character over the border line or not (left, right, upper, lower)
		if (x < 50+self.ofset[0][self.s]) or (1250+self.ofset[1][self.s] < x) or (y < 230+self.ofset[2][self.s]) or (870+self.ofset[3][self.s] < y):
			if RandomPlace[self.ID] == 1:
				if (self.ID % 12 == 0) or (self.ID % 12 == 1):
					self.circle += 1
				elif (self.ID % 12 == 2) or (self.ID % 12 == 3):
					self.cross  += 1
				elif (self.ID % 12 == 4) or (self.ID % 12 == 5):
					self.rect   += 1
				elif (self.ID % 12 == 6) or (self.ID % 12 == 7):
					self.tri    += 1
				elif (self.ID % 12 == 8):
					self.alpha  += 1
				elif (self.ID % 12 == 9):
					self.ALPHA  += 1
				elif (self.ID % 12 == 10):
					self.kana   += 1
				else:
					self.num    += 1
				RandomPlace[self.ID] = 0                   # to avoid overap counting
				score.Number_of_Shape(self.circle, self.cross, self.rect, self.tri, self.alpha, self.ALPHA, self.kana, self.num)
				scene.update()

	def ofset_select(self):                                # set ofset about each characters
		if (self.ID % 12 == 0) or (self.ID % 12 == 1):
			self.s = 0
		elif (self.ID % 12 == 2) or (self.ID % 12 == 3):
			self.s = 1
		elif (self.ID % 12 == 4) or (self.ID % 12 == 5):
			self.s = 2
		elif (self.ID % 12 == 6) or (self.ID % 12 == 7):
			self.s = 3
		elif (self.ID % 12 == 8):
			self.s = 4
		elif (self.ID % 12 == 9):
			self.s = 5
		elif (self.ID % 12 == 10):
			self.s = 6
		else:
			self.s = 7
		self.update()

	def resizeEvent(self, e):        # If you want to add a function corresponding to changing the window size, write it here.
		pass




class Layout:
	def SceneSet(self):
		global scene, winWidth, winHeight, item, RandomPlace, RandomColor, row, column

		# How many each characters are exist (connected to class Score)
		Tcircle = Tcross = Trect = Ttri = Ta = TA = Tkana = Tnum = 0    # T means total

		adjustX = [ 0,   0, 240, 150, 110, 80, 60, 45, 35, 30, 15]      # character position depends on the number of column
		adjustY = [ 0, 240, 110,  60,  40, 30, 15]                      # character position depends on the number of row

		ofsetX = 50 + adjustX[column]                       # setting ofset
		ofsetY = 250 + adjustY[row]                         # setting ofset

		TotalChara = row * column
		GapX = 1200 / column
		GapY = 600  / row

		for num in range(TotalChara):                       #random color setting
			while True:
				value = random.randint( 0, TotalChara - 1)
				if RandomColor[value] == 0:
					RandomColor[value] = (num % 5) + 1
					break

		for num in range(TotalChara):                       #decide where to place
			while True:
				value = random.randint( 0, TotalChara - 1)
				if RandomPlace[value] == 0:
					PosRow = int(value / column)
					PosCol = value % column
					RandomPlace[value] = 1
					break

			#place each characters in turn below
			if num%12 == 0:
				item[num] = circle(num)
				item[num].setPos( ofsetX + (PosCol*GapX)     , ofsetY + (PosRow*GapY)     )
				Tcircle += 1
			elif num%12 == 1:
				item[num] = circle_hollow(num)
				item[num].setPos( ofsetX + (PosCol*GapX)     , ofsetY + (PosRow*GapY)     )
				Tcircle += 1
			elif num%12 == 2:
				item[num] = cross(num)
				item[num].setPos( ofsetX + (PosCol*GapX) - 10, ofsetY + (PosRow*GapY) - 20)
				Tcross += 1
			elif num%12 == 3:
				item[num] = plus(num)
				item[num].setPos( ofsetX + (PosCol*GapX) - 10, ofsetY + (PosRow*GapY) - 20)
				Tcross += 1
			elif num%12 == 4:
				item[num] = rect(num)
				item[num].setPos( ofsetX + (PosCol*GapX)     , ofsetY + (PosRow*GapY)     )
				Trect += 1
			elif num%12 == 5:
				item[num] = rect_hollow(num)
				item[num].setPos( ofsetX + (PosCol*GapX)     , ofsetY + (PosRow*GapY)     )
				Trect += 1
			elif num%12 == 6:
				item[num] = triangle(num)
				item[num].setPos( ofsetX + (PosCol*GapX) + 15, ofsetY + (PosRow*GapY)     )
				Ttri += 1
			elif num%12 == 7:
				item[num] = triangle_hollow(num)
				item[num].setPos( ofsetX + (PosCol*GapX) + 15, ofsetY + (PosRow*GapY)     )
				Ttri += 1
			elif num%12 == 8:
				item[num] = alphabet(num)
				item[num].setPos( ofsetX + (PosCol*GapX) + 15, ofsetY + (PosRow*GapY) + 70)
				Ta += 1
			elif num%12 == 9:
				item[num] = ALPHABET(num)
				item[num].setPos( ofsetX + (PosCol*GapX) + 10, ofsetY + (PosRow*GapY) + 80)
				TA += 1
			elif num%12 == 10:
				item[num] = kana(num)
				item[num].setPos( ofsetX + (PosCol*GapX) +  5, ofsetY + (PosRow*GapY) + 70)
				Tkana += 1
			else:
				item[num] = Number(num)
				item[num].setPos( ofsetX + (PosCol*GapX) + 15, ofsetY + (PosRow*GapY) + 70)
				Tnum += 1
			scene.addItem(item[num])

		# set outflame and backscreen
		backscreen = Backscreen()
		scene.addItem(backscreen)

		# use picture
		housePic = QGraphicsPixmapItem(QPixmap('./picture/pick/house.png'))
		housePic.setTransform(QTransform.fromScale( 1.79, 1.79), True)
		scene.addItem(housePic)
		ghostPic = QGraphicsPixmapItem(QPixmap('./picture/pick/ghost.png'))
		ghostPic.setTransform(QTransform.fromScale( 1.2, 1.2), True)
		ghostPic.setPos( 1060, 0)
		scene.addItem(ghostPic)
		flamePic = QGraphicsPixmapItem(QPixmap('./picture/pick/flame.png'))
		flamePic.setTransform(QTransform.fromScale( 1.05, 1.0), True)
		flamePic.setPos( 540, 25)
		scene.addItem(flamePic)

		# score flame
		global score
		score = Score()
		score.TotalNum_of_Shape(Tcircle, Tcross, Trect, Ttri, Ta, TA, Tkana, Tnum)
		score.setPos( 590, 110)
		scene.addItem(score)

		#button setting
		global left, right
		QToolTip.setFont(QFont('SansSerif', 10))
		quit = Quit_Button()
		quit.setPos( 430, 35)
		quit.setToolTip('Game Quit')                        # pop up
		scene.addItem(quit)
		start = Start_Button()
		start.setPos( 430, 105)
		start.setToolTip('Game Start')                      # pop up
		scene.addItem(start)
		set = Settings_Button()
		set.setPos( 430, 175)
		set.setToolTip('Game Settings')                     # pop up
		scene.addItem(set)
		right = Select_Right()
		right.setPos( 990, 80)
		right.setToolTip('Target select')                   # pop up
		scene.addItem(right)
		left = Select_Left()
		left.setPos( 850, 80)
		left.setToolTip('Target select')                    # pop up
		scene.addItem(left)

	def reset(self):
		global RandomPlace, RandomColor, view
		view.value_init()
		RandomPlace = [0 for i in range(60)]
		RandomColor = [0 for i in range(60)]




def main():
	qsrand(QTime(0, 0, 0).secsTo(QTime.currentTime()))
	global scene, winWidth, winHeight

	app = QApplication(sys.argv)
	scene = QGraphicsScene( 0, 0, winWidth, winHeight)

	#charactr position set 
	lay = Layout()
	lay.SceneSet()

	global view
	view = gamewindow(scene)
	view.show()
	view.raise_()
	app.exec_()




if __name__== '__main__':
	main()
	sys.exit()
