'''
If you add some pictures to this game, make a folder in /home/the77lab/RehabGame/picture/squeegee/image/
and add pictures you want.
They are automatically loaded.
'''



import sys, cv2, os, subprocess, re, select
os.chdir("/home/mrbengutierrez/Desktop/RehabGame")

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

winHeight = 900
winWidth = 1200
scene = image = view = None
picHeight = 0
picWidth = 0
picPosX = picPosY = 0
scale = 1.0
filepath = "./picture/squeegee/image/scenery/cherry_blossoms.jpg"
title = "cherry_blossoms"

nc_cmd = 'netcat 192.168.1.12 3333'
process = subprocess.Popen(nc_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)




##-------------------------------------------
#    character setting


class Calc_Pic(QGraphicsItem):
    def __init__(self):
        super(Calc_Pic, self).__init__()
        global SqegHeight, SqegWidth, HalfWidth
        SqegHeight = 20
        SqegWidth = 70
        HalfWidth = int( SqegWidth / 2)
        self.setup()

    def setup(self):
        global filepath, path, imgCalc, imgOutput, show_Pic, picWidth, picHeight
        path = cv2.imread(filepath)
        self.imgOrigin = cv2.cvtColor(path, cv2.COLOR_BGR2HSV)        # load original image
        h, s, v = cv2.split(self.imgOrigin)                           # split into h,s,v data
        s.fill(0)                                                     # grayscale
        imgCalc = cv2.merge([h, s, v])                                # reconstruct to image data
        imgOutput = cv2.cvtColor( imgCalc, cv2.COLOR_HSV2RGB)         # output grayscale image
        picWidth = self.imgOrigin.shape[1]                            # width of image
        picHeight = self.imgOrigin.shape[0]                           # height of image
        show_Pic = QImage( imgOutput.data, picWidth, picHeight, QImage.Format_RGB888)        # create image data

    def boundingRect(self):
        return QRectF( 0, 0, self.imgOrigin.shape[1], self.imgOrigin.shape[0])

    def paint(self, painter, option, widget):
        global show_Pic
        painter.drawPixmap(0, 0, QPixmap.fromImage( show_Pic, Qt.AutoColor))        # display image

    def Wiper(self):        # coloring function
        global picPosX, picPosY, imgCalc, imgOutput, picWidth, picHeight, show_Pic, SqegWidth, HalfWidth, SqegHeight
        for i in range(SqegHeight):                    # squeegee's thickness
            drawY = picPosY + i
            if self.imgOrigin.shape[0] <= picPosY + i: # when the mouse + thickness exceeds the height of the image
                drawY = self.imgOrigin.shape[0] - 1
            for j in range(SqegWidth):                 # squeegee's width
                drawX = picPosX - HalfWidth + j
                if drawX - HalfWidth + j <= 0:         # when the mouse + thickness exceeds the width of the image (left boundary)
                    drawX = 0
                elif self.imgOrigin.shape[1] <= drawX - HalfWidth + j: # right boundary
                    drawX = self.imgOrigin.shape[1] - 1
                if imgCalc[drawY][drawX][1] == 0:      # coloring when the mouse position image is gray
                    imgCalc[drawY][drawX][1] = self.imgOrigin[drawY][drawX][1]
        imgOutput = cv2.cvtColor( imgCalc, cv2.COLOR_HSV2RGB)
        show_Pic = QImage( imgOutput.data, picWidth, picHeight, QImage.Format_RGB888)  # display image
        scene.update()




class Frame(QGraphicsItem):
    def __init__(self):
        super(Frame, self).__init__()
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setup()


class PicTitle(Frame):
    def setup(self):
        pass

    def boundingRect(self):
        return QRectF( 0, 0, 400, 200)

    def paint(self, painter, option, widget):
        global title
        painter.setFont(QFont('Norasi',30))
        painter.drawText(0, 0, str(title))


class Start(Frame):
    def setup(self):
        self.image = QImage("./picture/squeegee/layout/start.png")

    def boundingRect(self):
        return QRectF( 0, 0, self.image.width(), self.image.height())

    def paint(self, painter, option, widget):
        painter.drawImage( 0, 0, self.image)

    def mousePressEvent(self, event):
        global picWidth, picHeight, imgCalc, imgOutput, show_Pic
        h, s, v = cv2.split(imgCalc)
        s.fill(0)
        imgCalc = cv2.merge([h, s, v])
        imgOutput = cv2.cvtColor( imgCalc, cv2.COLOR_HSV2RGB)
        show_Pic = QImage( imgOutput.data, picWidth, picHeight, QImage.Format_RGB888)
        scene.update()


class Quit(Frame):
    def setup(self):
        self.image = QImage("./picture/squeegee/layout/quit.png")

    def boundingRect(self):
        return QRectF( 0, 0, self.image.width(), self.image.height())

    def paint(self, painter, option, widget):
        painter.drawImage( 0, 0, self.image)

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


class Settings(Frame):
    def setup(self):
        self.image = QImage("./picture/squeegee/layout/settings.png")

    def boundingRect(self):
        return QRectF( 0, 0, self.image.width(), self.image.height())

    def paint(self, painter, option, widget):
        painter.drawImage( 0, 0, self.image)

    def mousePressEvent(self, event):
        subWindow = SubWindow()
        subWindow.show()
        subWindow.exec_()


class SubWindow(QDialog):
    def __init__(self, parent=None):
        super(SubWindow, self).__init__(parent)
        subwinWidth  = 600
        subwinHeight = 350
        self.setGeometry(500, 300, subwinWidth, subwinHeight)
        self.setMaximumSize( subwinWidth, subwinHeight)
        self.setMinimumSize( subwinWidth, subwinHeight)
        self.setWindowTitle("Settings")

        text1 = QLabel(self)
        text1.setFont(QFont('Norasi', 15))
        text1.setText("SELECT PICTURE")
        text1.move( 170, 30)

        list1 = os.listdir("./picture/squeegee/image")
        text2 = QLabel(self)
        text2.setFont(QFont('Norasi', 12))
        text2.setText("group")
        text2.move( 80, 85)
        self.combo1 = QComboBox(self)
        self.combo1.setFont(QFont('Norasi',12))
        for num in range(len(list1)):
            self.combo1.addItem(list1[num])
        self.combo1.move( 80, 120)
        self.select = self.combo1.currentText()
        self.combo1.currentIndexChanged.connect(self.indexChanged)

        path = "./picture/squeegee/image/" + str(self.select)    # load images from this directory automatically
        self.list2 = os.listdir(path)
        text3 = QLabel(self)
        text3.setFont(QFont('Norasi', 12))
        text3.setText("picture")
        text3.move( 300, 85)
        self.combo2 = QComboBox(self)
        self.combo2.setFont(QFont('Norasi',12))
        for num in range(len(self.list2)):
            self.combo2.addItem(self.list2[num])
        self.combo2.move( 300, 120)

    def indexChanged(self):
        self.combo2.clear()
        self.select = self.combo1.currentText()
        path = "./picture/squeegee/image/" + str(self.select)    # load images from this directory automatically
        self.list2 = os.listdir(path)
        for num in range(len(self.list2)):
            self.combo2.addItem(self.list2[num])
        self.combo2.move( 300, 120)

    def closeEvent(self,event):
        global filepath, title, view
        filepath = "./picture/squeegee/image/" + self.combo1.currentText() + "/" + self.combo2.currentText()    # load images from this directory automatically
        title = self.combo2.currentText()
        title = title.rstrip('.jpg')
        scene.clear()
        lay = Layout()
        lay.SceneSet()
        view.Set()




##-------------------------------------------
#    window setting


class gamewindow(QGraphicsView, QWidget):
    def __init__( self, parent = None ):
        super(gamewindow, self).__init__(parent)
        global winWidth, winHeight, Points
        self.wx = winWidth
        self.wy = winHeight
        self.direction = 1
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
            process.stdin.write('g wrist_aa_pos\n')
        else:
            process.stdin.write('g wrist_fe_pos\n')
        poll_obj = select.poll()
        poll_obj.register(process.stdout, select.POLLIN)
        poll_result = poll_obj.poll(0)

        if(poll_result):
            line = str(process.stdout.readline()).rstrip('\n')
            if('wrist_aa_pos' in line):
                aa_pos = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                if(aa_pos < 0):
                    value_aa = float(aa_pos[1]) * 10.0
                else:
                    value_aa = float(aa_pos[1]) * 4.0
                self.cursorY = int( (winHeight / 2) - ((winHeight / 2) * value_aa))
                self.switch = - self.switch
            elif('wrist_fe_pos' in line):
                fe_pos = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                value_fe = float(fe_pos[1]) * 2.0
                self.cursorX = int( (winWidth / 2) + ((winWidth / 2) * value_fe))
                self.switch = - self.switch
        self.player.setRect(self.cursorX - int(self.R/2), self.cursorY - int(self.R/2), self.R, self.R)

    def initUI(self):
        self.setMouseTracking(True)
        self.setGeometry(250, 100, self.wx, self.wy)
        self.setMaximumSize( self.wx, self.wy)
        self.setMinimumSize( self.wx, self.wy)
        self.setWindowTitle("Squeegee")
        self.combo = QComboBox(self)
        self.combo.setFont(QFont('Norasi',20))
        self.combo.addItem("Vertical")
        self.combo.addItem("Horizontal")
        self.combo.move( 780, 20)
        self.combo.activated.connect(self.ComboChange)
        self.sp = QSpinBox(self)
        self.sp.setFont(QFont('Norasi',20))
        self.sp.setRange( 0, 10)
        self.sp.setValue(5)
        self.sp.move( 980, 20)
        self.sp.valueChanged.connect(self.ValueChange)

    def ComboChange(self):        # change the pad length and width
        global SqegHeight, SqegWidth, HalfWidth
        if ( self.combo.currentText() == 'Vertical'):
            self.direction = 1
            SqegHeight = 20
            SqegWidth = 20 + (10 * self.sp.value())
            HalfWidth = int( SqegWidth / 2)
        else:
            self.direction = 0
            SqegWidth = 20
            SqegHeight = 20 + (10 * self.sp.value())
            HalfWidth = int( SqegWidth / 2)

    def ValueChange(self):        # 
        global SqegWidth, SqegHeight, HalfWidth
        if (self.direction == 1):
            SqegWidth = 20 + (10 * self.sp.value())
            HalfWidth = int( SqegWidth / 2)
        else:
            SqegHeight = 20 + (10 * self.sp.value())
            HalfWidth = int( SqegWidth / 2)

    def Set(self):
        global picWidth, picHeight, view, Item_Pic
        windowX = view.frameGeometry().width()
        windowY = view.frameGeometry().height()
        self.ofsetX = (windowX - picWidth) / 2
        self.ofsetY = (windowY - picHeight) / 2
        Item_Pic.setPos( int(self.ofsetX), int(self.ofsetY))

    def moving(self):
        global  picPosX, picPosY, Item_Pic, scene, Points
        picPosX = int(self.cursorX - self.ofsetX)
        picPosY = int(self.cursorY - self.ofsetY)

        if ((0 <= picPosX) and (picPosX < picWidth)):
             if ((0 <= picPosY) and (picPosY < picHeight)):
                Item_Pic.Wiper()




class Layout:
    def SceneSet(self):
        global scene, Item_Pic

        pb = QGraphicsPixmapItem(QPixmap('./picture/squeegee/layout/pb.png'))
        pb.setPos( 0, 0)
        scene.addItem(pb)

        frame = QGraphicsPixmapItem(QPixmap('./picture/squeegee/layout/frame.png'))
        frame.setPos( 30, 20)
        frame.setTransform(QTransform.fromScale(0.8, 0.8), True)
        scene.addItem(frame)
        settings = Settings()
        settings.setPos( 300, 28)
        settings.setTransform(QTransform.fromScale(0.9, 0.9), True)
        scene.addItem(settings)
        start = Start()
        start.setPos( 180, 23)
        start.setTransform(QTransform.fromScale(0.9, 0.9), True)
        scene.addItem(start)
        quit = Quit()
        quit.setPos( 50, 30)
        scene.addItem(quit)

        Item_Pic = Calc_Pic()
        Item_Pic.setPos(100, 100)
        Item_Pic.setTransform(QTransform.fromScale(1.0, 1.0), True)
        scene.addItem(Item_Pic)

        pictitle = PicTitle()
        pictitle.setPos(800,110)
        scene.addItem(pictitle)




def main():
    global scene, winWidth, winHeight, view
    app = QApplication(sys.argv)
    scene = QGraphicsScene(0, 0, winWidth, winHeight)

    lay = Layout()
    lay.SceneSet()

    view = gamewindow(scene)
    view.show()
    view.raise_()
    view.Set()
    app.exec_()




##-------------------------------------------
#    game setting

if __name__== '__main__':
    main()
    sys.exit()
