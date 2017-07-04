#!/usr/bin/python
import mindwave_mobile.mindwave as mw
from bluetooth.btcommon import BluetoothError
from time import sleep
import sys
import serial


def setupArduino():
    arduino_fd = '/dev/ttyUSB0'
    arduino = serial.Serial(arduino_fd, 9600, timeout=5)
    

def setupMindwave(mac_addr="A0:E6:F8:F7:B9:58"):

    mindwave = mw.MindwaveBluetooth(mac_addr)

    if not mindwave.connected:
        sys.exit("Couldn't connect to device connceted. Please Try again")
    # Need to wait before the device is ready for sending data
    sleep(2)
    # Need to put the EEG into the correct mode
    #mindwave.write("\0x20")
    return mindwave

def main():

    while True:
        mindwave = setupMindwave()
        while mindwave.connected:
            try:
                mindwave.update()
            except BluetoothError, e:
                print e
                print("Sleeping. Hoping the error sorts itself out")
                sleep(1)
                break
            else:
                # Print all the current values
                #print("Blink Strength: %s" % str(mindwave.get_blink_strength_value()))
                print("----------------------")
                print("Meditation    : %s" % str(mindwave.get_meditation_value()))
                print("Attention     : %s" % str(mindwave.get_attention_value()))
                sleep(0.25)
        mindwave.close()
            
if __name__ == '__main__':
    main()
