from operator import itemgetter

import cv2
import winsound
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import pyttsx3
import sys
import data_base
import datetime
from PyQt5.QtGui import QTextCursor

flag2 = True


def check_eyes(gender, volume):
    eye_cascPath = r'haarcascade_eye_tree_eyeglasses.xml'  # eye detect model
    face_cascPath = r'haarcascade_frontalface_alt.xml'  # face detect model
    faceCascade = cv2.CascadeClassifier(face_cascPath)
    eyeCascade = cv2.CascadeClassifier(eye_cascPath)
    flag = False
    cap = cv2.VideoCapture(0)
    while flag2:
        ret, img = cap.read()
        if ret:
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect faces in the image
            faces = faceCascade.detectMultiScale(
                frame,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                # flags = cv2.CV_HAAR_SCALE_IMAGE
            )
            # print("Found {0} faces!".format(len(faces)))
            if len(faces) > 0:
                #   choose the closest face
                persons = [(x, y, w, h, w * h) for (x, y, w, h) in faces]
                #  Draw a rectangle around the faces
                (x, y, w, h) = max(persons, key=itemgetter(4))[:-1]
                # Draw a rectangle around the faces

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame_tmp = img[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1, :]
                frame = frame[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1]
                eyes = eyeCascade.detectMultiScale(
                    frame,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    # flags = cv2.CV_HAAR_SCALE_IMAGE
                )
                if len(eyes) == 0:
                    flag += 1
                    print('no')
                    if flag > 7:
                        frequency = 2500  # Set Frequency To 2500 Hertz
                        duration = 1000  # Set Duration To 1000 ms == 1 second
                        winsound.Beep(frequency, duration)
                        speak(gender, volume, "hey, wake up")
                        flag = 0
                else:
                    flag = 0
                    print('yes')
                frame_tmp = cv2.resize(frame_tmp, (400, 400), interpolation=cv2.INTER_LINEAR)
                cv2.imshow('Face Recognition', frame_tmp)
            waitkey = cv2.waitKey(1)
            if waitkey == ord('q') or waitkey == ord('Q'):
                cv2.destroyAllWindows()
                break


def speak(gender, volume, text):
    converter = pyttsx3.init()
    converter.setProperty('rate', 150)
    converter.setProperty('volume', volume)
    converter.setProperty('voice', gender)
    converter.say(text)
    converter.runAndWait()


def countWarning():
    recentWarnings = []
    warningsList = data_base.get_user_data(user_id)
    d = datetime.datetime.now() - datetime.timedelta(days = 50)
    for w in warningsList:
        w = datetime.datetime.fromisoformat(w)
        if w > d:
            recentWarnings.append(w)
    return 10
    #return len(recentWarnings)


class Ui_MainWindow():
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.gender_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
        self.volume = 0.8

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(600, 270, 121, 111))
        font = QtGui.QFont()
        font.setPointSize(32)
        self.stopButton.setFont(font)
        self.stopButton.setStyleSheet("QPushButton {\n"
"    border-image: url(:/stop/stop.jpeg);\n"
"    color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 55px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
"        );\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
"        );\n"
"    }\n"
"border-image: url(:/stop/stop.jpeg);")
        self.stopButton.setText("")
        self.stopButton.setObjectName("stopButton")
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setGeometry(QtCore.QRect(430, 270, 121, 111))
        self.playButton.setStyleSheet("QPushButton {\n"
"    border-image: url(:/play/play.jpeg);\n"
"    color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 55px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
"        );\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
"        );\n"
"    }")
        self.playButton.setText("")
        self.playButton.setObjectName("playButton")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 801, 561))
        font = QtGui.QFont()
        font.setFamily("Kristen ITC")
        font.setPointSize(22)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.background.setFont(font)
        self.background.setAutoFillBackground(False)
        self.background.setStyleSheet("border-image: url(:/b_sleep/sleep_background.jpeg);\n"
"")
        self.background.setText("")
        self.background.setTextFormat(QtCore.Qt.RichText)
        self.background.setObjectName("background")
        self.welcome = QtWidgets.QLabel(self.centralwidget)
        self.welcome.setGeometry(QtCore.QRect(100, 90, 271, 91))
        font = QtGui.QFont()
        font.setFamily("Narkisim")
        font.setPointSize(41)
        font.setBold(True)
        font.setWeight(75)
        self.welcome.setFont(font)
        self.welcome.setAutoFillBackground(False)
        self.welcome.setStyleSheet("background-color: rgba(255, 255, 255, 10);\n"
"")
        self.welcome.setObjectName("welcome")
        self.volumeButton = QtWidgets.QSlider(self.centralwidget)
        self.volumeButton.setGeometry(QtCore.QRect(490, 170, 171, 31))
        self.volumeButton.setMaximum(10)
        self.volumeButton.setSingleStep(1)
        self.volumeButton.setPageStep(10)
        self.volumeButton.setOrientation(QtCore.Qt.Horizontal)
        self.volumeButton.setObjectName("volumeButton")
        self.voiceGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.voiceGroup.setGeometry(QtCore.QRect(480, 30, 301, 91))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.voiceGroup.setFont(font)
        self.voiceGroup.setObjectName("voiceGroup")
        self.femaleButton = QtWidgets.QRadioButton(self.voiceGroup)
        self.femaleButton.setGeometry(QtCore.QRect(20, 50, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.femaleButton.setFont(font)
        self.femaleButton.setObjectName("femaleButton")
        self.maleButton = QtWidgets.QRadioButton(self.voiceGroup)
        self.maleButton.setGeometry(QtCore.QRect(150, 50, 95, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.maleButton.setFont(font)
        self.maleButton.setObjectName("maleButton")
        self.volumeLable = QtWidgets.QLabel(self.centralwidget)
        self.volumeLable.setGeometry(QtCore.QRect(490, 130, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.volumeLable.setFont(font)
        self.volumeLable.setObjectName("volumeLable")
        self.statisticsButton = QtWidgets.QPushButton(self.centralwidget)
        self.statisticsButton.setGeometry(QtCore.QRect(70, 420, 111, 111))
        font = QtGui.QFont()
        font.setFamily("Narkisim")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.statisticsButton.setFont(font)
        self.statisticsButton.setStyleSheet("QPushButton {\n"
"    border: 2px solid #555;\n"
"    border-radius: 55px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;\n"
"    background-color: rgb(123, 174, 255);\n"
"    }\n"
"")
        self.statisticsButton.setObjectName("statisticsButton")
        self.background.raise_()
        self.stopButton.raise_()
        self.playButton.raise_()
        self.welcome.raise_()
        self.volumeButton.raise_()
        self.voiceGroup.raise_()
        self.volumeLable.raise_()
        self.statisticsButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.playButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
        self.maleButton.clicked.connect(self.male_voice)
        self.femaleButton.clicked.connect(self.female_voice)
        self.volumeButton.valueChanged.connect(self.valuechange)
        self.statisticsButton.clicked.connect(self.report_f)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.welcome.setText(_translate("MainWindow", "Welcome"))
        self.voiceGroup.setTitle(_translate("MainWindow", "voice gender"))
        self.femaleButton.setText(_translate("MainWindow", "female"))
        self.maleButton.setText(_translate("MainWindow", "male"))
        self.volumeLable.setText(_translate("MainWindow", "volume"))
        self.statisticsButton.setText(_translate("MainWindow", "report"))

    def start(self):
        print("start")
        speak(self.gender_voice, self.volume, "are you ready? let's go")
        check_eyes(self.gender_voice, self.volume)

    def stop(self):
        print("stop")
        flag2 = False
        waitkey = ord('q')

    def male_voice(self):
        self.gender_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"

    def female_voice(self):
        self.gender_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

    def valuechange(self):
        self.volume = float(self.volumeButton.value()/10)

    def report_f(self):
        self.report_window = QtWidgets.QMainWindow()
        self.ui_report = reportWin()
        self.ui_report.setupUi(self.report_window)
        #ui.hide()
        self.report_window.show()


class signUp(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(796, 599)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.signUpButton = QtWidgets.QPushButton(self.centralwidget)
        self.signUpButton.setGeometry(QtCore.QRect(350, 280, 101, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.signUpButton.setFont(font)
        self.signUpButton.setStyleSheet("QPushButton{\n"
"    border: 2px solid #555;\n"
"    border-radius: 15px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;\n"
"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"    }")
        self.signUpButton.setObjectName("signUpButton")
        self.lineID = QtWidgets.QLineEdit(self.centralwidget)
        self.lineID.setGeometry(QtCore.QRect(270, 210, 271, 41))
        self.lineID.setStyleSheet(" QLineEdit{\n"
"    color: rgb(255, 255, 255);\n"
"    border: 2px solid #555;\n"
"    border-radius: 20px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;\n"
"    background-color: rgb(255, 255, 255);\n"
"    }")
        self.lineID.setText("")
        self.lineID.setObjectName("lineID")
        self.lineID.setStyleSheet("color: rgb(0, 0, 0);")
        self.enterID = QtWidgets.QLabel(self.centralwidget)
        self.enterID.setGeometry(QtCore.QRect(290, 140, 231, 71))
        font = QtGui.QFont()
        font.setFamily("Narkisim")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.enterID.setFont(font)
        self.enterID.setObjectName("enterID")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 801, 581))
        self.background.setStyleSheet("border-image: url(:/b_sleep/sleep_background.jpeg);")
        self.background.setText("")
        self.background.setObjectName("background")
        self.background.raise_()
        self.signUpButton.raise_()
        self.lineID.raise_()
        self.enterID.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 796, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.signUpButton.clicked.connect(self.newWindow)

    def newWindow(self):
        new_id = str(self.lineID.text())
        data_base.create_user(new_id)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        MainWindow.hide()
        self.window.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.signUpButton.setText(_translate("MainWindow", "Sign Up"))
        self.enterID.setText(_translate("MainWindow", "Enter Your ID"))


class reportWin(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(-20, -10, 801, 551))
        self.background.setStyleSheet("border-image: url(:/b_sleep/sleep_background.jpeg);")
        self.background.setText("")
        self.background.setObjectName("background")
        self.countText = QtWidgets.QTextEdit(self.centralwidget)
        self.countText.setGeometry(QtCore.QRect(150, 20, 591, 61))
        font = QtGui.QFont()
        font.setFamily("Narkisim")
        font.setPointSize(14)
        self.countText.setFont(font)
        self.countText.setStyleSheet("QTextEdit {\n"
"    border: 2px solid #555;\n"
"    border-radius: 30px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;\n"
"    background-color: rgb(255, 255, 255);\n"
"    }\n"
"")
        self.countText.setObjectName("countText")
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(30, 410, 111, 111))
        font = QtGui.QFont()
        font.setFamily("Narkisim")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.backButton.setFont(font)
        self.backButton.setStyleSheet("QPushButton {\n"
"    border: 2px solid #555;\n"
"    border-radius: 55px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;\n"
"    background-color: rgb(123, 174, 255);\n"
"    }\n"
"")
        self.backButton.setObjectName("backButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 30, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Narkisim")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(190, 170, 521, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar::chunk {\n"
"    background-color: rgb(221, 0, 0);\n"
"}\n"
"\n"
"\n"
"QProgressBar{\n"
"text-align: center;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.progressBar.setProperty("value", 50)
        self.progressBar.setObjectName("progressBar")
        self.hoursText = QtWidgets.QTextEdit(self.centralwidget)
        self.hoursText.setGeometry(QtCore.QRect(150, 90, 591, 61))
        font = QtGui.QFont()
        font.setFamily("Narkisim")
        font.setPointSize(14)
        self.hoursText.setFont(font)
        self.hoursText.setStyleSheet("QTextEdit {\n"
"    border: 2px solid #555;\n"
"    border-radius: 30px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;\n"
"    background-color: rgb(255, 255, 255);\n"
"    }\n"
"")
        self.hoursText.setObjectName("hoursText")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #count = countWarning()
        count = 10
        s_count = "Amount warnings at the last month: " + str(count)
        self.countText.insertPlainText(s_count)
        self.countText.setEnabled(False)
        s_hour = "Problematic hour: "
        self.hoursText.insertPlainText(s_hour)
        self.hoursText.setEnabled(False)
        self.progressBar.setValue((count/30)*100)

        self.backButton.clicked.connect(self.mainWin)

    def mainWin(self):
        self.main_window = QtWidgets.QMainWindow()
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self.main_window)
        #ui.window.hide()
        self.main_window.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.countText.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Narkisim\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:7.8pt;\"><br /></p></body></html>"))
        self.backButton.setText(_translate("MainWindow", "Back"))
        self.label.setText(_translate("MainWindow", "Report"))
        self.hoursText.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Narkisim\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:7.8pt;\"><br /></p></body></html>"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    user_id = data_base.get_user_id()
    if not user_id:
        ui = signUp()
        ui.setupUi(MainWindow)
        MainWindow.show()
    else:
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()

    sys.exit(app.exec_())







