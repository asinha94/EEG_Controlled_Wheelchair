from PySide import QtCore, QtGui
import serial

class ArduinoWidget(QtGui.QWidget):
    def __init__(self, comport):
        QtGui.QWidget.__init__(self)
        self.comport = comport
        self.btn_connect_string = "Connect"
        self.btn_disconnect_string = "Disconnect"
        self.connected = False
        self.initLayout()

    def initLayout(self):
        font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        self.arduino_label = QtGui.QLabel("Arduino")
        self.arduino_label.setFont(font)
        self.arduino_status_label = QtGui.QLabel(self.getStatusString())
        self.button = QtGui.QPushButton(self.btn_connect_string)
        self.button.clicked.connect(self.buttonPressed)
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.arduino_label)
        self.vbox.addWidget(self.arduino_status_label)
        self.vbox.addWidget(self.button)
        self.setLayout(self.vbox)

    def buttonPressed(self):
        if self.connected:
            self.disconnect()
        else:
            self.connect()

    def getStatusString(self):
        status = "Connected" if self.connected else "Disconnected"
        return "Status: %s" % status

    def connect(self):
        # self.connection = serial.Serial(comPort, baudrate=9600, timeout=5)
        self.connected = True
        self.arduino_status_label.setText(self.getStatusString())
        self.button.setText(self.btn_disconnect_string)

    def disconnect(self):
        # self.connection.close()
        self.connected = False
        self.arduino_status_label.setText(self.getStatusString())
        self.button.setText(self.btn_connect_string)

    def forward(self):
        self.connection.write('')

    def stop(self):
        self.connection.write('')

class MindwaveWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.btn_connect_string = "Connect"
        self.btn_disconnect_string = "Disconnect"
        self.initLayout()

    def initLayout(self):
        font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        self.arduino_label = QtGui.QLabel("EEG")
        self.arduino_label.setFont(font)
        self.arduino_status_label = QtGui.QLabel('Disconnected')
        self.button = QtGui.QPushButton(self.btn_connect_string)
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.arduino_label)
        self.vbox.addWidget(self.arduino_status_label)
        self.vbox.addWidget(self.button)
        self.setLayout(self.vbox)
        
