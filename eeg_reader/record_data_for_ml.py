#!/usr/bin/pythonp
import mindwave_mobile.mindwave as mw
from mindwave_mobile.recorders import recorders
from mindwave_mobile.parser import Parser
from bluetooth.btcommon import BluetoothError
from time import sleep, time
import sys

def getParserForMood(mood):
    recorder = recorders()
    recorder.start_raw_serial_recording(file_name="%s_raw_serial.out" % mood)
    recorder.start_raw_data_recording(file_name="%s_raw_data.out" % mood)
    return Parser(record_readings=False, recorder)


def main():

    mindwave = mw.MindwaveBluetooth(mac_addr, parser=None)

    if not mindwave.connected:
        sys.exit("Couldn't connect to device connceted. Please Try again")
        # Need to wait before the device is ready for sending data
        sleep(2)
        # Need to put the EEG into the correct mode
        #mindwave.write("\0x20")

    moods = []

    for mood in moods:
        print("%s Mood " % mood)
        parser = getParserForMood(mood)
        start = time()
        sleep_time = 0.25
        minutes = 5
        duration = minutes * 60
        iterations = 60 / sleep_time
        i = 0
        while (time() - start) < minutes:
            try:
                mindwave.update()
            except BluetoothError, e:
                print e
                print("Sleeping. Hoping the error sorts itself out")
                sleep(1)
                continue
            except KeyboardInterrupt:
                # Only catchthing this so we can break and close properly
                # If you dont close you might have to power cycle
                # before you can connect again
                break
            else:
                i += 1
                if i == iterations:
                    time_left_minutes = (duration - (time() -start)) / 60
                    print("%d minutes left" % time_left_minutes)
                    i = 0
                sleep(sleep_time)

    mindwave.close()

if __name__ == '__main__':
    main()
