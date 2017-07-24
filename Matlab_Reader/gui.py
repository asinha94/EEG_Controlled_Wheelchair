from PySide import QtGui, QtCore, QtDeclarative
from devices import DevicesLeftPane, DevicesRightPane, ArduinoWidget, MindwaveWidget
import PySide
import sys

class StreamWriter(QtCore.QObject):
	attention_signal = QtCore.Signal(int)
	meditation_signal = QtCore.Signal(int)
	blink_signal = QtCore.Signal(int)
	def __init__(self):
		QtCore.QObject.__init__(self)
		self.oldstdout = sys.stdout
		sys.stdout = self

	def write(self, data):
		if len(data.strip()):
			self.updateValue(data)

	def updateValue(self, data):
		param, val = data.strip().lower().split(':')
		if param == 'attention':
			self.attention_signal.emit(int(val))
		elif param == 'meditation':
			self.meditation_signal.emit(int(val))
		elif param == 'blink':
			self.blink_signal.emit(int(val))
		else:
			sys.stderr.write('Unkown Command: %s:%s' % (param, val))

class SpeedDial(QtDeclarative.QDeclarativeView):
    def __init__(self):
        QtDeclarative.QDeclarativeView.__init__(self)
        self.setSource(QtCore.QUrl.fromLocalFile('qml\dialcontrol.qml'))
        self.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    def convertVal(value):
        return value * (5/6)

    def setValue(self, value):
        self.rootObject().setProperty("value", self.convertVal(value))

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
        self.initStream()

    def initStream(self):
        self.stream = StreamWriter()
        self.stream.attention_signal.connect(self.attention.setValue)
        self.stream.meditation_signal.connect(self.meditation.setValue)
        self.stream.blink_signal.connect(self.blink.setValue)

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
        self.meditation = SpeedDialWidget("Meditation")
        self.attention = SpeedDialWidget("Attention")
        self.blink = SpeedDialWidget("Blink Strength")
        hbox.addWidget(self.meditation)
        hbox.addWidget(self.attention)
        hbox.addWidget(self.blink)
        self.vbox.addLayout(hbox)

    def initDevices(self):
        hbox = QtGui.QHBoxLayout()
        left = DevicesLeftPane()
        right = DevicesRightPane()
        hbox.addWidget(left)
        hbox.addWidget(right)
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