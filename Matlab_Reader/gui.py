from PySide import QtGui, QtCore, QtDeclarative
from devices import DevicesLeftPane, DevicesRightPane, ArduinoWidget, MindwaveWidget
import PySide
import sys

def debug(data):
    sys.stderr.write('%s\n' % str(data))

class StreamWriter(QtCore.QObject):
    attention_signal = QtCore.Signal(int)
    meditation_signal = QtCore.Signal(int)
    blink_signal = QtCore.Signal(int)
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.oldstdout = sys.stdout

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
            pass
            #sys.stderr.write('Unkown Command: %s:%s' % (param, val))

class SpeedDial(QtDeclarative.QDeclarativeView):
    def __init__(self):
        QtDeclarative.QDeclarativeView.__init__(self)
        self.setSource(QtCore.QUrl.fromLocalFile('qml\dialcontrol.qml'))
        self.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    def convertVal(self, value):
        return int(value * (5/6))

    def setValue(self, value):
        self.rootObject().setProperty("value", value)

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
    forward_signal = QtCore.Signal()
    stop_signal = QtCore.Signal()
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.stream = StreamWriter()
        sys.stdout = self.stream
        self.initWindow()
        self.initLayout()
        self.setWidgetFormatting()
        self.initStream()

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
        self.forward_signal.connect(left.forward)
        self.forward_signal.connect(right.forward)
        self.stop_signal.connect(left.stop)
        self.stop_signal.connect(right.stop)
        hbox.addWidget(left)
        hbox.addWidget(right)
        self.vbox.addLayout(hbox)

    def setWidgetFormatting(self):
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor('white'))
        self.centralWidget.setPalette(pal)
        self.centralWidget.setAutoFillBackground(True)

    def initStream(self):
        self.stream.attention_signal.connect(self.attentionHandler)
        self.stream.meditation_signal.connect(self.meditationHandler)
        self.stream.blink_signal.connect(self.blinkHandler)

    def attentionHandler(self, val):
        self.attention.setValue(val)
        if val > 50:
            self.forward_signal.emit()
        else:
            self.stop_signal.emit()

    def meditationHandler(self, val):
        self.meditation.setValue(val)

    def blinkHandler(self, val):
        self.blink.setValue(val)
        if val > 60:
            self.stop_signal.emit()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    frame  = MainWindow()
    frame.show()
    sys.exit(app.exec_())