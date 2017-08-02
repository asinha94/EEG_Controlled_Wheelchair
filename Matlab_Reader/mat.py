from time import sleep
from PySide import QtCore
import sys
import matlab.engine

class MatlabThread(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)
		
	def run(self):
		eng = matlab.engine.start_matlab()
		task = eng.new(async=True, nargout=0)
		while not task.done():
			sleep(0.5)
		
if __name__ == '__main__':
	a = MatlabThread()
	a.start()
	sleep(10)
	a.terminate()