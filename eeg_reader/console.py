#!/usr/bin/python
import mindwave_mobile.mindwave as mw
from bluetooth.btcommon import BluetoothError
from time import sleep
import sys

def main():
    mac_addr = "A0:E6:F8:F7:B9:58"
    mindwave = mw.MindwaveBluetooth(mac_addr)

    if not mindwave.connected:
        print("Couldn't connect to device connceted. Try again.")
        sys.exit(1)

    # Need to wait before the device is ready for sending data
    sleep(2)

    # Need to put the EEG into the correct mode
    #mindwave.write("\0x20")

    while True:
        try:
            mindwave.update()
        except BluetoothError, e:
            print e
            print("Sleeping. Hoping the error sorts itself out")
            sleep(1)
        except KeyboardInterrupt:
            # Only catchthing this so we can break and close
            # If you dont close you might have to power cycle
            # before you can connect again
            break
    
        # Print all the current values
        #print("Blink Strength: %s" % str(mindwave.get_blink_strength_value()))
        print("Meditation    : %s" % str(mindwave.get_meditation_value()))
        print("Attention     : %s\n\n" % str(mindwave.get_attention_value()))
        sleep(0.2)

    # 
    mindwave.close()

if __name__ == '__main__':
    main()
