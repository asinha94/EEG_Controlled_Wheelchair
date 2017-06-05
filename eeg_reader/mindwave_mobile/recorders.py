import struct
import time
from numpy import mean # Remove?

class recorders:
    def __init__(self):
        self.raw_serial_file = None
        self.raw_data_file = None
        self.esense_file = None
        self.time_format = "----- %Y-%m-%d --- %H:%M:%S -----"

    def start_raw_serial_recording(self, file_name="raw_serial.out"):
        self.raw_serial_file = open(file_name, "w")
        self.raw_serial_file.write("%s\n" % time.strftime(self.time_format))

    def start_esense_recording(self, file_name="esense_reading.out"):
        self.esense_file = open(file_name, "w")
        self.esense_file.write("%s\n" % time.strftime(self.time_format))

    def start_raw_data_recording(self, file_name="raw_data.out"):
        self.raw_data_file = open(file_name, "w")
        self.raw_data_file.write("%s\n" % time.strftime(self.time_format))

    def stop_raw_serial_recording(self):
        if self.raw_serial_file:
            self.raw_serial_file.close()
            self.raw_serial_file = None
        
    def stop_esense_recording(self):
        if self.esense_file:
            self.esense_file.close()
            self.esense_file = None

    def write_raw_serial(self, byte):
        if self.raw_serial_file is not None:
            self.raw_serial_file.write("%s\n" % hex(ord(byte)))
            
    def write_raw_data(self, raw_reading):
        if self.raw_data_file is not None:
            self.raw_data_file.write("%s\n" % str(raw_reading))

    def write_esense_meditation(self, reading):
        if self.esense_file is not None:
            self.esense_file.write("Meditation: %s\n" % str(reading))

    def write_esense_attention(self, reading):
        if self.esense_file is not None:
            self.esense_file.write("Attention: %s\n" % str(reading))

    def write_esense_blink_strength(self, reading):
        if self.esense_file is not None:
            self.esense_file.write("Blink Strength: %s\n" % str(reading))

    
