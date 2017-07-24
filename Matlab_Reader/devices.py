from PySide import QtCore, QtGui
from mat import MatlabThread
import serial

class ArduinoWidget(QtGui.QWidget):
    def __init__(self, comport):
        QtGui.QWidget.__init__(self)
        self.comport = comport
        self.connected = False
        self.initLayout()

    def initLayout(self):
        # Main Label
        font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        self.arduino_label = QtGui.QLabel("Arduino")
        self.arduino_label.setFont(font)
        # Buttton
        self.btn_connect_string = "Connect"
        self.btn_disconnect_string = "Disconnect"
        self.button = QtGui.QPushButton(self.btn_connect_string)
        self.button.clicked.connect(self.buttonPressed)
        # Image
        self.loadIcons()
        self.status_label = QtGui.QLabel()
        self.status_label.setPixmap(self.disconnected_icon)
        # Add widgets
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.arduino_label)
        hbox.addWidget(self.button)
        hbox.addWidget(self.status_label)
        self.setLayout(hbox)

    def loadIcons(self):
        green_icon = QtGui.QPixmap('images\green-square.jpg')
        self.connected_icon = green_icon.scaled(20, 20, QtCore.Qt.KeepAspectRatio)
        red_icon = QtGui.QPixmap('images\Red.png')
        self.disconnected_icon = red_icon.scaled(20, 20, QtCore.Qt.KeepAspectRatio)

    def buttonPressed(self):
        if self.connected:
            self.disconnect()
        else:
            self.connect()

    def connect(self):
        self.connection = serial.Serial(comPort, baudrate=9600, timeout=5)
        self.connected = True
        self.button.setText(self.btn_disconnect_string)
        self.status_label.setPixmap(self.connected_icon)

    def disconnect(self):
        self.connection.close()
        self.connected = False
        self.button.setText(self.btn_connect_string)
        self.status_label.setPixmap(self.disconnected_icon)

    def forward(self):
        self.connection.write('f\n')
        pass

    def stop(self):
        self.connection.write('s\n')
        pass

class MindwaveWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.connected = False
        self.loadIcons()
        self.initLayout()
        self.matlabThread = None

    def initMatlabThread(self):
        self.matlabThread = MatlabThread()
        self.matlabThread.start()

    def killMatlabThread(self):
        self.matlabThread.terminate()
        self.matlabThread = None

    def initLayout(self):
        # Main Label
        font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        self.eeg_label = QtGui.QLabel("EEG")
        self.eeg_label.setFont(font)
        # Buttons
        self.btn_connect_string = "Connect"
        self.btn_disconnect_string = "Disconnect"
        self.button = QtGui.QPushButton(self.btn_connect_string)
        self.button.clicked.connect(self.buttonPressed)
        # Image
        self.status_label = QtGui.QLabel()
        self.status_label.setPixmap(self.disconnected_icon)
        # Add to Widget
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.eeg_label)
        hbox.addWidget(self.button)
        hbox.addWidget(self.status_label)
        self.setLayout(hbox)

    def loadIcons(self):
        green_icon = QtGui.QPixmap('images/green-square.jpg')
        self.connected_icon = green_icon.scaled(20, 20, QtCore.Qt.KeepAspectRatio)
        red_icon = QtGui.QPixmap('images/Red.png')
        self.disconnected_icon = red_icon.scaled(20, 20, QtCore.Qt.KeepAspectRatio)

    def buttonPressed(self):
        if self.connected:
            self.disconnect()
        else:
            self.connect()

    def connect(self):
        self.initMatlabThread()
        self.status_label.setPixmap(self.connected_icon)
        self.button.setText(self.btn_disconnect_string)
        self.connected = True

    def disconnect(self):
        self.killMatlabThread()
        self.status_label.setPixmap(self.disconnected_icon)
        self.button.setText(self.btn_connect_string)
        self.connected = False
        
class DevicesLeftPane(QtGui.QWidget):
    attention_signal = QtCore.Signal(int)
    meditation_signal = QtCore.Signal(int)
    blink_signal = QtCore.Signal(int)
    def __init__(self):
        QtGui.QWidget.__init__(self)
        vbox = QtGui.QVBoxLayout()
        self.arduino = ArduinoWidget('COM4')
        self.mindwave = MindwaveWidget()
        vbox.addWidget(self.arduino)
        vbox.addWidget(self.mindwave)
        self.setLayout(vbox)

    def forward(self):
        self.arduino.forward()

    def stop(self):
        self.arduino.stop()

class DevicesRightPane(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.moving = False
        self.loadIcons()
        # Main
        font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        main_label = QtGui.QLabel('Vehicle Controls')
        main_label.setFont(font)
        # Forward
        hbox_forward = QtGui.QHBoxLayout()
        forward_label = self.createLabel('Forward')
        self.forward_select_label = QtGui.QLabel()
        hbox_forward.addWidget(forward_label)
        hbox_forward.addWidget(self.forward_select_label)
        # Stop
        hbox_stop = QtGui.QHBoxLayout()
        stop_label = self.createLabel('Stop')
        self.stop_select_label = QtGui.QLabel()
        self.stop_select_label.setPixmap(self.select_icon)
        hbox_stop.addWidget(stop_label)
        hbox_stop.addWidget(self.stop_select_label)
        # Add to main widget
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(main_label)
        vbox.addLayout(hbox_forward)
        vbox.addLayout(hbox_stop)
        self.setLayout(vbox)

    def createLabel(self, labelName):
        sub_font = QtGui.QFont("Arial", 15, QtGui.QFont.Bold)
        label = QtGui.QLabel(labelName)
        label.setFont(sub_font)
        return label

    def loadIcons(self):
        black_icon = QtGui.QPixmap('images/black.jpg')
        self.select_icon = black_icon.scaled(20, 20, QtCore.Qt.KeepAspectRatio)

    def forward(self):
        self.moving = True
        self.forward_select_label.setPixmap(self.select_icon)
        self.stop_select_label.setPixmap(None)

    def stop(self):
        self.moving = False
        self.forward_select_label.setPixmap(None)
        self.stop_select_label.setPixmap(self.select_icon)
        