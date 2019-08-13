import sys, math, random, time, subprocess, re, select

# import python library to control nanotec motors
from NanotecLibrary import NanotecWrapper as NanotecMotor

import os
os.chdir("../rehab-games")

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

winWidth = 1300
winHeight = 900

nc_cmd = 'netcat 192.168.1.12 3333'
process = subprocess.Popen(nc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)




#---------------------------------------------------------------
# character setting


class Circle(QGraphicsItem):            # set center circle
	def __init__(self):
		super(Circle, self).__init__()
		self.d = 60
		self.r = self.d / 2

	def boundingRect(self):
		return QRectF( - self.r , - self.r, self.d, self.d)

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.black, 2))
		painter.setBrush(Qt.gray)
		painter.drawEllipse( - self.r, - self.r, self.d, self.d)




class Target(QGraphicsItem):            # set target circle
	def __init__(self):
		super(Target, self).__init__()
		self.d = 120
		self.r = self.d / 2

	def boundingRect(self):
		return QRectF( - self.r, - self.r, self.d, self.d)

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.red, 6))
		painter.setBrush(Qt.NoBrush)
		painter.drawEllipse( - self.r, - self.r, self.d, self.d)




class Animals(QGraphicsItem):           # set animal pictures
	def __init__(self, num):
		super(Animals, self).__init__()
		self.num = num
		self.pic = ["dog", "duck", "bear", "rabbit", "pig", "lion", "raccoon", "elephant"]
		path = "./picture/clock/" + self.pic[self.num] + ".png"
		self.image = QImage(path)

	def boundingRect(self):
		return QRectF( - self.image.width() / 2, - self.image.height() / 2, self.image.width(), self.image.height())

	def paint(self, painter, option, widget):
		painter.drawImage( - self.image.width() / 2, - self.image.height() / 2, self.image)




class Arrow(QGraphicsItem):             # set indicator (draw rect and triangle)
	def __init__(self):
		super(Arrow, self).__init__()
		self.pos = [ 230, -100]
		self.angle = [ 0, 180]

	def DirectionSet(self, direction):
		self.direction = direction

	def boundingRect(self):
		self.tri = 30
		return QRectF( -25, -25, 250, 50)

	def paint(self, painter, option, widget):
		painter.setPen(QPen(QColor( 255, 0, 0), 2))
		painter.setBrush(QColor( 255, 129, 25))
		painter.drawRect( 80, - self.tri + 22, 160, 15)
		self.pgn = QPolygonF()
		for i in range(3):
			x = self.tri * math.cos(math.radians(120*i))
			y = self.tri * math.sin(math.radians(120*i))
			self.pgn.append(QPointF( self.pos[self.direction] + x, y))
		painter.rotate(self.angle[self.direction])
		painter.drawPolygon(self.pgn)




class Score(QGraphicsItem):             # set score indicator
	def __init__(self):
		super(QGraphicsItem, self).__init__()

	def TrialSet(self, trial):
		self.textCount = "{0:2d}".format(trial)

	def boundingRect(self):
		return QRectF(0, 0, 300, 600)

	def paint(self, painter, option, widget):
		total = 30
		painter.setPen(Qt.red)
		painter.setFont(QFont('Norasi',32))
		painter.drawText( 0, 0, str("SCORE"))
		painter.setPen(Qt.black)
		painter.setFont(QFont('Norasi', 40))
		painter.drawText( 10, 70, self.textCount + "/" + str("{0}".format(total)))




#---------------------------------------------------------------
# drawing main window


class gamewindow(QGraphicsView):
	def __init__( self, parent = None):
		super(gamewindow, self).__init__(parent)
		global winWidth, winHeight
		self.wx = winWidth
		self.wy = winHeight
		self.randmemory = [0 for i in range(8)]             # to avoid pointing same place over and over
		self.ofsetX = 5                                     # adjusting the position
		self.ofsetY = 5                                     # adjusting the position
		self.setGeometry(250, 100, self.wx, self.wy)
		self.setMaximumSize(self.wx, self.wy)
		self.setMinimumSize(self.wx, self.wy)
		self.setWindowTitle("clock")
		self.setMouseTracking(True)                         # become to be able to chase the mouse cursor
		self.initUI()
		self.ManusSetting()
		
		# initialize motors
		serialPort1 = "/dev/ttyACM0"
		ID1 = 1
		self.motor1 = NanotecMotor(serialPort1,ID1)
		
		serialPort2 = "/dev/ttyACM1"
		ID2 = 2
		self.motor2 = NanotecMotor(serialPort2,ID2)

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

		timer2 = QTimer(self)
		timer2.timeout.connect(self.moving)     # game action
		timer2.start(10)

	def initUI(self):                                       # button settings
		quit = QPushButton("     QUIT     ",self)           # quit button
		quit.move( 50, 60)
		quit.setFont(QFont('Norasi',18))
		quit.setStyleSheet("background-color:rgb( 255, 98, 50); color:rgb( 255, 255, 255)");
		quit.clicked.connect(self.QuitClick)
		reset = QPushButton("    RESET   ",self)            # reset button
		reset.move( 50, 130)
		reset.setFont(QFont('Norasi',18))
		reset.setStyleSheet("background-color:rgb( 40, 175, 12); color:rgb( 255, 255, 255)");
		reset.clicked.connect(self.ResetClick)
		settings = QPushButton(" SETTINGS ",self)           # settings button
		settings.move( 50, 200)
		settings.setFont(QFont('Norasi',18))
		settings.setStyleSheet("background-color:rgb( 80, 77, 203); color:rgb( 255, 255, 255)");
		settings.clicked.connect(self.SettingClick)

	def valueload(self, count, direction, position, cordX, cordY):
		self.count = count            # your score
		self.direction = direction    # a variable for alternately selectin center and outside
		self.position = position      # a variable which determines the position of the next target
		self.cordX = cordX            # next target circle's cordinate X
		self.cordY = cordY            # next target circle's cordinate Y

	def reading(self):
		global process, winWidth, winHeight
			
		if (self.switch == 1):
			aa_pos_360 = self.motor1.getAbsoluteAngularPosition() # command for load wrist aa_pos value
			aa_pos = (aa_pos_360 -180.0)/ 360.0 # convert degrees [0,360.0) to [-1,1)
			if(aa_pos < 0):
				value_aa = float(aa_pos) * 10.0            # scaling
			else:
				value_aa = float(aa_pos) * 4.0             # scaling
			self.cursorY = int( (winHeight / 2) - ((winHeight / 2) * value_aa))
			self.switch = - self.switch
		else:
			fe_pos_360 = self.motor2.getAbsoluteAngularPosition() # command for load wrist_fe_pos value
			fe_pos = (fe_pos_360 - 180.0)/ 360.0 # convert degrees [0,360.0) to [-1,1)
			value_fe = float(fe_pos) * 2.0
			self.cursorX = int( (winWidth / 2) + ((winWidth / 2) * value_fe))
			self.switch = - self.switch
			
		self.player.setRect(self.cursorX - int(self.R/2), self.cursorY - int(self.R/2), self.R, self.R)    # show player cursor
		
		
	   

	def moving(self):
		global score, target, arrow

		if ( self.cursorX + self.ofsetX - self.cordX) ** 2 + ( self.cursorY + self.ofsetY - self.cordY) ** 2 < 60 ** 2:    # whether mouse cursor has reached the target
			if self.direction == 0:
				self.randmemory[self.position] = 1
				if (self.randmemory.count(0)) == 0:
					self.randmemory = [0] * 8
				self.cordX = self.wx / 2
				self.cordY = self.wy / 2
				self.direction = 1
				arrow.DirectionSet(self.direction)                  # pass variable to item 'arrow' to change arrow's direction
			elif self.direction == 1:
				while True:                                         # to avoid pointing same place over and over
					self.position = random.randint(0,7)
					if self.randmemory[self.position] == 0:
						break
				self.cordX = self.wx / 2 + 350 * math.cos ( math.pi * self.position / 4)  # setting next target circle's cordinate X
				self.cordY = self.wy / 2 + 350 * math.sin ( math.pi * self.position / 4)  # setting next target circle's cordinate Y
				self.direction = 0
				self.count += 1
				arrow.DirectionSet(self.direction)
				score.TrialSet(self.count)
				if (self.count == 30):                              # finish this game if you finishing the trial count
					self.setMouseTracking(False)                    # become to not be able to chase the mouse cursor

			target.setPos( self.cordX, self.cordY)                  # setting target and arrow position
			arrow.setRotation(45 * self.position)
			scene.update()

	def QuitClick(self):            # function after pressing quit button
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setWindowTitle("Attention")
		msg.setText("Do you really want to quit this game ?")
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		ret = msg.exec_()
		if ret == QMessageBox.Yes:
			QApplication.quit() 
		elif ret == QMessageBox.No:
			self.close

	def ResetClick(self):           # function after pressing reset button
		global scene
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setWindowTitle("Attention")
		msg.setText("Reset ?")
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		ret = msg.exec_()
		if ret == QMessageBox.Yes: # POSSIBLE BUG IN IF BLOCK
			scene.clear()
			self.count = 0
			self.direction = 0
			self.position = random.randint(0,7)
			self.cordX = self.wx / 2 + 350 * math.cos ( math.pi * self.position / 4)
			self.cordY = self.wy / 2 + 350 * math.sin ( math.pi * self.position / 4)
			lay = Layout(self.direction, self.position, self.cordX, self.cordY)
			lay.SceneSet()
			self.setMouseTracking(True)
		elif ret == QMessageBox.No:
			self.close

	def SettingClick(self):          # function after pressing reset button ( not implemented)
		settingWindow = SettingWindow()
		settingWindow.show()
		settingWindow.exec_()




class SettingWindow(QDialog):
	def __init__(self, parent=None):
		super(SettingWindow, self).__init__(parent)
		self.setGeometry(500, 300, 300, 200)
		self.setMaximumSize( 300, 200)
		self.setMinimumSize( 300, 200)
		self.setWindowTitle("Settings")

		label1 = QLabel(self)
		label1.setFont(QFont('Norasi',20))
		label1.setText('comming')
		label1.move( 40, 30)

		label2 = QLabel(self)
		label2.setFont(QFont('Norasi',20))
		label2.setText('soon')
		label2.move( 40, 70)




class Layout:                 # screen display
	def __init__( self, direction, position, cordX, cordY):
		global winWidth, winHeight
		self.direction = direction
		self.position = position
		self.cordX = cordX
		self.cordY = cordY
		self.wx = winWidth
		self.wy = winHeight

	def SceneSet(self):
		global scene, score, target, arrow

		BGPic = QGraphicsPixmapItem(QPixmap('./picture/clock/grass.jpg'))  # back ground picture
		BGPic.setTransform(QTransform.fromScale( 1.35, 1.25), True)
		BGPic.setPos( 0, 0)
		scene.addItem(BGPic)

		frame = QGraphicsPixmapItem(QPixmap('./picture/clock/frame.png'))  # frame of score
		frame.setTransform(QTransform.fromScale( 0.8, 0.8), True)
		frame.setPos( 1050, 50)
		scene.addItem(frame)

		score = Score()                    # display score
		score.TrialSet(0)
		score.setPos( 1100, 120)
		scene.addItem(score)

		circle = Circle()                  # display center circle
		circle.setPos( self.wx / 2, self.wy / 2)
		scene.addItem(circle)

		for num in range(0, 8):            # display each animals
			x = self.wx / 2 + 350 * math.cos( math.pi * num / 4)
			y = self.wy / 2 + 350 * math.sin( math.pi * num / 4)
			animals = Animals(num)
			animals.setPos( x, y)
			animals.setTransform( QTransform.fromScale( 0.9, 0.9), True)
			scene.addItem(animals)

		target = Target()                  # display holo circle around the target animal
		target.setPos( self.cordX, self.cordY)
		scene.addItem(target)

		arrow = Arrow()                    # display arrow
		arrow.DirectionSet(self.direction)
		arrow.setPos( self.wx / 2, self.wy / 2)
		arrow.setRotation(45 * self.position)
		scene.addItem(arrow)




def main():
	global winWidth, winHeight, scene
	app = QApplication(sys.argv)
	scene = QGraphicsScene( 0, 0, winWidth, winHeight)

	count = 0
	direction = 0
	position = random.randint(0,7)
	cordX = winWidth  / 2 + 350 * math.cos ( math.pi * position / 4)        # Target's cordinate X
	cordY = winHeight / 2 + 350 * math.sin ( math.pi * position / 4)        # Target's cordinate Y

	lay = Layout(direction, position, cordX, cordY)
	lay.SceneSet()

	view = gamewindow(scene)
	view.valueload(count, direction, position, cordX, cordY)
	view.show()
	view.raise_()
	app.exec_()




if __name__ == '__main__':
	main()
	sys.exit()
