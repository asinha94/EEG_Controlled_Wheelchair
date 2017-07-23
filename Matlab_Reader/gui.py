from PySide import QtGui, QtCore, QtDeclarative
from devices import ArduinoWidget, MindwaveWidget
import PySide
import sys


class SpeedDial(QtDeclarative.QDeclarativeView):
    def __init__(self):
        QtDeclarative.QDeclarativeView.__init__(self)
        self.setSource(QtCore.QUrl.fromLocalFile('qml\dialcontrol.qml'))
        self.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    def setValue(self, value):
        self.rootObject().setProperty("value", 40)

class SpeedDialWidget(QtGui.QWidget):
    def __init__(self, labelName):
        QtGui.QWidget.__init__(self)
        self.label = QtGui.QLabel(labelName)
        font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.dial = SpeedDial()
        
        # Add the VBox to the main layout
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.dial)
        self.vbox.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.vbox)

    def setValue(self, value):
        self.dial.setValue(value)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initWindow()
        self.initLayout()
        self.setWidgetFormatting()

    def initWindow(self):
        self.setWindowTitle('EEG Command Center')
        self.width = 800
        self.height = 600
        self.resize(self.width, self.height)

    def initLayout(self):
        self.vbox = QtGui.QVBoxLayout()
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.vbox)
        self.setCentralWidget(self.centralWidget)
        self.initDials()
        self.initDevices()

    def initDials(self):
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(SpeedDialWidget("Meditation"))
        hbox.addWidget(SpeedDialWidget("Attention"))
        hbox.addWidget(SpeedDialWidget("Blink Strength"))
        self.vbox.addLayout(hbox)

    def initDevices(self):
        hbox = QtGui.QHBoxLayout()
        arduino = ArduinoWidget('COM6')
        eeg = MindwaveWidget()
        hbox.addWidget(arduino)
        hbox.addWidget(eeg)
        self.vbox.addLayout(hbox)

    def setWidgetFormatting(self):
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor('white'))
        self.centralWidget.setPalette(pal)
        self.centralWidget.setAutoFillBackground(True)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    frame  = MainWindow()
    frame.show()
    sys.exit(app.exec_())