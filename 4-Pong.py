import sys, math, subprocess, re, select
import os
os.chdir("/home/mrbengutierrez/Desktop/RehabGame")

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

winWidth = 1300
winHeight = 900

scene = None


wall   = [0 for i in range(4)]
player = [0 for i in range(4)]
Wall       = ["Wall_left",  "Wall_right", "Wall_upper", "Wall_lower"]
Wall_Pos   = [   (250,50),     (1000,50),     (300,50),    (300,800)]
Player     = ["Plyaer_left", "Plyaer_right", "Plyaer_upper", "Plyaer_lower"]
Player_Pos = [    (330,360),      (920,360),      (560,130),      (560,720)]

nc_cmd = 'netcat 192.168.1.12 3333'
process = subprocess.Popen(nc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)




#---------------------------------------------------------------
# character setting


class Flame(QGraphicsItem):
    def __init__(self):
        super(Flame, self).__init__()
        self.paddle_width = 180

    def load_paddle_width(self, width):
        self.paddle_width = width


class Wall_left(Flame):
    def boundingRect(self):
        return QRectF( 0, 0, 50, 800)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(QColor( 237, 125, 49), 1))
        painter.setBrush(QColor( 237, 125, 49))
        painter.drawRect( 0, 0, 50, 800)


class Wall_right(Flame):
    def boundingRect(self):
        return QRectF( 0, 0, 50, 800)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(QColor( 0, 176, 80), 1))
        painter.setBrush(QColor( 0, 176, 80))
        painter.drawRect( 0, 0, 50, 800)


class Wall_upper(Flame):
    def boundingRect(self):
        return QRectF( 0, 0, 700,  50)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(QColor( 255, 192, 0), 1))
        painter.setBrush(QColor( 255, 192, 0))
        painter.drawRect( 0, 0, 700,  50)


class Wall_lower(Flame):
    def boundingRect(self):
        return QRectF( 0, 0, 700,  50)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(QColor( 143, 170, 220), 1))
        painter.setBrush(QColor( 143, 170, 220))
        painter.drawRect( 0, 0, 700,  50)


class Plyaer_left(Flame):
    def boundingRect(self):
        return QRectF( 0, 0, 50, 230)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(QColor( 237, 125, 49), 1))
        painter.setBrush(QColor( 237, 125, 49))
        painter.drawRect( 0, 0, 50, self.paddle_width)


class Plyaer_right(Flame):
    def boundingRect(self):
        return QRectF( 0, 0, 50, 230)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(QColor( 0, 176, 80), 1))
        painter.setBrush(QColor( 0, 176, 80))
        painter.drawRect( 0, 0, 50, self.paddle_width)


class Plyaer_upper(Flame):
    def boundingRect(self):
        return QRectF( 0, 0, 230,  50)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(QColor( 255, 192, 0), 1))
        painter.setBrush(QColor( 255, 192, 0))
        painter.drawRect( 0, 0, self.paddle_width, 50)


class Plyaer_lower(Flame):
    def boundingRect(self):
        return QRectF( 0, 0, 230,  50)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(QColor( 143, 170, 220), 1))
        painter.setBrush(QColor( 143, 170, 220))
        painter.drawRect( 0, 0, self.paddle_width, 50)


class Score(QGraphicsItem):
    def __init__(self):
        super(Score, self).__init__()
        self.total = 30
        self.trial = 0
        self.score = 0

    def load_value(self, trial, score):
        self.trial = trial
        self.score = score

    def load_total(self, total):
        self.total = total

    def boundingRect(self):
        global winWidth, winHeight
        return QRectF(0, 0, 300, 600)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.red)
        painter.setFont(QFont('Norasi',32))
        painter.drawText(  0,   0, str("SCORE"))
        painter.setPen(Qt.black)
        painter.setFont(QFont('Norasi', 40))
        painter.drawText( 30,  70, "{0:4d}".format(self.score))
        painter.setPen(Qt.red)
        painter.setFont(QFont('Norasi',32))
        painter.drawText( 10, 250, str("TRIAL"))
        painter.setPen(Qt.black)
        painter.setFont(QFont('Norasi', 40))
        painter.drawText( 30, 320, "{0:2d}".format(self.trial) + "/" + "{0:2d}".format(self.total))




class Center_Pic(QGraphicsItem):
    def __init__(self):
        super(Center_Pic, self).__init__()
        self.image = QImage("./picture/pong/center.png")
    def boundingRect(self):
        return QRectF( - (self.image.width() / 2), - (self.image.height() / 2), self.image.width(), self.image.height())
    def paint(self, painter, option, widget):
        painter.drawImage(  - (self.image.width() / 2), - (self.image.height() / 2), self.image)




class Text(Flame):
    def boundingRect(self):
        global winWidth, winHeight
        return QRectF(0, 0, 300, 800)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.black)
        painter.setFont(QFont('Norasi',20))
        painter.drawText( 50,  60, str("- START -"))
        painter.drawText( 50, 160, str("- RESET -"))
        painter.drawText( 60, 260, str("- STOP -"))
        painter.drawText( 65, 360, str("- QUIT -"))
        painter.drawText( 60, 580, str("Ball Speed"))
        painter.drawText( 55, 700, str("Paddle Width"))
        painter.setFont(QFont('Norasi',14))
        painter.drawText( 90,  90, str("Z key"))
        painter.drawText( 90, 190, str("X key"))
        painter.drawText( 70, 290, str("Space key"))
        painter.drawText( 90, 390, str("C key"))




class Marker(QGraphicsItem):
    def __init__(self):
        super(Marker, self).__init__()
        self.image = QImage("./picture/pong/target.png")
    def boundingRect(self):
        return QRectF( - ( self.image.width() / 2), - ( self.image.height() / 2), self.image.width(), self.image.height())
    def paint(self, painter, option, widget):
        painter.drawImage(  - ( self.image.width() / 2), - ( self.image.height() / 2), self.image)




#---------------------------------------------------------------
# drawing

class gamewindow(QGraphicsView, QWidget):
    def __init__( self, parent = None ):
        super(gamewindow, self).__init__(parent)
        self.initGlobalValue()
        self.initValue()
        self.initButton()
        self.initUI()
        self.ManusSetting()

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
            process.stdin.write('g wrist_aa_pos\n')    # command for load wrist_aa_pos value
        else:
            process.stdin.write('g wrist_fe_pos\n')    # command for load wrist_fe_pos value
        poll_obj = select.poll()
        poll_obj.register(process.stdout, select.POLLIN)
        poll_result = poll_obj.poll(0)

        if(poll_result):
            line = str(process.stdout.readline()).rstrip('\n')    # remove \n from inmorted values
            if('wrist_aa_pos' in line):
                aa_pos = re.findall(r'[-+]?\d*\.\d+|\d+', line)   # translate string to float
                if(aa_pos < 0):
                    value_aa = float(aa_pos[1]) * 10.0            # scaling
                else:
                    value_aa = float(aa_pos[1]) * 4.0             # scaling
                self.cursorY = int( (winHeight / 2) - ((winHeight / 2) * value_aa))
                self.switch = - self.switch
            elif('wrist_fe_pos' in line):
                fe_pos = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                value_fe = float(fe_pos[1]) * 2.0
                self.cursorX = int( (winWidth / 2) + ((winWidth / 2) * value_fe))
                self.switch = - self.switch
        self.player.setRect(self.cursorX - int(self.R/2), self.cursorY - int(self.R/2), self.R, self.R)    # show player cursor

    def initGlobalValue(self):
        global targetON, N, S, E, W
        targetON = 0
        N = S = E = W = 1

    def initValue(self):
        self.mouseX = 0                  # current mouse x coordinate
        self.mouseY = 0                  # current mouse y coordinate
        self.x = winWidth / 2            # current x coordinate
        self.y = winHeight / 2           # current y coordinate
        self.r = 50                      # ball radius
        self.stepx = 4                   # ball x step
        self.stepy = 3                   # ball y step
        self.preX = self.x
        self.preY = self.y
        self.sec = 0                     # for hit animation
        self.trigger = 0                 # for hit animation
        self.timing = 0                  # Synchronize wih computer cycle
        self.hit = 0                     # to judge which wall was hit
        self.hit_continue = 0            # hit animation is continue while this value = 1
        self.preHitpos = 0               # to avoid duplicate processing when hitting the same place
        self.playing = 0                 # this value = 1 means game playing ( = 0 means game stopping)
        self.gamespeed = 30              # game speed
        self.left_border = 300           # outer frame left border
        self.right_border = 1000         # outer frame right border
        self.upper_border = 100          # outer frame upper border
        self.lower_border = 800          # outer frame lower border
        self.TargetPosChange = 1         # target cursor position change (if this value = 1)
        self.score = 0                   # score
        self.trial = 0                   # trial number
        self.total = 30                  # total number
        self.paddle_width = 180          # paddle width

    def load_total(self, total):
        self.total = total

    def initButton(self):
        self.sp1 = QSpinBox(self)
        self.sp1.setFont(QFont('Norasi',20))
        self.sp1.setRange( 0, 10)
        self.sp1.setValue(5)
        self.sp1.move( 120, 600)
        self.sp1.valueChanged.connect(self.ValueChange1)

        self.sp2 = QSpinBox(self)
        self.sp2.setFont(QFont('Norasi',20))
        self.sp2.setRange( 0, 10)
        self.sp2.setValue(5)
        self.sp2.move( 120, 720)
        self.sp2.valueChanged.connect(self.ValueChange2)

        other = QPushButton("  OTHERS  ",self)
        other.move( 40, 800)
        other.setFont(QFont('Norasi',20))
        other.setStyleSheet("background-color:rgb( 237, 125, 49); color:rgb( 255, 255, 255)");
        other.clicked.connect(self.OtherClick)

    def ValueChange1(self):
        self.gamespeed = 55 - (5 * self.sp1.value())

    def ValueChange2(self):
        global scene, player
        self.paddle_width = 130 + (10 * self.sp2.value())
        for num in range(4):
            player[num].load_paddle_width(self.paddle_width)
        scene.update()

    def OtherClick(self):
        self.playing = 0
        self.setMouseTracking(False)
        subWindow = SubWindow()
        subWindow.load_total_value(self.total)
        subWindow.show()
        subWindow.exec_()

    def initUI(self):
        global winWidth, winHeight, scene
        self.setGeometry(250, 100, winWidth, winHeight)
        self.setMaximumSize(winWidth, winHeight)
        self.setMinimumSize(winWidth, winHeight)
        self.setWindowTitle("Pong")
        self.setMouseTracking(False)

        pen   = QPen(QColor('dodgerblue'))
        brush = QBrush(pen.color())
        self.dot = scene.addEllipse(self.x, self.y, self.r, self.r, pen, brush)
        timer = QTimer(self)
        timer.timeout.connect(self.dot_move)
        timer.start(1)

    def dot_move(self):        # bellow dot move control
        global Item_score, Item_mark, targetON, W, E, N, S
        if (self.playing == 1):

            if (targetON == 1):                                            # whether target cursor assist function is on or not
                if (self.TargetPosChange == 1):                            # below target cursor position change
                    if (self.stepx > 0):                                   # when the ball is going to right side
                        step1 = (self.right_border - self.x) / self.stepx
                        if (self.stepy > 0):                               # the ball is going to upper side
                            step2 = (self.lower_border - self.y) / self.stepy
                        else:                                              # the ball is going to down side
                            step2 = (self.upper_border - self.y) / self.stepy
                        if (step1 <= step2):                               # which side is faster to reach
                            targetX = self.x + self.stepx * step1
                            targetY = self.y + self.stepy * step1
                        else:
                            targetX = self.x + self.stepx * step2
                            targetY = self.y + self.stepy * step2
                    else:                                                  # when the ball is going to left side
                        step1 = (self.left_border - self.x) / self.stepx
                        if (self.stepy > 0):
                            step2 = (self.lower_border - self.y) / self.stepy
                        else:
                            step2 = (self.upper_border - self.y) / self.stepy
                        if (step1 <= step2):
                            targetX = self.x + self.stepx * step1
                            targetY = self.y + self.stepy * step1
                        else:
                            targetX = self.x + self.stepx * step2
                            targetY = self.y + self.stepy * step2
                    Item_mark.setPos( targetX, targetY)
                    self.TargetPosChange = 0
            else:
                Item_mark.setPos( -50, -50)         # target cursor set

            self.timing += 1
            if (self.hit_continue == 1):            # whether hit action will continue or not
                self.Hit_Action()
            if (self.timing % self.gamespeed == 0):
                a = (self.left_border - self.r < self.x - self.r)    # judgement of left side
                b = (self.x + self.r < self.right_border)            # right side
                c = (self.upper_border - self.r < self.y - self.r)   # upper side
                d = (self.y + self.r < self.lower_border)            # down side
                if (a and b) and (c and d):                          # the ball is in the outer frame
                    e = (self.mouseY - ((self.paddle_width / 2) + self.r) < self.y)    # whether the paddle and ball are at the same height
                    f = (self.y < self.mouseY + (self.paddle_width / 2))               # same
                    if e and f:
                        if (self.x < 330 + 50):            # about leftside paddle
                            if (W == 1):
                                if (self.preHitpos != 1):
                                    self.score += 10
                                    self.trial += 1
                                    self.TargetPosChange = 1
                                self.preHitpos = 1
                                if (self.y < self.preY - ((self.paddle_width / 2) + self.r)):  # when the ball hit to upper side of paddle
                                    self.stepy = - abs(self.stepy)
                                elif (self.preY + (self.paddle_width / 2) < self.y):           # when the ball hit to lower side of paddle
                                    self.stepy = abs(self.stepy)
                                else:
                                    self.stepx = abs(self.stepx)                               # the ball hit to right side
                        elif (870 + 50 < self.x + self.r): # situation of right side
                            if (E == 1):
                                if (self.preHitpos != 2):
                                    self.score += 10
                                    self.trial += 1
                                    self.TargetPosChange = 1
                                self.preHitpos = 2
                                if (self.y < self.preY - ((self.paddle_width / 2) + self.r)):
                                    self.stepy = - abs(self.stepy)
                                elif (self.preY + (self.paddle_width / 2) < self.y):
                                    self.stepy = abs(self.stepy)
                                else:
                                    self.stepx = - abs(self.stepx)
                    g = (self.mouseX - ((self.paddle_width / 2) + self.r) + 50 < self.x)
                    h = (self.x < self.mouseX + (self.paddle_width / 2) + 50)
                    if g and h:
                        if (self.y < 180):
                            if (N == 1):
                                if self.preHitpos != 3:
                                    self.score += 10
                                    self.trial += 1
                                    self.TargetPosChange = 1
                                self.preHitpos = 3
                                if (self.x < self.preX - ((self.paddle_width / 2) + self.r) + 50):
                                    self.stepx = - abs(self.stepx)
                                elif (self.preX + (self.paddle_width / 2) + 50 < self.x):
                                    self.stepx = abs(self.stepx)
                                else:
                                    self.stepy = abs(self.stepy)
                        elif (720 < self.y + self.r):
                            if (S == 1):
                                if (self.preHitpos != 4):
                                    self.score += 10
                                    self.trial += 1
                                    self.TargetPosChange = 1
                                self.preHitpos = 4
                                if (self.x < self.preX - ((self.paddle_width / 2) + self.r)):
                                    self.stepx = - abs(self.stepx)
                                elif (self.preX + (self.paddle_width / 2) < self.x):
                                    self.stepx = abs(self.stepx)
                                else:
                                    self.stepy = - abs(self.stepy)
                else:        # when the ball goes to outside of outer frame
                    self.TargetPosChange = 1
                    if (self.x - self.r < 250 + 50 - 30):    # leftside
                        self.stepx = abs( self.stepx)
                        if (W == 1):
                            self.hit = 0
                            self.hit_continue = 1
                            self.trigger = 1
                            self.score -= 20
                            self.trial += 1
                    elif (950 + 50 - 10 < self.x + self.r):  # tight side
                        self.stepx = - abs( self.stepx)
                        if (E == 1):
                            self.hit = 1
                            self.hit_continue = 1
                            self.trigger = 1
                            self.score -= 20
                            self.trial += 1
                    if (self.y - self.r < 100 - 30):         # upper side
                        self.stepy = abs( self.stepy)
                        if (N == 1):
                            self.hit = 2
                            self.hit_continue = 1
                            self.trigger = 1
                            self.score -= 20
                            self.trial += 1
                    elif (950 - 150 < self.y + self.r):      # lower side
                        self.stepy = - abs( self.stepy)
                        if (S == 1):
                            self.hit = 3
                            self.hit_continue = 1
                            self.trigger = 1
                            self.score -= 20
                            self.trial += 1
                self.x += self.stepx
                self.y += self.stepy
                self.dot.setRect( self.x, self.y, self.r, self.r)
                self.preX = self.mouseX
                self.preY = self.mouseY
                Item_score.load_value(self.trial, self.score)
                Item_score.load_total(self.total)
                if ( self.trial == self.total):
                    self.playing = 0
                    self.setMouseTracking(False)
                scene.update()

    def moving(self):
        global player, W, E, N, S    # paddle will not move when uncheck the checkbox in settings ( W,E,N and S become 0)
        self.mouseX = self.cursorX
        self.mouseY = self.cursorY
        if (W == 1):
            player[0].setPos( 280 + 50, self.mouseY - (self.paddle_width / 2))
        if (E == 1):
            player[1].setPos( 870 + 50, self.mouseY - (self.paddle_width / 2))
        if (N == 1):
            player[2].setPos( self.mouseX - (self.paddle_width / 2) + 50, 130)
        if (S == 1):
            player[3].setPos( self.mouseX - (self.paddle_width / 2) + 50, 720)

    def Hit_Action(self):        # vibration the wall
        global wall, Wall_Pos
        if self.trigger == 1:
            self.sec = 0
            self.trigger = 0
        self.sec += 1
        if self.hit <= 1:
            if self.sec < 10:
                wall[self.hit].setPos( Wall_Pos[self.hit][0] - 15, Wall_Pos[self.hit][1])
            elif self.sec < 20:
                wall[self.hit].setPos( Wall_Pos[self.hit][0] + 15, Wall_Pos[self.hit][1])
            elif self.sec < 30:
                wall[self.hit].setPos( Wall_Pos[self.hit][0] - 15, Wall_Pos[self.hit][1])
            elif self.sec < 40:
                wall[self.hit].setPos( Wall_Pos[self.hit][0] + 15, Wall_Pos[self.hit][1])
            else:
                wall[self.hit].setPos( Wall_Pos[self.hit][0], Wall_Pos[self.hit][1])
                self.hit_continue = 0
        else:
            if self.sec < 10:
                wall[self.hit].setPos( Wall_Pos[self.hit][0], Wall_Pos[self.hit][1] - 15)
            elif self.sec < 20:
                wall[self.hit].setPos( Wall_Pos[self.hit][0], Wall_Pos[self.hit][1] + 15)
            elif self.sec < 30:
                wall[self.hit].setPos( Wall_Pos[self.hit][0], Wall_Pos[self.hit][1] - 15)
            elif self.sec < 40:
                wall[self.hit].setPos( Wall_Pos[self.hit][0], Wall_Pos[self.hit][1] + 15)
            else:
                wall[self.hit].setPos( Wall_Pos[self.hit][0], Wall_Pos[self.hit][1])
                self.hit_continue = 0

    def keyPressEvent(self, hoge):
        global scene
        if hoge.key() == Qt.Key_Z:          # game start
            self.playing = 1
            self.setMouseTracking(True)

        elif hoge.key() == Qt.Key_X:        # reset
            self.playing = 0
            self.setMouseTracking(False)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Attention")
            msg.setText("Reset ?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            ret = msg.exec_()
            if ret == QMessageBox.Yes:

                global W, E, N, S, player, Item_score
                self.x = winWidth / 2
                self.y = winHeight / 2
                scene.clear()
                lay = Layout()
                lay.SceneSet()
                if (W == 0):
                    scene.removeItem(player[0])
                if (E == 0):
                    scene.removeItem(player[1])
                if (N == 0):
                    scene.removeItem(player[2])
                if (S == 0):
                    scene.removeItem(player[3])
                self.score = 0
                self.trial = 0
                Item_score.load_value(self.trial, self.score)
                self.paddle_width = 130 + (10 * self.sp2.value())
                for num in range(4):
                    player[num].load_paddle_width(self.paddle_width)
                pen   = QPen(QColor('dodgerblue'))
                brush = QBrush(pen.color())
                self.dot = scene.addEllipse(self.x, self.y, self.r, self.r, pen, brush)

            elif ret == QMessageBox.No:
                self.close

        elif hoge.key() == Qt.Key_Space:    # game stop
            self.playing = 0
            self.setMouseTracking(False)

        elif hoge.key() == Qt.Key_C:        # game close
            self.playing = 0
            self.setMouseTracking(False)
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




class SubWindow(QDialog):                # setting window
    def __init__(self, parent=None):
        super(SubWindow, self).__init__(parent)
        subwinWidth  = 600
        subwinHeight = 350
        self.setGeometry(500, 300, subwinWidth, subwinHeight)
        self.setMaximumSize( subwinWidth, subwinHeight)
        self.setMinimumSize( subwinWidth, subwinHeight)
        self.setWindowTitle("Others")

        text1 = QLabel(self)
        text1.setFont(QFont('Norasi', 20))
        text1.setText("OTHER SETTINGS")
        text1.move( 170, 20)

        text2 = QLabel(self)
        text2.setFont(QFont('Norasi', 20))
        text2.setText("Trial")
        text2.move( 100, 100)
        self.sp = QSpinBox(self)
        self.sp.setFont(QFont('Norasi',20))
        self.sp.setRange( 0, 50)
        self.sp.setValue(0)
        self.sp.move( 90, 140)
        self.sp.valueChanged.connect(self.ValueChange)

        text3 = QLabel(self)
        text3.setFont(QFont('Norasi', 20))
        text3.setText("Paddle")
        text3.move( 380, 100)
        self.W = QCheckBox('W', self)
        self.W.move( 370, 200)
        if (W == 1):
            self.W.toggle()
        self.W.stateChanged.connect(self.W_clicked)
        self.E = QCheckBox('E', self)
        self.E.move( 470, 200)
        if (E == 1):
            self.E.toggle()
        self.E.stateChanged.connect(self.E_clicked)
        self.N = QCheckBox('N', self)
        self.N.move( 420, 150)
        if (N == 1):
            self.N.toggle()
        self.N.stateChanged.connect(self.N_clicked)
        self.S = QCheckBox('S', self)
        self.S.move( 420, 250)
        if (S == 1):
            self.S.toggle()
        self.S.stateChanged.connect(self.S_clicked)

        text4 = QLabel(self)
        text4.setFont(QFont('Norasi', 20))
        text4.setText("Target")
        text4.move( 80, 220)
        self.combo = QComboBox(self)
        self.combo.setFont(QFont('Norasi',15))
        if (targetON == 0):
            self.combo.addItem("off")
            self.combo.addItem("on")
        else:
            self.combo.addItem("on")
            self.combo.addItem("off")
        self.combo.move( 90, 260)
        self.combo.activated.connect(self.Marker_switch)

    def load_total_value(self, total):
        self.total = total
        self.sp.setValue(self.total)

    def ValueChange(self):
        global view, Item_score
        self.total = self.sp.value()
        Item_score.load_total(self.total)
        view.load_total(self.total)

    def W_clicked(self):
        global W, scene, player, Player, Player_Pos
        if (self.W.isChecked()):
            W = 1
            player[0] = eval( Player[0])()
            player[0].setPos( Player_Pos[0][0], Player_Pos[0][1])
            scene.addItem(player[0])
        else:
            W = 0
            scene.removeItem(player[0])

    def E_clicked(self):
        global E, scene, player, Player, Player_Pos
        if (self.E.isChecked()):
            E = 1
            player[1] = eval( Player[1])()
            player[1].setPos( Player_Pos[1][0], Player_Pos[1][1])
            scene.addItem(player[1])
        else:
            E = 0
            scene.removeItem(player[1])

    def N_clicked(self):
        global N, scene, player, Player, Player_Pos
        if (self.N.isChecked()):
            N = 1
            player[2] = eval( Player[2])()
            player[2].setPos( Player_Pos[2][0], Player_Pos[2][1])
            scene.addItem(player[2])
        else:
            N = 0
            scene.removeItem(player[2])

    def S_clicked(self):
        global S, scene, player, Player, Player_Pos
        if (self.S.isChecked()):
            S = 1
            player[3] = eval( Player[3])()
            player[3].setPos( Player_Pos[3][0], Player_Pos[3][1])
            scene.addItem(player[3])
        else:
            S = 0
            scene.removeItem(player[3])

    def Marker_switch(self):
        global targetON
        if ( self.combo.currentText() == 'on'):
            targetON = 1
        else:
            targetON = 0




class Layout:
    def __init__( self, parent = None ):
        pass

    def SceneSet(self):
        global scene, winWidth, winHeight

        BGPic = QGraphicsPixmapItem(QPixmap('./picture/pong/flooring.png'))
        BGPic.setTransform(QTransform.fromScale( 1.45, 1.5), True)
        BGPic.setPos( 0, 0)
        scene.addItem(BGPic)

        center = Center_Pic()
        center.setTransform(QTransform.fromScale( 0.8, 0.8), True)
        center.setPos( winWidth / 2, winHeight / 2)
        scene.addItem(center)

        menu = QGraphicsPixmapItem(QPixmap('./picture/pong/menuframe.png'))
        menu.setTransform(QTransform.fromScale( 0.9, 0.8), True)
        menu.setPos( 20, 10)
        scene.addItem(menu)

        frameScore = QGraphicsPixmapItem(QPixmap('./picture/pong/frame.png'))
        frameScore.setTransform(QTransform.fromScale( 1.0, 1.0), True)
        frameScore.setPos( 1060, 50)
        scene.addItem(frameScore)

        frameTrial = QGraphicsPixmapItem(QPixmap('./picture/pong/frame.png'))
        frameTrial.setTransform(QTransform.fromScale( 1.0, 1.0), True)
        frameTrial.setPos( 1060, 300)
        scene.addItem(frameTrial)

        global Item_score
        Item_score = Score()
        Item_score.setPos( 1100, 120)
        scene.addItem(Item_score)

        text = Text()
        text.setPos( 0, 0)
        scene.addItem(text)

        global wall, Wall, Wall_Pos
        for num in range(4):
            wall[num] = eval( Wall[num])()
            wall[num].setPos( Wall_Pos[num][0], Wall_Pos[num][1])
            scene.addItem(wall[num])

        global player, Player, Player_Pos
        for num in range(4):
            player[num] = eval( Player[num])()
            player[num].setPos( Player_Pos[num][0], Player_Pos[num][1])
            scene.addItem(player[num])

        global Item_mark
        Item_mark = Marker()
        Item_mark.setTransform(QTransform.fromScale( 0.8, 0.8), True)
        Item_mark.setPos( -50, -50)
        scene.addItem(Item_mark)




#---------------------------------------------------------------
# main function


def main():
    global scene
    app = QApplication(sys.argv)
    scene = QGraphicsScene(0, 0, winWidth, winHeight)

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
