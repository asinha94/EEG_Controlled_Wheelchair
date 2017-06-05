import mindwave_mobile.mindwave as mw
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

    while True:
        mindwave.update()
        print("Blink Strength: %s" % str(mindwave.get_blink_strength_value()))
        print("Meditation    : %s" % str(mindwave.get_meditation_value()))
        print("Attention     : %s\n\n" % str(mindwave.get_attention_value()))
        sleep(0.2)
    


if __name__ == '__main__':
    main()
