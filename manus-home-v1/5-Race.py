import sys, math, random, subprocess, re, select
import os
os.chdir("../rehab-games")

import NanotecLibrary as NT # import python library to control nanotec motors


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

winWidth = 1300
winHeight = 900

scene = view = None
Item_bar = [0 for i in range(2)]
Item_gate = [0 for i in range(2)]
Item_indicator = [0 for i in range(2)]
border = [0 for i in range(2)]

RectStart = RectEnd = 0
GateSize = 5

nc_cmd = 'netcat 192.168.1.12 3333'
process = subprocess.Popen(nc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)




#---------------------------------------------------------------
# character setting

class Flame(QGraphicsItem):
	def __init__(self):
		super(Flame, self).__init__()
		self.setup()


class rect1(Flame):
	def setup(self):
		self.SC1 = 0    # select color rect 1
		self.Color = [ Qt.red, Qt.blue, Qt.green, Qt.yellow, Qt.magenta]

	def boundingRect(self):
		return QRectF(0, -5, 800, 35)

	def get_color(self, color):
		self.SC1 = color

	def paint(self, painter, option, widget):
		painter.setPen(QPen(self.Color[self.SC1], 1))
		painter.setBrush(self.Color[self.SC1])
		painter.drawRect(0, 0, 800, 30)


class rect2(Flame):
	def setup(self):
		self.SC2 = 1    # select color rect 2
		self.Color = [ Qt.red, Qt.blue, Qt.green, Qt.yellow, Qt.magenta]

	def boundingRect(self):
		return QRectF(0, -5, 800, 35)

	def get_color(self, color):
		self.SC2 = color

	def paint(self, painter, option, widget):
		painter.setPen(QPen(self.Color[self.SC2], 1))
		painter.setBrush(self.Color[self.SC2])
		painter.drawRect(0, 0, 800, 30)


class Player(Flame):
	def setup(self):
		pass

	def boundingRect(self):
		return QRectF( 0, 0, 30, 80)

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.yellow, 1))
		painter.setBrush(Qt.yellow)
		painter.drawEllipse(0, 0, 30, 80)


class Border(Flame):
	def setup(self):
		pass

	def boundingRect(self):
		return QRectF(0, 0, 800, 50)

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.darkGray, 1))
		painter.setBrush(Qt.darkGray)
		painter.drawRect(0, 0, 800, 50)


class Gate(Flame):
	def setup(self):
		pass

	def boundingRect(self):
		return QRectF( -85, -5, 85, 35)

	def paint(self, painter, option, widget):
		global GateSize
		painter.setPen(QPen(Qt.gray, 1))
		painter.setBrush(Qt.gray)
		painter.drawRect( - (GateSize * 5) -35, 0, (GateSize * 10) + 70, 30)


class lead_triangle(Flame):
	def setup(self):
		self.deg = 0
		self.tri = 20
		self.ofsetx = -12

	def boundingRect(self):
		return QRectF(self.ofsetx, 0, self.tri * 2, self.tri * 2)

	def load_deg(self, deg):
		self.deg = deg

	def paint(self, painter, option, widget):
		painter.setPen(QPen(QColor( 240, 240, 240), 1))
		painter.setBrush(QColor( 240, 240, 240))
		self.pgn = QPolygonF()
		for i in range(3):
			x = self.tri * math.cos(math.radians(120*i + self.deg))
			y = self.tri * math.sin(math.radians(120*i + self.deg))
			self.pgn.append(QPointF(self.tri + self.ofsetx + x, self.tri + y))
		painter.drawPolygon(self.pgn)


class lead_rect(Flame):
	def setup(self):
		pass

	def boundingRect(self):
		return QRectF(0, -5, abs(RectStart - RectEnd), 15)

	def paint(self, painter, option, widget):
		global RectStart, RectEnd
		painter.setPen(QPen(QColor( 240, 240, 240), 1))
		painter.setBrush(QColor( 240, 240, 240))
		painter.drawRect(0, 0, abs(RectStart - RectEnd), 10)


class Text(Flame):
	def setup(self):
		pass

	def boundingRect(self):
		return QRectF(0, 0, 300, 800)

	def paint(self, painter, option, widget):
		painter.setPen(Qt.black)
		painter.setFont(QFont('Norasi',20))
		painter.drawText( 50,  60, str("- START -"))
		painter.drawText( 50, 160, str("- RESET -"))
		painter.drawText( 60, 260, str("- STOP -"))
		painter.drawText( 65, 360, str("- QUIT -"))
		painter.drawText( 60, 570, str("Direction"))
		painter.drawText( 60, 690, str("Gate Width"))
		painter.drawText( 70, 790, str("Trial"))
		painter.setFont(QFont('Norasi',14))
		painter.drawText( 90,  90, str("Z key"))
		painter.drawText( 90, 190, str("X key"))
		painter.drawText( 70, 290, str("Space key"))
		painter.drawText( 90, 390, str("C key"))




class Score(QGraphicsItem):
	def __init__(self):
		super(Score, self).__init__()
		self.text = "{0:2d}".format(0)
		self.score = 0
		self.trial = 30

	def load_score(self, score):
		self.score = score

	def load_text(self, count):
		self.text = "{0:2d}".format(count)

	def load_trial(self, trial):
		self.trial = trial

	def boundingRect(self):
		return QRectF(0, 0, 300, 600)

	def paint(self, painter, option, widget):
		painter.setPen(Qt.red)
		painter.setFont(QFont('Norasi',32))
		painter.drawText( 0, 0, str("SCORE"))
		painter.setPen(Qt.black)
		painter.setFont(QFont('Norasi', 40))
		painter.drawText( 30, 70, "{0:4d}".format(self.score))
		painter.setPen(Qt.red)
		painter.setFont(QFont('Norasi',32))
		painter.drawText( 10, 250, str("TRIAL"))
		painter.setPen(Qt.black)
		painter.setFont(QFont('Norasi', 40))
		painter.drawText( 20, 320, self.text + "/" + "{0}".format(self.trial))




#---------------------------------------------------------------
# drawing


class gamewindow(QGraphicsView, QWidget):
	def __init__( self, parent = None ):
		super(gamewindow, self).__init__(parent)
		self.setup()
		self.initValue()
		self.resetValue()
		self.initUI()
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

		timer2 = QTimer(self)
		timer2.timeout.connect(self.moving)     # game action
		timer2.start(10)

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

	def setup(self):
		global winWidth, winHeight
		self.setGeometry(250, 100, winWidth, winHeight)
		self.setMaximumSize(winWidth, winHeight)
		self.setMinimumSize(winWidth, winHeight)
		self.setWindowTitle("Race")
		self.setMouseTracking(False)
		timer = QTimer(self)
		timer.timeout.connect(self.Line_Move)
		timer.start(1)

	def initValue(self):
		global winWidth, winHeight
		self.trial = 30            # trial number
		self.state = 0             # state = 1 means game playing, state = 0 means game stopped

		self.gsp = 0               # gate start position

		self.gamespeed = 30        # game speed
		self.terminal = winHeight  # edge
		self.mouseX = 0            # current mouse cursor X
		self.mouseY = 0            # current mouse cursor Y
		self.timing = 0            # Synchronize wih computer cycle
		self.move1 = 440           # initial position of bar 1
		self.move2 = 0             # initial position of bar 2
		self.step = 4              # the speed of bar falling
		self.turn = 1              # switch target bars
		self.gap = int( (winWidth - 800) / 2)    # the width from left edge to center square
		self.PlayerPosX = winWidth / 2        # player icon position
		self.PlayerPosY = winHeight - 180     # player icon position

	def resetValue(self):
		self.SC1 = 0               # Select Color rect 1
		self.SC2 = 1               # Select Color rect 2
		self.score = 0             # score
		self.count = 0             # count

	def initUI(self):
		self.combo = QComboBox(self)
		self.combo.setFont(QFont('Norasi',20))
		self.combo.addItem("Vertical")
		self.combo.addItem("Horizontal")
		self.combo.move( 40, 580)
		self.combo.activated.connect(self.ComboChange)

		self.sp1 = QSpinBox(self)
		self.sp1.setFont(QFont('Norasi',20))
		self.sp1.setRange( 0, 10)
		self.sp1.setValue(5)
		self.sp1.move( 120, 700)
		self.sp1.valueChanged.connect(self.ValueChange1)
		self.sp2 = QSpinBox(self)
		self.sp2.setFont(QFont('Norasi',20))
		self.sp2.setRange( 1, 50)
		self.sp2.setValue(30)
		self.sp2.move( 120, 800)
		self.sp2.valueChanged.connect(self.ValueChange2)

	def ComboChange(self):
		global direction, Item_score
		self.state = 0
		self.setMouseTracking(False)

		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setWindowTitle("Attention")
		msg.setText("Reset")
		msg.setStandardButtons(QMessageBox.Ok)
		ret = msg.exec_()
		if ret == QMessageBox.Ok:    # initialize related to mode change (vertical, horizontal)

			if ( self.combo.currentText() == 'Vertical'):
				direction = 1
				self.PlayerPosX = winWidth / 2
				self.PlayerPosY = winHeight - 180
				self.move1 = 440
				self.move2 = 0
			else:
				direction = 0
				self.PlayerPosX = self.gap + 180
				self.PlayerPosY = winHeight / 2
				self.move1 = 1050 - 440
				self.move2 = 1050
			self.resetValue()

			scene.clear()
			lay = Layout()
			lay.SceneSet()
			Item_score.load_text(self.trial)

	def ValueChange1(self):
		global GateSize
		GateSize = self.sp1.value()

	def ValueChange2(self):
		self.trial = self.sp2.value()

	def Line_Move(self):
		global direction
		if (self.state== 1):           # whether game playing of not
			self.timing += 1
			if (self.timing % self.gamespeed == 0):
				if (direction == 1):
					self.Vertical()    # calling vertical mode
				else:
					self.Horizontal()  # calling horizontal mode

	def Vertical(self):
		global scene, Gate1x, Gate2x, RectStart, RectEnd, winHeight, GateSize
		global Item_bar, Item_score, Item_indicator, Item_gate
		posSet = PosSetting(Gate1x, Gate2x, self.turn)
		initpos = 0                         # position for generating gate
		self.terminal1 = winHeight - 140    # position to score judgement
		self.terminal2 = winHeight - 40     # decide the end point of the flowing bar

		self.move1 += self.step
		self.move2 += self.step

		if (self.turn == 1):                # here switch target bars
			judgePos1 = self.move1
			judgePos2 = self.move2
			judgeGate = Gate1x
		else:
			judgePos1 = self.move2
			judgePos2 = self.move1
			judgeGate = Gate2x

		if ( self.terminal1 < judgePos1):            # stop calculate until the bar goes near the bottom end
			if (judgePos1 < self.terminal1 + 10):    # near the bottom end
				# whether the cursor is within gate width
				if (judgeGate - 35 - (GateSize * 5) < self.mouseX) and (self.mouseX < judgeGate + ( 35 + (GateSize * 5) - 30)):
					self.score += 10
					self.count += 1
				else:
					self.score -= 10
					self.count += 1
				self.turn = - self.turn              # switch targt bars
				posSet.lead()                        # .lead() and .Deg() decide lead arrow's direction
				self.deg, self.gsp = posSet.Deg()
				Item_indicator[0].load_deg(self.deg)
				Item_indicator[0].setPos( self.gsp + 60 - ((GateSize * 5) + 35), winHeight - 95)
				Item_indicator[1].setPos( RectStart + 60 - ((GateSize * 5) + 35), winHeight - 80)  # set arrow
				Item_score.load_score(self.score)        # show score
				scene.update()

		if (self.terminal2 < judgePos2):             # at same time, another bar goes to the edge and will recreate
			if (self.turn == 1):                     # switch target bars
				self.move2 = initpos                 # initial position
				self.SC2 = (self.SC2 + 2) % 5        # recoloring
				Gate2x = posSet.Setting()            # decide new Gate2's x cordinate
				Item_bar[1].get_color(self.SC2)      # reflect color change
			else:
				self.move1 = initpos
				self.SC1 = (self.SC1 + 2) % 5
				Gate1x = posSet.Setting()
				Item_bar[0].get_color(self.SC1)
			scene.update()

		Item_score.load_text(self.count)             # show trial number
		Item_bar[0].setPos( self.gap, self.move1)    # set each bars and gates
		Item_gate[0].setPos(  Gate1x, self.move1)
		Item_bar[1].setPos( self.gap, self.move2)
		Item_gate[1].setPos(  Gate2x, self.move2)

		if (self.count == self.trial):               # stop the game if count number reach trial number 
			self.state = 0                           # stop the game
			self.setMouseTracking(False)

	def Horizontal(self):    # almost same as vertical
		global scene, Gate1x, Gate2x, RectStart, RectEnd, winHeight, GateSize
		global Item_bar, Item_score, Item_indicator, Item_gate
		posSet = PosSetting(Gate1x, Gate2x, self.turn)
		initpos = 1050
		self.terminal1 = self.gap + 90
		self.terminal2 = self.gap - 10
		self.move1 -= self.step
		self.move2 -= self.step
		if (self.turn == 1):
			judgePos1 = self.move1
			judgePos2 = self.move2
			judgeGate = Gate1x
		else:
			judgePos1 = self.move2
			judgePos2 = self.move1
			judgeGate = Gate2x

		if (judgePos1 < self.terminal1):
			if (self.terminal1 - 10 < judgePos1):
				if (judgeGate - 35 - (GateSize * 5) < self.mouseY) and (self.mouseY < judgeGate + ( 35 + (GateSize * 5) - 30)):
					self.score += 10
					self.count += 1
				else:
					self.score -= 10
					self.count += 1
				self.turn = - self.turn
				posSet.lead()
				self.deg, self.gsp = posSet.Deg()
				Item_indicator[0].load_deg(self.deg)
				Item_indicator[0].setPos( self.gap + 95, self.gsp + 60 - ((GateSize * 5) + 35))
				Item_indicator[1].setPos( self.gap + 80, RectStart + 60 - ((GateSize * 5) + 35))
				Item_score.load_score(self.score)
				scene.update()

		if (judgePos2 < self.terminal2):
			if (self.turn == 1):
				self.move2 = initpos
				self.SC2 = (self.SC2 + 2) % 5
				Gate2x = posSet.Setting()
				Item_bar[1].get_color(self.SC2)
			else:
				self.move1 = initpos
				self.SC1 = (self.SC1 + 2) % 5
				Gate1x = posSet.Setting()
				Item_bar[0].get_color(self.SC1)
			scene.update()

		Item_score.load_text(self.count)
		Item_bar[0].setPos(  self.move1,     53)
		Item_gate[0].setPos( self.move1, Gate1x)
		Item_bar[1].setPos(  self.move2,     53)
		Item_gate[1].setPos( self.move2, Gate2x)

		if (self.count == self.trial):
			self.state = 0
			self.setMouseTracking(False)

	def moving(self):
		global Item_player1, Item_player2, direction
		self.mouseX = self.cursorX
		self.mouseY = self.cursorY
		if (direction == 1):
			if self.mouseX < self.gap:    # move player character in vertical mode
				Item_player1.setPos( 250     , self.PlayerPosY)          # behavior when arriving at the edge
				Item_player2.setPos( 250 - 13, self.PlayerPosY)
			elif winWidth -self.gap - 30 < self.mouseX:
				Item_player1.setPos( 1050 - 30     , self.PlayerPosY)    # behavior when arriving at the edge
				Item_player2.setPos( 1050 - 30 - 13, self.PlayerPosY)
			else:
				Item_player1.setPos( self.mouseX     , self.PlayerPosY)
				Item_player2.setPos( self.mouseX - 13, self.PlayerPosY)
		else:
			if self.mouseY < 50:          # move player character in horizontal mode
				Item_player1.setPos( self.PlayerPosX, 50     )
				Item_player2.setPos( self.PlayerPosX, 50 - 13)
			elif 850 - 30 < self.mouseY:
				Item_player1.setPos( self.PlayerPosX, 850 - 30     )
				Item_player2.setPos( self.PlayerPosX, 850 - 30 - 13)
			else:
				Item_player1.setPos( self.PlayerPosX, self.mouseY     )
				Item_player2.setPos( self.PlayerPosX, self.mouseY - 13)

	def keyPressEvent(self, hoge):
		global scene
		if hoge.key() == Qt.Key_Z:          # start game
			self.state = 1
			self.setMouseTracking(True)

		elif hoge.key() == Qt.Key_X:        # reset
			global direction, Item_score
			self.state = 0
			self.setMouseTracking(False)

			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setWindowTitle("Attention")
			msg.setText("Reset ?")
			msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
			ret = msg.exec_()
			if ret == QMessageBox.Yes:

				scene.clear()
				if (direction == 1):
					self.move1 = 440
					self.move2 = 0
				else:
					self.move1 = 1050 - 440
					self.move2 = 1050
				self.resetValue()
				lay = Layout()
				lay.SceneSet()
				Item_score.load_trial(self.trial)

			elif ret == QMessageBox.No:
				self.close

		elif hoge.key() == Qt.Key_Space:    # game stop
			self.state = 0
			self.setMouseTracking(False)

		elif hoge.key() == Qt.Key_C:
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




class PosSetting:
	def __init__(self, gate1, gate2, turn):        # read data for calculation
		self.CordinalteX = 0
		self.gate1 = gate1
		self.gate2 = gate2
		self.turn = turn

	def Setting(self):
		global GateSize, direction
		if (direction == 1):
			gate = 250
		else:
			gate = 0
		qsrand(QTime(0, 0, 0).secsTo(QTime.currentTime()))
		value = random.randint( 0, 800 - ((GateSize * 10) + 70))    # decide the next position consiering current gate size
		self.CordinateX = value + (gate + (GateSize + 35))   # decide the next gate position considering the space betwwwn game stage and window
		return self.CordinateX

	def lead(self):
		global RectStart, RectEnd
		if self.gate1 <= self.gate2:   # identify the larger cordinate value compare with previous gate cordinate
			RectStart = self.gate1
			RectEnd = self.gate2
		else:
			RectStart = self.gate2
			RectEnd = self.gate1

	def Deg(self):
		global RectStart, RectEnd
		if self.turn == 1:                # when turn = 1, next generate gate is gate1
			print("1")
			if self.gate1 < self.gate2:
				self.deg = 0              # facing right (down)
				self.gsp = RectEnd        # gate start position
			else:
				self.deg = 180            # facing left (upper)
				self.gsp = RectStart

		else:                             # gate2 will recreate
			print("2")
			if self.gate1 < self.gate2:
				self.deg = 180
				self.gsp = RectStart
			else:
				self.deg = 0
				self.gsp = RectEnd
		return(self.deg, self.gsp)




class Layout:
	def __init__( self, parent = None ):
		global Gate1x, Gate2x, winWidth
		posSet = PosSetting(0,0,0)
		Gate1x = posSet.Setting()
		Gate2x = posSet.Setting()
		posSet = PosSetting((winWidth / 2) - 60, Gate1x, 1)
		posSet.lead()
		self.deg, self.gsp = posSet.Deg()

	def SceneSet(self):
		global scene, Gate1x, Gate2x, winWidth, winHeight, RectStart, direction, GateSize
		Func = [("rect1", "rect2"), ("Gate", "Gate"), ("lead_triangle", "lead_rect")]
		gap = int( (winWidth - 800) / 2)
		if (direction == 1):
			angle = 0.0
			InitPosX = winWidth / 2
			InitPosY = winHeight - 180
			iniPos = [( gap, 440, Gate1x, 440), ( gap, 0, Gate2x, 0)]
			borderpos = [( gap, 0), ( gap, 850)]
			IndicatorPos = [ ( self.gsp + 60 - ( (GateSize * 5) + 35), winHeight - 95), (RectStart + 60 - ( (GateSize * 5) + 35), winHeight - 80)]
		else:
			angle = 90.0
			InitPosX = gap + 180
			InitPosY = winHeight / 2
			iniPos = [( 1050 - 440, 53, 1050 - 440, Gate1x), ( 1050, 53, 1050, Gate2x)]
			borderpos = [( winWidth - gap + 50, 53), ( gap, 53)]
			IndicatorPos = [ ( gap + 95, self.gsp + 60 - ( (GateSize * 5) + 35)), ( gap + 80, self.gsp + 60 - ( (GateSize * 5) + 35))]

		BGPic = QGraphicsPixmapItem(QPixmap('./picture/race/earth.jpg'))
		BGPic.setTransform(QTransform.fromScale( 1.45, 1.78), True)
		BGPic.setPos( 0, 0)
		scene.addItem(BGPic)

		scale1 = 0.8
		field = QGraphicsPixmapItem(QPixmap('./picture/race/field.png'))
		field.setTransform(QTransform.fromScale( scale1, scale1), True)
		field.setPos( 247, 50)
		scene.addItem(field)

		global Item_bar, Item_gate
		for num in range(2):
			Item_bar[num] = eval(Func[0][num])()
			Item_bar[num].setPos( iniPos[num][0], iniPos[num][1])
			Item_bar[num].setRotation(angle)
			scene.addItem(Item_bar[num])
			Item_gate[num] = eval(Func[1][num])()
			Item_gate[num].setPos( iniPos[num][2], iniPos[num][3])
			Item_gate[num].setRotation(angle)
			scene.addItem(Item_gate[num])

		for num in range(2):
			border[num] = Border()
			border[num].setPos( borderpos[num][0], borderpos[num][1])
			border[num].setRotation(angle)
			scene.addItem(border[num])
			Item_indicator[num] = eval(Func[2][num])()
			Item_indicator[num].setPos( IndicatorPos[num][0], IndicatorPos[num][1])
			Item_indicator[num].setRotation(angle)
			scene.addItem(Item_indicator[num])

		Item_indicator[0].load_deg(self.deg)

		menu = QGraphicsPixmapItem(QPixmap('./picture/race/menuframe.png'))
		menu.setTransform(QTransform.fromScale( 0.9, 0.8), True)
		menu.setPos( 20, 10)
		scene.addItem(menu)
		frameScore = QGraphicsPixmapItem(QPixmap('./picture/race/frame.png'))
		frameScore.setTransform(QTransform.fromScale( 1.0, 1.0), True)
		frameScore.setPos( 1060, 50)
		scene.addItem(frameScore)
		frameTrial = QGraphicsPixmapItem(QPixmap('./picture/race/frame.png'))
		frameTrial.setTransform(QTransform.fromScale( 1.0, 1.0), True)
		frameTrial.setPos( 1060, 300)
		scene.addItem(frameTrial)

		global Item_player1
		Item_player1 = Player()
		Item_player1.setPos( InitPosX, InitPosY)
		Item_player1.setRotation(angle)
		scene.addItem(Item_player1)

		global Item_player2
		scale2 = 0.25
		Item_player2 = QGraphicsPixmapItem(QPixmap('./picture/race/shuttle.png'))
		Item_player2.setTransform(QTransform.fromScale( scale2, scale2), True)
		if (direction == 1):
			Item_player2.setPos( InitPosX - 13, InitPosY)
		else:
			Item_player2.setPos( InitPosX, InitPosY - 13)
		Item_player2.setRotation(angle)
		scene.addItem(Item_player2)

		global Item_score        # item score
		Item_score = Score()
		Item_score.setPos( 1100, 120)
		scene.addItem(Item_score)
		text = Text()
		text.setPos( 0, 0)
		scene.addItem(text)




#---------------------------------------------------------------
# main function


def main():
	global winWidth, winHeight, scene, direction
	app = QApplication(sys.argv)
	scene = QGraphicsScene(0, 0, winWidth, winHeight)
	direction = 1

	lay = Layout()
	lay.SceneSet()

	view = gamewindow(scene)
	view.show()
	view.raise_()
	app.exec_()




if __name__== '__main__':
	main()
	sys.exit()
