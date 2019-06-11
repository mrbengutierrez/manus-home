import sys, time, datetime, csv, subprocess, re, select
import os
os.chdir("/home/mrbengutierrez/Desktop/RehabGame")

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

winWidth = 1300
winHeight = 900

nc_cmd = 'netcat 192.168.1.12 3333'
process = subprocess.Popen(nc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)




#---------------------------------------------------------------
# character setting


class Maze(QGraphicsItem):            # make maze
    def __init__(self, posX, posY):
        super(Maze, self).__init__()
        self.PosX = posX                                  # start point cordinate of and end point cordinalte of each rect about X
        self.PosY = posY                                  # start point cordinate of and end point cordinalte of each rect about Y
        self.trial = 0                                    # record how many targets player has reached
        self.clear = 0                                    # whether game cleared or not (1 mean game cleared)
        self.cR = [ 240, 255, 255,  51,  51, 204, 255]    # color red
        self.cG = [   0, 153, 255, 153, 102, 153, 153]    # color green
        self.cB = [   0,   0,   0, 102, 255, 255, 204]    # color blue

    def LoadValue(self, trial, clear, cleartime):
        self.trial = trial                   # load current trial number
        self.clear = clear                   # load current clear number
        self.cleartime = cleartime           # load the time when player clear this game

    def boundingRect(self):
        global winWidth, winHeight
        return QRectF( 0, 0, winWidth, winHeight)

    def paint(self, painter, option, widget):
        global scene

        self.x = 0
        self.y = 0
        self.count = 0
        self.line = 0
        # the processing while game is not cleared
        if self.clear == 0:
            while self.y < 19:
                # fill rect with color until not reached rect
                if self.x + self.y < self.trial:
                    painter.setPen  (QColor( self.cR[self.count % 7], self.cG[self.count % 7], self.cB[self.count % 7]))
                    painter.setBrush(QColor( self.cR[self.count % 7], self.cG[self.count % 7], self.cB[self.count % 7]))
                    # change color
                    self.count += 1
                else:
                    # fill rect with gray color that has not acheved
                    painter.setPen(QColor( 169, 169, 169))
                    painter.setBrush(QColor( 169, 169, 169))
                # whether next drowing line is horizontal or not
                # drawing horizontal line (self.line = 0)
                if self.line == 0:
                    # change start point and end point depend on each cordinate
                    if self.PosX[self.x] > self.PosX[self.x + 1]:
                        painter.drawRect( self.PosX[self.x + 1], self.PosY[self.y], self.PosX[self.x]     - self.PosX[self.x + 1] + 35, 35)
                    else:
                        painter.drawRect( self.PosX[self.x],     self.PosY[self.y], self.PosX[self.x + 1] - self.PosX[self.x]     + 35, 35)
                    self.x += 1
                    self.line = 1
                # drawing vertical line (self.line = 1)
                else:
                    if self.PosY[self.y] > self.PosY[self.y + 1]:
                        painter.drawRect( self.PosX[self.x], self.PosY[self.y + 1], 35, self.PosY[self.y] - self.PosY[self.y + 1] + 35)
                    else:
                        painter.drawRect( self.PosX[self.x], self.PosY[self.y], 35, self.PosY[self.y + 1] - self.PosY[self.y] + 35)
                    self.y += 1
                    self.line = 0
        # the processing after game was cleared
        else:
            while self.y < 19:
                # change color depend on time
                set = ((int(time.time() - self.cleartime)) + self.count) % 7
                painter.setPen(QColor( self.cR[set], self.cG[set], self.cB[set]))
                painter.setBrush(QColor( self.cR[set], self.cG[set], self.cB[set]))
                self.count += 1
                if self.line == 0:
                    if self.PosX[self.x] > self.PosX[self.x + 1]:
                        painter.drawRect( self.PosX[self.x + 1], self.PosY[self.y], self.PosX[self.x] - self.PosX[self.x + 1] + 35, 35)
                    else:
                        painter.drawRect( self.PosX[self.x], self.PosY[self.y], self.PosX[self.x + 1] - self.PosX[self.x] + 35, 35)
                    self.x += 1
                    self.line = 1
                else:
                    if self.PosY[self.y] > self.PosY[self.y + 1]:
                        painter.drawRect( self.PosX[self.x], self.PosY[self.y + 1], 35, self.PosY[self.y] - self.PosY[self.y + 1] + 35)
                    else:
                        painter.drawRect( self.PosX[self.x], self.PosY[self.y], 35, self.PosY[self.y + 1] - self.PosY[self.y] + 35)
                    self.y += 1
                    self.line = 0
        scene.update()




class Text(QGraphicsItem):        # text setting
    def __init__(self):
        super(Text, self).__init__()

    def boundingRect(self):
        return QRectF(0, 0, 300, 500)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.red)
        painter.setFont(QFont('Norasi',20))
        painter.drawText(  0,   0, "High Score")
        painter.setFont(QFont('Norasi',25))
        painter.drawText( 30, 180, "YOU")




class Score(QGraphicsItem):              # score text setting
    def __init__(self, highscore):       # load high score and text setting
        super(Score, self).__init__()
        self.playtime = 0
        self.highscore = highscore

        millisec1 = self.highscore % 100        # convert value to time
        second1 = (self.highscore / 100) % 60
        minute1 = (self.highscore / 100) / 60
        MS1 = "{0:02d}".format(int(millisec1))
        S1  = "{0:02d}".format(int(second1))
        M1  = "{0:02d}".format(int(minute1))
        self.text1 = M1 + ":" + S1 + ":" + MS1

    def boundingRect(self):
        return QRectF(0, 0, 300, 400)

    def LoadPlaytime(self, playtime):    # load current play time
        self.playtime = playtime

    def paint(self, painter, option, widget):    # print current play time
        millisec2 = self.playtime % 100
        second2 = (self.playtime / 100) % 60
        minute2 = (self.playtime / 100) / 60
        MS2 = "{0:02d}".format(int(millisec2))
        S2  = "{0:02d}".format(int(second2))
        M2  = "{0:02d}".format(int(minute2))
        self.text2 = M2 + ":" + S2 + ":" + MS2

        painter.setPen(Qt.black)
        painter.setFont(QFont('Norasi', 25))
        painter.drawText( 0,   0, self.text1)
        painter.drawText( 0, 170, self.text2)




#---------------------------------------------------------------
# drawing main window


class gamewindow(QGraphicsView):
    def __init__( self, parent = None ):
        super(gamewindow, self).__init__(parent)
        global winWidth, winHeight
        self.setGeometry(250, 100, winWidth, winHeight)
        self.setMaximumSize(winWidth, winHeight)
        self.setMinimumSize(winWidth, winHeight)
        self.setWindowTitle("Maze")
        self.setMouseTracking(False)
        self.circleX = 0          # next target's position
        self.circleY = 0          # next target's position
        self.playing = 0          # whether this game is running or not
        self.cleartime = 0        # the value for color change
        self.playtime = 0         # current playing time
        self.clear = 0            # flag of game was cleared or not
        self.trial = 0            # record how many targets player has reached
        self.initUI()
        self.initTimer()
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

    def LoadValue(self, posX, posY, scorelist, highscore):
        self.PosX = posX                 # start point cordinate of and end point cordinalte of each rect about X
        self.PosY = posY                 # start point cordinate of and end point cordinalte of each rect about Y
        self.scorelist = scorelist       # for recording high score
        self.highscore = highscore       # highscore

    def initUI(self):                             # button settings
        quit = QPushButton("   QUIT    ", self)   # quit button
        quit.move( 40, 60)
        quit.setFont(QFont('Norasi',18))
        quit.setStyleSheet("background-color:rgb( 255, 98, 50); color:rgb( 255, 255, 255)");
        quit.clicked.connect(self.QuitClick)
        start = QPushButton("  START  ", self)    # start button
        start.move( 40, 130)
        start.setFont(QFont('Norasi',18))
        start.setStyleSheet("background-color:rgb( 40, 175, 12); color:rgb( 255, 255, 255)");
        start.clicked.connect(self.StartClick)
        stop = QPushButton("   STOP   ", self)    # stop button
        stop.move( 40, 200)
        stop.setFont(QFont('Norasi',18))
        stop.setStyleSheet("background-color:rgb( 80, 77, 203); color:rgb( 255, 255, 255)");
        stop.clicked.connect(self.StopClick)

    def initTimer(self):                 # play time count
        timer = QTimer(self)
        timer.timeout.connect(self.TimeCount)
        timer.start(100)                 # TimeCount function is called every 100 milli seconds

    def TimeCount(self):                 # play time count up
        global score
        if (self.playing == 1):
            self.playtime += 10
            score.LoadPlaytime(self.playtime)

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

    def StartClick(self):           # function after pressing start button
        global scene, lay
        if (self.clear == 1):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Attention")
            msg.setText("Restart this game ?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            ret = msg.exec_()
            if ret == QMessageBox.Yes:        # initialize all variables
                self.trial = 0
                self.clear = 0
                scene.clear()
                lay.SceneSet()
                self.circleX = 0
                self.circleY = 0
                self.playtime = 0
                self.setMouseTracking(False)
            elif ret == QMessageBox.No:
                self.close
        else:
            self.playing = 1
            self.setMouseTracking(True)

    def StopClick(self):            # function after pressing stop button
        self.playing = 0            # count up stop
        self.setMouseTracking(False)

    def moving(self):
        global scene, maze, target
        mouseX = self.cursorX
        mouseY = self.cursorY

        # whether this game was already cleared or not
        if self.clear == 0:
            # judgement of whether mouse cursor is reach next target
            if (mouseX - self.PosX[self.circleX] - 15) ** 2 + (mouseY - self.PosY[self.circleY] - 20) ** 2 < 30 ** 2:
                self.trial += 1
                if self.trial % 2 == 1:
                    if self.circleX == 19:
                        self.clear = 1
                        self.cleartime = time.time() - 1
                    else:
                        self.circleX += 1
                else:
                    self.circleY += 1
                maze.LoadValue(self.trial, self.clear, self.cleartime)
            target.setPos( self.PosX[self.circleX] - 20, self.PosY[self.circleY] - 20)
            scene.update()
        else:
            # if already cleared this game, stop the count up function and report highscore
            self.playing = 0
            if (self.playtime < self.highscore):
                self.scorelist[ int(self.scorelist[0][7]) ][2] = self.playtime
                f = open('patientID.csv', 'w')
                writer = csv.writer(f)
                writer.writerows(self.scorelist)
                f.close()




class Layout:
    def __init__( self, posX, posY, highscore):
        self.PosX = posX
        self.PosY = posY
        self.highscore = highscore

    def SceneSet(self):
        global winWidth, winHeight, scene

        BGPic = QGraphicsPixmapItem(QPixmap('./picture/maze/court.png'))
        BGPic.setTransform(QTransform.fromScale( 0.857, 0.79), True)
        BGPic.setPos( 0, 0)
        scene.addItem(BGPic)

        player = QGraphicsPixmapItem(QPixmap('./picture/maze/player.png'))
        player.setTransform(QTransform.fromScale( 0.28, 0.28), True)
        player.setPos( 1100, 470)
        scene.addItem(player)

        frame1 = QGraphicsPixmapItem(QPixmap('./picture/maze/frame.png'))
        frame1.setTransform(QTransform.fromScale( 0.8, 0.8), True)
        frame1.setPos( 1090, 30)
        scene.addItem(frame1)

        frame2 = QGraphicsPixmapItem(QPixmap('./picture/maze/frame.png'))
        frame2.setTransform(QTransform.fromScale( 0.8, 0.8), True)
        frame2.setPos( 1090, 200)
        scene.addItem(frame2)

        text = Text()
        text.setPos(1120, 80)
        scene.addItem(text)

        global score
        score = Score(self.highscore)
        score.setPos( 1130, 140)
        scene.addItem(score)

        global maze
        maze = Maze(self.PosX, self.PosY)
        maze.setPos( 0, 0)
        scene.addItem(maze)

        goal = QGraphicsPixmapItem(QPixmap('./picture/maze/goal.png'))
        goal.setTransform(QTransform.fromScale( 1.1, 1.1), True)
        goal.setPos( 580, 400)
        scene.addItem(goal)

        global target
        scale = 0.2
        target = QGraphicsPixmapItem(QPixmap('./picture/maze/ball.png'))
        target.setPos( self.PosX[0] - 20, self.PosY[0] - 20)
        target.setTransform(QTransform.fromScale( scale, scale), True)
        scene.addItem(target)




#---------------------------------------------------------------
# main function


def main():
    global winWidth, winHeight, scene
    app = QApplication(sys.argv)
    scene = QGraphicsScene( 0, 0, winWidth, winHeight)

    ofsetX = 133
    cordX = [ 75,435,195,795,555,855,135,375, 75,915,495,735,255,435,555,615,375,315,675,495, 75]
    posX = [ num + ofsetX for num in cordX]
    ofsetY = -13
    cordY = [865,685,145,745,805, 85,745,805, 25,865,685,205,625,385,565,325,565,265,625,445,865]
    posY = [ num + ofsetY for num in cordY]

    f = open("patientID.csv", "r")        # csv file loading
    Reader = csv.reader(f)
    scorelist = [ e for e in Reader]
    f.close()
    highscore = int( scorelist[ int(scorelist[0][7]) ][2])

    global lay
    lay = Layout(posX, posY, highscore)
    lay.SceneSet()

    view = gamewindow(scene)
    view.LoadValue(posX, posY, scorelist, highscore)
    view.show()
    view.raise_()
    app.exec_()




if __name__ == '__main__':
    main()
    sys.exit()
