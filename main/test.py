# !/usr/bin/env python2

import sys
# import rospy
import os
import vectors
import webbrowser
import threading
import subprocess
import cv2
from subprocess import call, Popen, PIPE, check_output
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from settings import *
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

# Get the actual Script $PATH
scriptPath = str(os.getcwd())
print (scriptPath)
# Reads the XML File
xmlFile = et.parse('environment.xml')
# Find the root element from the file (in this case "environment")
root = xmlFile.getroot()
# Load the XML values from environment file
myIP = root.findtext('MY_IP')
masterIP = root.findtext('MASTER_IP')
rosMasterURI = root.findtext('ROS_MASTER_URI')
rosHostname = root.findtext('ROS_HOSTNAME')
rosNamespace = root.findtext('ROS_NAMESPACE')
address = root.findtext('TURTLEBOT_IP')
usernameClient = root.findtext('USERNAME')
passwordClient = root.findtext('PASSWORD')
portClient = root.findtext('PORT')
perspectiveLocation = root.findtext('PERSPECTIVE_LOCATION')
rosSource = root.findtext("ROS_SOURCE")
rosEtc = root.findtext('ROS_ETC_DIRECTORY')
rosRoot = root.findtext('ROS_ROOT')
# Values to Export into "~/.bashrc"
exportIP = str('ROS_IP='+myIP)
exportMasterIP = str('MASTER_IP='+myIP)
exportMasterIPURI = str('export ROS_MASTER_URI=http://$MASTER_IP:11311/')
exportRosIP = str('export ROS_IP=$MY_IP')
exportHostname = str('export ROS_HOSTNAME_IP=$MY_IP')
exportNamespace = str('export ROS_NAMESPACE='+rosNamespace)


class EmbTerminal(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmbTerminal, self).__init__(parent)
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.terminal)
        # Works also with urxvt:
        self.process.start('urxvt', ['-embed', str(int(self.winId()))])
        self.setGeometry(90, 460, 1160, 125)


class InProgress(QtWidgets.QWidget):
    def __init__(self, parent=None):
        Error = QtWidgets.QMessageBox()
        Error.setText('Sorry, in development!')
        Error.setIcon(QtWidgets.QMessageBox.Information)
        Error.setWindowTitle('Warning!')
        Error.show()
        Error.exec_()


class Homebox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        HomeInfo = QMessageBox()
        HomeInfo.setText("You're alrady in HOME")
        HomeInfo.setIcon(QMessageBox.Information)
        HomeInfo.setWindowTitle("Warning!")
        HomeInfo.show()
        HomeInfo.exec_()


class Ui_MainWindow(object):

    def UFPBClick(self):
        # Only 1 click at every 5 seconds
        self.logoButton.setDown(True)
        QTimer.singleShot(5000, lambda: self.UFPBButton.setDown(False))
        webbrowser.open('http://ppgi.ci.ufpb.br/')

    def monitoringTool(self):
        self.MonitorButton.setDown(True)
        QTimer.singleShot(5000, lambda: self.MonitorButton.setDown(False))
        MonitorCommand = 'rosrun rqt_robot_monitor rqt_robot_monitor'
        # Using Popen instead of Call because the first one don't block the process
        monitorRqtProcess = subprocess.Popen(MonitorCommand, stdout=PIPE,
                                             stdin=PIPE, shell=True)
        MonitorProcStdout = monitorRqtProcess.communicate()[0].strip()
        print (MonitorProcStdout)

    def rqtDashboardTool(self):
        self.rqtDashboardButton.setDown(True)
        QTimer.singleShot(5000, lambda: self.rqtDashboardButton.setDown(False))
        RqtCommand = 'rqt'
        # Using Popen instead of Call because the first one don't block the process
        RqtProcess = subprocess.Popen(RqtCommand, stdout=PIPE,
                                      stdin=PIPE, shell=True)
        RqtToolProcStdout = RqtProcess.communicate()[0].strip()
        print (RqtToolProcStdout)

    def rqtBagTool(self):
        self.rqtBagButton.setDown(True)
        QTimer.singleShot(5000, lambda: self.rqtBagButton.setDown(False))
        BagCommand = 'rqt_bag'
        # Using Popen instead of Call because the first one don't block the process
        BagProcess = subprocess.Popen(BagCommand, stdout=PIPE,
                                      stdin=PIPE, shell=True)
        BagProcStdout = BagProcess.communicate()[0].strip()
        print (BagProcStdout)

    def rqtConsoleTool(self):
        self.rqtConsoleButton.setDown(True)
        QTimer.singleShot(5000, lambda: self.rqtConsoleButton.setDown(False))
        rqtConsoleCommand = 'rqt_console'
        # Using Popen instead of Call because the first one don't block the process
        rqtConsoleProcess = subprocess.Popen(rqtConsoleCommand, stdout=PIPE,
                                             stdin=PIPE, shell=True)
        rqtConsoleProcStdout = rqtConsoleProcess.communicate()[0].strip()
        print (rqtConsoleProcStdout)

    def rqtLoggerTool(self):
        self.rqtLoggerButton.setDown(True)
        QTimer.singleShot(5000, lambda: self.rqtLoggerButton.setDown(False))
        rqtLoggerCommand = 'rosrun rqt_logger_level rqt_logger_level'
        # Using Popen instead of Call because the first one don't block the process
        rqtLoggerProcess = subprocess.Popen(rqtLoggerCommand, stdout=PIPE,
                                            stdin=PIPE, shell=True)
        rqtLoggerProcStdout = rqtLoggerProcess.communicate()[0].strip()
        print (rqtLoggerProcStdout)

    def rvizGraphButton(self):
        self.rvizButton.setDown(True)
        QTimer.singleShot(5000, lambda: self.rvizButton.setDown(False))
        rvizCommand = 'rviz'
        rvizProcess = subprocess.Popen(rvizCommand, stdout=PIPE,
                                       stdin=PIPE, shell=True)

    def gmappGraphButton(self):
        self.gmappButton.setDown(True)
        QTimer.singleShot(5000, lambda: self.gmappButton.setDown(False))
        gmappStartCommand = 'roslaunch turtlebot_navigation gmapping_demo.launch'
        gmappLaunchCommand = 'roslaunch turtlebot_rviz_launchers view_navigation.launch'
        gmappStartProcess = subprocess.Popen(gmappStartCommand, stdout=PIPE,
                                             stdin=PIPE, shell=True)
        gmappStartProcess = subprocess.Popen(gmappLaunchCommand, stdout=PIPE,
                                             stdin=PIPE, shell=True)

    def mainState(self):
        if (self.playButton.isChecked() is True):
            # sshStart(self)
            print('Play selecionado')
            self.playButton.setDown(True)
            QTimer.singleShot(2000, lambda: self.playButton.setDown(False))

        elif (self.stopButton.isChecked() is True):
            print('Stop selecionado')
            self.stopButton.setDown(True)
            QTimer.singleShot(5000, lambda: self.stopButton.setDown(False))

        elif (self.pauseButton.isChecked() is True):
            print('Pause selecionado')

        elif (self.JoystickButton.isChecked() is True):
            print('Joy selecionado')
            self.JoystickButton.setDown(True)
            QTimer.singleShot(5000, lambda: self.JoystickButton.setDown(False))
            joySelection = 'roslaunch turtlebot_teleop keyboard_teleop.launch'
            joyProcess = subprocess.Popen(joySelection, stdout=PIPE,
                                          stdin=PIPE, shell=True)
            joyProcStdout = joyProcess.communicate()[0].strip()
            print (joyProcStdout)

    def controlState(self):
        if (self.fuzzyControllerButton.isChecked() is True):
            print('Fuzzy selecionado')
        elif (self.mpcControllerButton.isChecked() is True):
            print('MPC selecionado')
        elif (self.gotoControllerButton.isChecked() is True):
            print('GotoXYTeta selecionado')
        elif (self.pwmButton.isChecked() is True):
            print('PWM selecionado')
        elif (self.otherControllerButton.isChecked() is True):
            print('Other Selecionado')
        elif (self.noneControllerButton.isChecked() is True):
            print('None Selecionado')

    def robotState(self):
        if (self.robotStartButton.isChecked() is True):
            print('Starting the Turtlebot...')
            self.robotStartButton.setDown(True)
            QTimer.singleShot(5000, lambda: self.robotStartButton.setDown(False))
            # For localserver use this code:
            minimalLaunch = 'roslaunch turtlebot_bringup minimal.launch '
            # kinectLaunch = 'roslaunch turtlebot_bringup 3dsensors.launch'
            # Using Popen instead of Call because the first one don't block the process
            launchProcess = subprocess.Popen(minimalLaunch, stdout=PIPE,
                                               stdin=PIPE, shell=True)
            # sensorsProcess = subprocess.Popen(kinectLaunch, stdout=PIPE,
                                              # stdin=PIPE, shell=True)
        elif (self.robotDownButton.isChecked() is True):
            print('Shutting Down the Turtlebot...')
            self.robotDownButton.setDown(True)
            QTimer.singleShot(5000, lambda: self.robotDownButton.setDown(False))
            # For localserver use this code:
            killRosNode = 'rosnode kill -a'
            killRosMaster = 'killall -9 rosmaster'
            killRosCore = 'killall -9 roscore'
            # Using Popen instead of Call because the first one don't block the process
            nodeKillProcess = subprocess.Popen(killRosNode, stdout=PIPE,
                                               stdin=PIPE, shell=True)
            masterKillProcess = subprocess.Popen(killRosMaster, stdout=PIPE,
                                                 stdin=PIPE, shell=True)
            coreKillProcess = subprocess.Popen(killRosCore, stdout=PIPE,
                                               stdin=PIPE, shell=True)

    def tools(self):
        if (self.joystickButton.isChecked() is True):
            print('Joystick Selected')
            self.joystickButton.setDown(True)
            QTimer.singleShot(5000, lambda: self.joystickButton.setDown(False))
            joystickCommand = 'rqt_remocon'
            nodeKillProcess = subprocess.Popen(joystickCommand, stdout=PIPE,
                                              stdin=PIPE, shell=True)

        elif (self.teleopButton.isChecked() is True):
            print('Teleop Selected')
            self.teleopButton.setDown(True)
            QTimer.singleShot(5000, lambda: self.teleopButton.setDown(False))
            teleopCommand = 'roslaunch turtlebot_teleop keyboard_teleop.launch'
            nodeKillProcess = subprocess.Popen(teleopCommand, stdout=PIPE,
                                                stdin=PIPE, shell=True)

    def simulationCheckbox(self, state):

        if state == QtCore.Qt.Checked:
            print('Show Simulation Selected')
            # release video capture
            self.cap = cv2.VideoCapture(0)
            # read image in BGR format
            ret, img = self.cap.read()
            image = QtGui.QImage(img, img.shape[1], img.shape[0],
                                 img.shape[1] * img.shape[2],
                                 QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(image.rgbSwapped())
            self.simulationWidget.setPixmap(pixmap)
            self.cap.release()
        else:
            print('Show Simulation Unchecked')
            self.cap.release()

    def mapCheckbox(self, state):

        if state == QtCore.Qt.Checked:
            print('Show Map Selected')
        else:
            print('Show Map Unchecked')

    def visionCheckbox(self, state):

        if state == QtCore.Qt.Checked:
            print('Show Vision Selected')
        else:
            print('Show Vision Unchecked')

    def xLcdNumber(self):
        xIntValue = float(0.0)
        return xIntValue

    def yLcdNumber(self):
        yIntValue = float(0.0)
        return yIntValue

    def velocityLcdNumber(self):
        velocityIntValue = float(0.0)
        return velocityIntValue

    def batteryLcdNumber(self):
        batteryIntValue = int(0)
        return batteryIntValue

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 600)
        self.Base = QtWidgets.QWidget(MainWindow)
        self.Base.setStyleSheet("background: #2A2E37;")
        self.Base.setObjectName("Base")
        self.logoFrame = QtWidgets.QFrame(self.Base)
        self.logoFrame.setGeometry(QtCore.QRect(0, 0, 120, 120))
        self.logoFrame.setStyleSheet("background: rgba(25, 27, 33, 0.2);\n"
                                     "image: url(:/newPrefix/LogoLaser.png);")
        self.logoFrame.setObjectName("logoFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.logoFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.lateralMenuFrame = QtWidgets.QFrame(self.Base)
        self.lateralMenuFrame.setGeometry(QtCore.QRect(0, 0, 120, 600))
        self.lateralMenuFrame.setStyleSheet("background: #313640;\n"
                                            "")
        self.lateralMenuFrame.setObjectName("lateralMenuFrame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.lateralMenuFrame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.MenuLine = QtWidgets.QFrame(self.Base)
        self.MenuLine.setGeometry(QtCore.QRect(120, 0, 2, 600))
        self.MenuLine.setStyleSheet("background: rgba(41, 63, 71, 0.75);")
        self.MenuLine.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MenuLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.MenuLine.setObjectName("MenuLine")
        # Home Button (Aba Lateral)
        self.homeButton = QtWidgets.QCommandLinkButton(self.Base)
        self.homeButton.setGeometry(QtCore.QRect(5, 200, 110, 70))
        self.homeButton.setStyleSheet("background: rgba(29, 222, 216, 0.1);\n"
                                      "color: white;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/Home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.homeButton.setIcon(icon)
        self.homeButton.setIconSize(QtCore.QSize(45, 45))
        self.homeButton.setObjectName("homeButton")
        self.homeButton.clicked.connect(Homebox)
        # Data Button (Aba Lateral)
        self.dataButton = QtWidgets.QCommandLinkButton(self.Base)
        self.dataButton.setGeometry(QtCore.QRect(5, 300, 110, 70))
        self.dataButton.setStyleSheet("background: rgba(29, 222, 216, 0.1);\n"
                                      "color: white;\n"
                                      "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/Data.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dataButton.setIcon(icon1)
        self.dataButton.setIconSize(QtCore.QSize(45, 45))
        self.dataButton.setObjectName("dataButton")
        self.dataButton.clicked.connect(InProgress)
        # Ad-Hoc Button (Aba Lateral)
        self.adhocButton = QtWidgets.QCommandLinkButton(self.Base)
        self.adhocButton.setGeometry(QtCore.QRect(5, 400, 110, 70))
        self.adhocButton.setStyleSheet("background: rgba(29, 222, 216, 0.1);\n"
                                       "color: white;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/Conection.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.adhocButton.setIcon(icon2)
        self.adhocButton.setIconSize(QtCore.QSize(45, 45))
        self.adhocButton.setObjectName("adhocButton")
        self.adhocButton.clicked.connect(InProgress)
        # Configuration Button
        self.configButton = QtWidgets.QCommandLinkButton(self.Base)
        self.configButton.setGeometry(QtCore.QRect(1070, 40, 100, 50))
        self.configButton.setStyleSheet("color: white;\n"
                                        "background: rgba(41, 63, 71, 0.75);")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/Config.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.configButton.setIcon(icon3)
        self.configButton.setIconSize(QtCore.QSize(30, 30))
        self.configButton.setObjectName("configButton")
        self.configButton.setToolTip('Configure Enviroment and System Variables')
        self.configButton.clicked.connect(settings)
        # E-mail Button
        self.mailButton = QtWidgets.QCommandLinkButton(self.Base)
        self.mailButton.setGeometry(QtCore.QRect(1180, 40, 81, 50))
        self.mailButton.setStyleSheet("color: white;\n"
                                      "background: rgba(41, 63, 71, 0.75);")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/Contact.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mailButton.setIcon(icon4)
        self.mailButton.setIconSize(QtCore.QSize(30, 30))
        self.mailButton.setObjectName("mailButton")
        self.mailButton.setToolTip('Contact the LASER Laboratory')
        self.mailButton.clicked.connect(InProgress)
        # UFPB site Button
        self.logoButton = QtWidgets.QCommandLinkButton(self.Base)
        self.logoButton.setGeometry(QtCore.QRect(10, 540, 100, 50))
        self.logoButton.setStyleSheet("color: white;\n"
                                      "font: 7pt \"Sans Serif\";\n"
                                      "background: rgba(41, 63, 71, 0.75);")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/newPrefix/Ufpb.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.logoButton.setIcon(icon5)
        self.logoButton.setIconSize(QtCore.QSize(30, 30))
        self.logoButton.setObjectName("logoButton")
        self.logoButton.setToolTip('Go to UFPB-PPGI Website')
        self.logoButton.clicked.connect(self.UFPBClick)
        # Design de Linhas
        self.SuperiorLine = QtWidgets.QFrame(self.Base)
        self.SuperiorLine.setGeometry(QtCore.QRect(121, 120, 1280, 2))
        self.SuperiorLine.setStyleSheet("background: #1DDED8;")
        self.SuperiorLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.SuperiorLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.SuperiorLine.setObjectName("SuperiorLine")
        self.InferiorLine = QtWidgets.QFrame(self.Base)
        self.InferiorLine.setGeometry(QtCore.QRect(121, 460, 1280, 2))
        self.InferiorLine.setStyleSheet("background: #1DDED8;")
        self.InferiorLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.InferiorLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.InferiorLine.setObjectName("InferiorLine")
        self.LateraLine = QtWidgets.QFrame(self.Base)
        self.LateraLine.setGeometry(QtCore.QRect(1061, 0, 2, 462))
        self.LateraLine.setStyleSheet("background: #1DDED8;")
        self.LateraLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.LateraLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.LateraLine.setObjectName("LateraLine")
        # Design de Label do Robot State
        self.robotStateLabel = QtWidgets.QFrame(self.Base)
        self.robotStateLabel.setGeometry(QtCore.QRect(1063, 122, 218, 30))
        self.robotStateLabel.setStyleSheet("background: rgba(29, 222, 216, 0.1);")
        self.robotStateLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.robotStateLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.robotStateLabel.setObjectName("robotStateLabel")
        self.robotStateTextLabel = QtWidgets.QLabel(self.robotStateLabel)
        self.robotStateTextLabel.setGeometry(QtCore.QRect(65, 9, 101, 16))
        self.robotStateTextLabel.setStyleSheet("background: transparent;\n"
                                               "font: 10pt \"Khmer OS System\";\n"
                                               "color: white;")
        self.robotStateTextLabel.setObjectName("robotStateTextLabel")
        # Design de Label do Simulation
        self.simulationLabel = QtWidgets.QFrame(self.Base)
        self.simulationLabel.setGeometry(QtCore.QRect(1063, 240, 218, 30))
        self.simulationLabel.setStyleSheet("background: rgba(29, 222, 216, 0.1);")
        self.simulationLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.simulationLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.simulationLabel.setObjectName("simulationLabel")
        self.simulationTextLabel = QtWidgets.QLabel(self.simulationLabel)
        self.simulationTextLabel.setGeometry(QtCore.QRect(75, 9, 81, 16))
        self.simulationTextLabel.setStyleSheet("background: transparent;\n"
                                               "font: 9pt \"Khmer OS System\";\n"
                                               "color: white;")
        self.simulationTextLabel.setObjectName("simulationTextLabel")
        # Design de Label do Tools
        self.toolsLabel = QtWidgets.QFrame(self.Base)
        self.toolsLabel.setGeometry(QtCore.QRect(1063, 360, 218, 30))
        self.toolsLabel.setStyleSheet("background: rgba(29, 222, 216, 0.1);")
        self.toolsLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.toolsLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.toolsLabel.setObjectName("toolsLabel")
        self.toolsTextLabel = QtWidgets.QLabel(self.toolsLabel)
        self.toolsTextLabel.setGeometry(QtCore.QRect(90, 9, 51, 16))
        self.toolsTextLabel.setStyleSheet("background: transparent;\n"
                                          "font: 9pt \"Khmer OS System\";\n"
                                          "color: white;")
        self.toolsTextLabel.setObjectName("toolsTextLabel")
        # Frame do MAIN CONTROL
        # Design de Label
        self.mainControlFrame = QtWidgets.QFrame(self.Base)
        self.mainControlFrame.setGeometry(QtCore.QRect(210, 10, 218, 101))
        self.mainControlFrame.setStyleSheet("background: rgba(29, 222, 216, 0.1);")
        self.mainControlFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainControlFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainControlFrame.setObjectName("mainControlFrame")
        self.mainTextLabel = QtWidgets.QLabel(self.mainControlFrame)
        self.mainTextLabel.setGeometry(QtCore.QRect(65, 5, 91, 16))
        self.mainTextLabel.setStyleSheet("background: transparent;\n"
                                         "color: white;")
        self.mainTextLabel.setObjectName("mainTextLabel")
        self.mainLineFrame = QtWidgets.QFrame(self.mainControlFrame)
        self.mainLineFrame.setGeometry(QtCore.QRect(56, 20, 110, 1))
        self.mainLineFrame.setStyleSheet("background: #1DDED8;")
        self.mainLineFrame.setFrameShape(QtWidgets.QFrame.HLine)
        self.mainLineFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        # PLAY
        self.mainLineFrame.setObjectName("mainLineFrame")
        self.playButton = QtWidgets.QRadioButton(self.mainControlFrame)
        self.playButton.setGeometry(QtCore.QRect(25, 30, 51, 21))
        self.playButton.setStyleSheet("background: transparent;\n"
                                      "color: rgb(206, 255, 188);")
        self.playButton.setObjectName("playButton")
        self.playButton.setChecked(False)
        self.playButton.toggled.connect(self.mainState)
        # PAUSE
        self.pauseButton = QtWidgets.QRadioButton(self.mainControlFrame)
        self.pauseButton.setGeometry(QtCore.QRect(25, 70, 61, 21))
        self.pauseButton.setStyleSheet("background: transparent;\n"
                                       "color: rgb(206, 255, 188);")
        self.pauseButton.setObjectName("pauseButton")
        self.pauseButton.setChecked(False)
        self.pauseButton.toggled.connect(self.mainState)
        # STOP
        self.stopButton = QtWidgets.QRadioButton(self.mainControlFrame)
        self.stopButton.setGeometry(QtCore.QRect(25, 50, 61, 21))
        self.stopButton.setStyleSheet("background: transparent;\n"
                                      "font: 9pt \"Sans Serif\";\n"
                                      "color: rgb(206, 255, 188);")
        self.stopButton.setObjectName("stopButton")
        self.pauseButton.setChecked(False)
        self.pauseButton.toggled.connect(self.mainState)
        # RESET
        self.resetMainButton = QtWidgets.QPushButton(self.mainControlFrame)
        self.resetMainButton.setGeometry(QtCore.QRect(110, 38, 91, 23))
        self.resetMainButton.setStyleSheet("color: rgb(193, 69, 69);\n"
                                           "font: 75 9pt \"Clean\";\n"
                                           "background: rgba(25, 27, 33, 0.2);")
        self.resetMainButton.setObjectName("resetMainButton")
        # self.resetMainButton.toggled.connect(InProgress)
        # RELOAD
        self.reloadMainButton = QtWidgets.QPushButton(self.mainControlFrame)
        self.reloadMainButton.setGeometry(QtCore.QRect(110, 62, 91, 23))
        self.reloadMainButton.setStyleSheet("color: rgb(193, 69, 69);\n"
                                            "font: 75 9pt \"Clean\";\n"
                                            "background: rgba(25, 27, 33, 0.2);")
        self.reloadMainButton.setObjectName("reloadMainButton")
        # self.reloadMainButton.toggled.connect(InProgress)
        # Desing de Label do Main
        self.mainLeftLineFrame = QtWidgets.QFrame(self.mainControlFrame)
        self.mainLeftLineFrame.setGeometry(QtCore.QRect(107, 38, 2, 50))
        self.mainLeftLineFrame.setStyleSheet("background: #313640;")
        self.mainLeftLineFrame.setFrameShape(QtWidgets.QFrame.VLine)
        self.mainLeftLineFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.mainLeftLineFrame.setObjectName("mainLeftLineFrame")
        self.mainRightLineFrame = QtWidgets.QFrame(self.mainControlFrame)
        self.mainRightLineFrame.setGeometry(QtCore.QRect(203, 38, 2, 50))
        self.mainRightLineFrame.setStyleSheet("background: #313640;")
        self.mainRightLineFrame.setFrameShape(QtWidgets.QFrame.VLine)
        self.mainRightLineFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.mainRightLineFrame.setObjectName("mainRightLineFrame")
        # Design de Label do Frame Controller
        self.controllerFrame = QtWidgets.QFrame(self.Base)
        self.controllerFrame.setGeometry(QtCore.QRect(480, 10, 218, 101))
        self.controllerFrame.setStyleSheet("background: rgba(29, 222, 216, 0.1);")
        self.controllerFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.controllerFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.controllerFrame.setObjectName("controllerFrame")
        self.controllerTextLabel = QtWidgets.QLabel(self.controllerFrame)
        self.controllerTextLabel.setGeometry(QtCore.QRect(70, 5, 91, 16))
        self.controllerTextLabel.setStyleSheet("background: transparent;\n"
                                               "color: white;")
        self.controllerTextLabel.setObjectName("controllerTextLabel")
        self.controllerLine = QtWidgets.QFrame(self.controllerFrame)
        self.controllerLine.setGeometry(QtCore.QRect(60, 20, 110, 1))
        self.controllerLine.setStyleSheet("background: #1DDED8;")
        self.controllerLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.controllerLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.controllerLine.setObjectName("controllerLine")
        # FUZZY
        self.fuzzyControllerButton = QtWidgets.QRadioButton(self.controllerFrame)
        self.fuzzyControllerButton.setGeometry(QtCore.QRect(20, 30, 61, 21))
        self.fuzzyControllerButton.setStyleSheet("background: transparent;\n"
                                                 "color: rgb(206, 255, 188);\n"
                                                 "\n"
                                                 "")
        self.fuzzyControllerButton.setObjectName("fuzzyControllerButton")
        self.fuzzyControllerButton.toggled.connect(self.controlState)
        # MPC
        self.mpcControllerButton = QtWidgets.QRadioButton(self.controllerFrame)
        self.mpcControllerButton.setGeometry(QtCore.QRect(20, 50, 61, 21))
        self.mpcControllerButton.setStyleSheet("background: transparent;\n"
                                               "color: rgb(206, 255, 188);\n"
                                               "")
        self.mpcControllerButton.setObjectName("mpcControllerButton")
        self.mpcControllerButton.toggled.connect(self.controlState)
        # GotoXYTeta
        self.gotoControllerButton = QtWidgets.QRadioButton(self.controllerFrame)
        self.gotoControllerButton.setGeometry(QtCore.QRect(20, 70, 91, 21))
        self.gotoControllerButton.setStyleSheet("background: transparent;\n"
                                                "color: rgb(206, 255, 188);")
        self.gotoControllerButton.setObjectName("gotoControllerButton")
        self.gotoControllerButton.toggled.connect(self.controlState)
        # PWM
        self.pwmButton = QtWidgets.QRadioButton(self.controllerFrame)
        self.pwmButton.setGeometry(QtCore.QRect(130, 30, 61, 21))
        self.pwmButton.setStyleSheet("background: transparent;\n"
                                     "color: rgb(206, 255, 188);")
        self.pwmButton.setObjectName("pwmButton")
        self.pwmButton.toggled.connect(self.controlState)
        # OTHER
        self.otherControllerButton = QtWidgets.QRadioButton(self.controllerFrame)
        self.otherControllerButton.setGeometry(QtCore.QRect(130, 50, 61, 21))
        self.otherControllerButton.setStyleSheet("background: transparent;\n"
                                                 "color: rgb(206, 255, 188);")
        self.otherControllerButton.setObjectName("otherControllerButton")
        self.otherControllerButton.toggled.connect(self.controlState)
        # NONE
        self.noneControllerButton = QtWidgets.QRadioButton(self.controllerFrame)
        self.noneControllerButton.setGeometry(QtCore.QRect(130, 70, 61, 21))
        self.noneControllerButton.setStyleSheet("background: transparent;\n"
                                                "color: rgb(206, 255, 188);")
        self.noneControllerButton.setObjectName("noneControllerButton")
        self.noneControllerButton.toggled.connect(self.controlState)
        # Widget do Terminal Embedded
        self.terminalWidget = QtWidgets.QTabWidget(self.Base)
        self.terminalWidget.setGeometry(QtCore.QRect(121, 462, 1160, 141))
        self.terminalWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.terminalWidget.setObjectName("terminalWidget")
        self.terminalWidget.addTab(EmbTerminal(), "Terminal")
        #
        self.terminalWidget = QtWidgets.QTabWidget(self.Base)
        self.terminalWidget.setGeometry(QtCore.QRect(121, 462, 1160, 141))
        self.terminalWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.terminalWidget.setObjectName("terminalWidget")
        self.terminalFrame = QtWidgets.QWidget()
        self.terminalFrame.setObjectName("terminalFrame")
        # Inicia o terminal no app
        self.terminalWidget.addTab(EmbTerminal(), "Terminal")
        # Design do Label Robot State
        self.robotStateFrame = QtWidgets.QFrame(self.Base)
        self.robotStateFrame.setGeometry(QtCore.QRect(1063, 152, 215, 88))
        self.robotStateFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.robotStateFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.robotStateFrame.setObjectName("robotStateFrame")
        # Robot State - START
        self.robotStartButton = QtWidgets.QRadioButton(self.robotStateFrame)
        self.robotStartButton.setGeometry(QtCore.QRect(10, 20, 61, 21))
        self.robotStartButton.setStyleSheet("color: rgb(255, 255, 255)")
        self.robotStartButton.setObjectName("robotStartButton")
        self.robotStartButton.toggled.connect(self.robotState)
        # Robot State - SHUT DOWN
        self.robotDownButton = QtWidgets.QRadioButton(self.robotStateFrame)
        self.robotDownButton.setGeometry(QtCore.QRect(10, 50, 101, 21))
        self.robotDownButton.setStyleSheet("color: white;\n"
                                           "")
        self.robotDownButton.setObjectName("robotDownButton")
        self.robotDownButton.toggled.connect(self.robotState)
        # Robot State Line Design
        self.robotStateLineFrame = QtWidgets.QFrame(self.robotStateFrame)
        self.robotStateLineFrame.setGeometry(QtCore.QRect(113, 21, 2, 50))
        self.robotStateLineFrame.setStyleSheet("background: #1DDED8;")
        self.robotStateLineFrame.setFrameShape(QtWidgets.QFrame.VLine)
        self.robotStateLineFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.robotStateLineFrame.setObjectName("robotStateLineFrame")
        # RQT Console Button
        self.rqtConsoleButton = QtWidgets.QPushButton(self.robotStateFrame)
        self.rqtConsoleButton.setGeometry(QtCore.QRect(119, 21, 91, 23))
        self.rqtConsoleButton.setStyleSheet("background: rgba(29, 222, 216, 0.1);\n"
                                            "color: rgb(22, 22, 22)")
        self.rqtConsoleButton.setObjectName("rqtConsoleButton")
        self.rqtConsoleButton.clicked.connect(self.rqtConsoleTool)
        # RQT Logger Button
        self.rqtLoggerButton = QtWidgets.QPushButton(self.robotStateFrame)
        self.rqtLoggerButton.setGeometry(QtCore.QRect(120, 48, 91, 23))
        self.rqtLoggerButton.setStyleSheet("background: rgba(29, 222, 216, 0.1);\n"
                                           "color: rgb(22, 22, 22)")
        self.rqtLoggerButton.setObjectName("rqtLoggerButton")
        self.rqtLoggerButton.clicked.connect(self.rqtLoggerTool)
        # Design do Frame SIMULATION
        self.simulationFrame = QtWidgets.QFrame(self.Base)
        self.simulationFrame.setGeometry(QtCore.QRect(1063, 270, 215, 90))
        self.simulationFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.simulationFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.simulationFrame.setObjectName("simulationFrame")
        self.simulationLineFrame = QtWidgets.QFrame(self.simulationFrame)
        self.simulationLineFrame.setGeometry(QtCore.QRect(83, 21, 2, 50))
        self.simulationLineFrame.setStyleSheet("background: #1DDED8;")
        self.simulationLineFrame.setFrameShape(QtWidgets.QFrame.VLine)
        self.simulationLineFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.simulationLineFrame.setObjectName("simulationLineFrame")
        # RVIZ
        self.rvizButton = QtWidgets.QPushButton(self.simulationFrame)
        self.rvizButton.setGeometry(QtCore.QRect(89, 21, 121, 23))
        self.rvizButton.setStyleSheet("background: rgba(29, 222, 216, 0.1);\n"
                                      "color: rgb(22, 22, 22)")
        self.rvizButton.setObjectName("rvizButton")
        self.rvizButton.clicked.connect(self.rvizGraphButton)
        # GMAPP
        self.gmappButton = QtWidgets.QPushButton(self.simulationFrame)
        self.gmappButton.setGeometry(QtCore.QRect(90, 48, 121, 23))
        self.gmappButton.setStyleSheet("background: rgba(29, 222, 216, 0.1);\n"
                                       "color: rgb(22, 22, 22)")
        self.gmappButton.setObjectName("gmappButton")
        self.gmappButton.clicked.connect(self.gmappGraphButton)
        # Checkbox SHOW MAP
        self.mapShowButton = QtWidgets.QCheckBox(self.simulationFrame)
        self.mapShowButton.setGeometry(QtCore.QRect(10, 35, 61, 21))
        self.mapShowButton.setStyleSheet("color: white;")
        self.mapShowButton.setObjectName("mapShowButton")
        self.mapShowButton.stateChanged.connect(self.mapCheckbox)
        # Checkbox SHOW VISION
        self.visionShowButton = QtWidgets.QCheckBox(self.simulationFrame)
        self.visionShowButton.setGeometry(QtCore.QRect(10, 55, 61, 21))
        self.visionShowButton.setStyleSheet("color: white;")
        self.visionShowButton.setObjectName("visionShowButton")
        self.visionShowButton.stateChanged.connect(self.visionCheckbox)
        # Checkbox SHOW SIMULATION
        self.showSimulationButton = QtWidgets.QCheckBox(self.simulationFrame)
        self.showSimulationButton.setGeometry(QtCore.QRect(10, 15, 61, 21))
        self.showSimulationButton.setStyleSheet("color: white;")
        self.showSimulationButton.setObjectName("showSimulationButton")
        self.showSimulationButton.stateChanged.connect(self.simulationCheckbox)
        # Design do Frame TOOLS
        self.toolsFrame = QtWidgets.QFrame(self.Base)
        self.toolsFrame.setGeometry(QtCore.QRect(1063, 390, 215, 71))
        self.toolsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.toolsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.toolsFrame.setObjectName("toolsFrame")
        self.toolsLineFrame = QtWidgets.QFrame(self.toolsFrame)
        self.toolsLineFrame.setGeometry(QtCore.QRect(83, 10, 2, 50))
        self.toolsLineFrame.setStyleSheet("background: #1DDED8;")
        self.toolsLineFrame.setFrameShape(QtWidgets.QFrame.VLine)
        self.toolsLineFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.toolsLineFrame.setObjectName("toolsLineFrame")
        # RQT BAG
        self.rqtBagButton = QtWidgets.QPushButton(self.toolsFrame)
        self.rqtBagButton.setGeometry(QtCore.QRect(90, 10, 121, 23))
        self.rqtBagButton.setStyleSheet("background: rgba(29, 222, 216, 0.1);\n"
                                        "color: rgb(22, 22, 22)")
        self.rqtBagButton.setObjectName("rqtBagButton")
        self.rqtBagButton.clicked.connect(self.rqtBagTool)
        # RQT Dashboard
        self.rqtDashboardButton = QtWidgets.QPushButton(self.toolsFrame)
        self.rqtDashboardButton.setGeometry(QtCore.QRect(90, 37, 121, 23))
        self.rqtDashboardButton.setStyleSheet("background: rgba(29, 222, 216, 0.1);\n"
                                              "color: rgb(22, 22, 22)")
        self.rqtDashboardButton.setObjectName("rqtDashboardButton")
        self.rqtDashboardButton.clicked.connect(self.rqtDashboardTool)
        # JOYSTICK
        self.joystickButton = QtWidgets.QRadioButton(self.toolsFrame)
        self.joystickButton.setGeometry(QtCore.QRect(10, 15, 61, 21))
        self.joystickButton.setStyleSheet("color: white;")
        self.joystickButton.setObjectName("joystickButton")
        self.joystickButton.toggled.connect(self.tools)
        # TELEOP
        self.teleopButton = QtWidgets.QRadioButton(self.toolsFrame)
        self.teleopButton.setGeometry(QtCore.QRect(10, 35, 71, 21))
        self.teleopButton.setStyleSheet("color: white;")
        self.teleopButton.setObjectName("teleopButton")
        self.teleopButton.toggled.connect(self.tools)
        # Design do frame ROBOT VALUES
        self.valuesFrame = QtWidgets.QFrame(self.Base)
        self.valuesFrame.setGeometry(QtCore.QRect(750, 10, 218, 101))
        self.valuesFrame.setStyleSheet("background: rgba(29, 222, 216, 0.1);")
        self.valuesFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.valuesFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.valuesFrame.setObjectName("valuesFrame")
        self.ValueTextLabel = QtWidgets.QLabel(self.valuesFrame)
        self.ValueTextLabel.setGeometry(QtCore.QRect(68, 5, 101, 16))
        self.ValueTextLabel.setStyleSheet("background: transparent;\n"
                                          "color: white;")
        self.ValueTextLabel.setObjectName("ValueTextLabel")
        self.valueLineFrame = QtWidgets.QFrame(self.valuesFrame)
        self.valueLineFrame.setGeometry(QtCore.QRect(60, 20, 110, 1))
        self.valueLineFrame.setStyleSheet("background: #1DDED8;")
        self.valueLineFrame.setFrameShape(QtWidgets.QFrame.HLine)
        self.valueLineFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.valueLineFrame.setObjectName("valueLineFrame")
        # Design do LCD e Label "X"
        self.XValue = QtWidgets.QLCDNumber(self.valuesFrame)
        self.XValue.setGeometry(QtCore.QRect(50, 33, 31, 20))
        self.XValue.setObjectName("XValue")
        self.XValue.display(self.xLcdNumber())
        self.XLabel = QtWidgets.QLabel(self.valuesFrame)
        self.XLabel.setGeometry(QtCore.QRect(30, 35, 16, 16))
        self.XLabel.setStyleSheet("background: transparent;\n"
                                  "color: rgb(206, 255, 188);")
        self.XLabel.setObjectName("XLabel")
        # Design do LCD e Label "Y"
        self.YLabel = QtWidgets.QLCDNumber(self.valuesFrame)
        self.YLabel.setGeometry(QtCore.QRect(50, 63, 31, 20))
        self.YLabel.setObjectName("YLabel")
        self.YValue = QtWidgets.QLabel(self.valuesFrame)
        self.YValue.setGeometry(QtCore.QRect(30, 65, 16, 16))
        self.YValue.setStyleSheet("background: transparent;\n"
                                  "color: rgb(206, 255, 188);")
        self.YValue.setObjectName("YValue")
        # Design do LCD e Label "VELOCITY"
        self.velocityValue = QtWidgets.QLCDNumber(self.valuesFrame)
        self.velocityValue.setGeometry(QtCore.QRect(165, 33, 31, 20))
        self.velocityValue.setObjectName("velocityValue")
        self.velocityLabel = QtWidgets.QLabel(self.valuesFrame)
        self.velocityLabel.setGeometry(QtCore.QRect(110, 35, 61, 16))
        self.velocityLabel.setStyleSheet("background: transparent;\n"
                                         "color: rgb(206, 255, 188);")
        self.velocityLabel.setObjectName("velocityLabel")
        # Design do LCD e Label "Battery"
        self.batteryValue = QtWidgets.QLCDNumber(self.valuesFrame)
        self.batteryValue.setGeometry(QtCore.QRect(165, 63, 31, 20))
        self.batteryValue.setObjectName("batteryValue")
        self.batteryLabel = QtWidgets.QLabel(self.valuesFrame)
        self.batteryLabel.setGeometry(QtCore.QRect(110, 65, 61, 16))
        self.batteryLabel.setStyleSheet("background: transparent;\n"
                                           "color: rgb(206, 255, 188);")
        self.batteryLabel.setObjectName("batteryLabel")
        # Widget Space for Simulation
        self.simulationWidget = QtWidgets.QLabel(self.Base)
        self.simulationWidget.setGeometry(QtCore.QRect(122, 122, 920, 338))
        # self.simulationWidget.setGeometry(QtCore.QRect(121, 125, 551, 333))
        self.simulationWidget.setObjectName("simulationWidget")
        # Widget Space for Map
        # self.mapWidget = QtWidgets.QLabel(self.Base)
        # self.mapWidget.setGeometry(QtCore.QRect(673, 126, 388, 221))
        # self.mapWidget.setObjectName("mapWidget")
        # Widget Space for Kinect
        # self.kinectWidget = QtWidgets.QLabel(self.Base)
        # self.kinectWidget.setGeometry(QtCore.QRect(673, 340, 388, 120))
        # self.kinectWidget.setStyleSheet("border-color: rgb(85, 255, 255);")
        # self.kinectWidget.setObjectName("kinectWidget")
        # Raise Widgets
        self.lateralMenuFrame.raise_()
        self.logoFrame.raise_()
        self.MenuLine.raise_()
        self.homeButton.raise_()
        self.dataButton.raise_()
        self.adhocButton.raise_()
        self.configButton.raise_()
        self.mailButton.raise_()
        self.logoButton.raise_()
        self.SuperiorLine.raise_()
        self.InferiorLine.raise_()
        self.LateraLine.raise_()
        self.robotStateLabel.raise_()
        self.simulationLabel.raise_()
        self.toolsLabel.raise_()
        self.mainControlFrame.raise_()
        self.controllerFrame.raise_()
        self.terminalWidget.raise_()
        self.robotStateFrame.raise_()
        self.simulationFrame.raise_()
        self.toolsFrame.raise_()
        self.valuesFrame.raise_()
        self.simulationWidget.raise_()
        # self.mapWidget.raise_()
        # self.kinectWidget.raise_()
        MainWindow.setCentralWidget(self.Base)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.homeButton.setText(_translate("MainWindow", "Home"))
        self.dataButton.setText(_translate("MainWindow", "Data"))
        self.adhocButton.setText(_translate("MainWindow", "Ad-hoc"))
        self.configButton.setText(_translate("MainWindow", "Config"))
        self.mailButton.setText(_translate("MainWindow", "Mail"))
        self.logoButton.setText(_translate("MainWindow", "PPGI UFPB"))
        self.robotStateTextLabel.setText(_translate("MainWindow", "ROBOT STATE"))
        self.simulationTextLabel.setText(_translate("MainWindow", "SIMULATION"))
        self.toolsTextLabel.setText(_translate("MainWindow", "TOOLS"))
        self.mainTextLabel.setText(_translate("MainWindow", "MAIN CONTROL"))
        self.playButton.setText(_translate("MainWindow", "PLAY"))
        self.pauseButton.setText(_translate("MainWindow", "PAUSE"))
        self.stopButton.setText(_translate("MainWindow", "STOP"))
        self.resetMainButton.setText(_translate("MainWindow", "RESET"))
        self.reloadMainButton.setText(_translate("MainWindow", "RELOAD"))
        self.controllerTextLabel.setText(_translate("MainWindow", "CONTROLLER"))
        self.fuzzyControllerButton.setText(_translate("MainWindow", "Fuzzy"))
        self.mpcControllerButton.setText(_translate("MainWindow", "MPC"))
        self.gotoControllerButton.setText(_translate("MainWindow", "GotoXYTeta"))
        self.pwmButton.setText(_translate("MainWindow", "PWM"))
        self.otherControllerButton.setText(_translate("MainWindow", "Other"))
        self.noneControllerButton.setText(_translate("MainWindow", "None"))
        self.robotStartButton.setText(_translate("MainWindow", "START"))
        self.robotDownButton.setText(_translate("MainWindow", "SHUT DOWN"))
        self.rqtConsoleButton.setText(_translate("MainWindow", "RQT Console"))
        self.rqtLoggerButton.setText(_translate("MainWindow", "RQT Logger"))
        self.rvizButton.setText(_translate("MainWindow", "RVIZ INTERFACE"))
        self.gmappButton.setText(_translate("MainWindow", "GMAPP INTERFACE"))
        self.mapShowButton.setText(_translate("MainWindow", "MAP"))
        self.visionShowButton.setText(_translate("MainWindow", "VISION"))
        self.showSimulationButton.setText(_translate("MainWindow", "SHOW"))
        self.rqtBagButton.setText(_translate("MainWindow", "RQT BAG FILE"))
        self.rqtDashboardButton.setText(_translate("MainWindow", "RQT DASHBOARD"))
        self.joystickButton.setText(_translate("MainWindow", "JOY"))
        self.teleopButton.setText(_translate("MainWindow", "TELEOP"))
        self.ValueTextLabel.setText(_translate("MainWindow", "ROBOT VALUES"))
        self.XLabel.setText(_translate("MainWindow", "X:"))
        self.YValue.setText(_translate("MainWindow", "Y:"))
        self.velocityLabel.setText(_translate("MainWindow", "Velocity:"))
        self.batteryLabel.setText(_translate("MainWindow", "Battery:"))


if __name__ == "__main__":
    # rospy.init_node('turtleui')
    # print('Running...')
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    # rospy.spin()
