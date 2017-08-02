import serial
from time import sleep

arduino_file_descriptor = "/dev/ttyUSB0"
arduino = serial.Serial(arduino_file_descriptor, 9600, timeout=5)

val = 1
while True:
    val = int(not val)
    arduino.write(str(val))
    sleep(2)
    

