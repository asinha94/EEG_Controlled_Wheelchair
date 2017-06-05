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
        except BluetoothError:
            print("Sleeping for 1s")
            sleep(1)
        except KeyboardInterrupt:
            mindwave.close()
            
    
        # Print all the current values
        print("Blink Strength: %s" % str(mindwave.get_blink_strength_value()))
        print("Meditation    : %s" % str(mindwave.get_meditation_value()))
        print("Attention     : %s\n\n" % str(mindwave.get_attention_value()))
        sleep(0.2)

if __name__ == '__main__':
    main()
