import struct
from time import time
from recorders import recorders

class Parser:
    def __init__(self, record_readings=True, recorder=recorders()):
        self.parser = self.run()
        self.parser.next()
        self.current_vector = []
        self.raw_values = []
        self.current_spectrum = []
        self.sending_data = False
        self.state ="initializing"
        self.recorder = recorder

        if record_readings:
            self.record()

    def record(self):
            self.recorder.start_raw_serial_recording()
            self.recorder.start_esense_recording()
            self.recorder.start_raw_data_recording()

    def parse(self, data):
        for byte in data:
            self.recorder.write_raw_serial(byte)
            self.parser.send(ord(byte))    # Send byte to the generator

    def close(self):
        self.recorder.stop_recording()

    def run(self):
        """
            This generator parses one byte at a time.
        """
        last = time()
        i = 1
        self.buffer_len = 512*3
        times = []
        while True:
            byte = yield
            if byte== 0xaa:
                byte = yield # This byte should be "\aa" too
                if byte== 0xaa:
                    # packet synced by 0xaa 0xaa
                    packet_length = yield
                    packet_code = yield
                    if packet_code == 0xd4:
                        # standing by
                        self.state= "standby"
                    elif packet_code == 0xd0:
                        self.state = "connected"
                    else:
                        self.sending_data = True
                        left = packet_length-2
                        while left>0:
                            if packet_code ==0x80: # raw value
                                row_length = yield
                                a = yield
                                b = yield
                                value = struct.unpack("<h",chr(a)+chr(b))[0]
                                self.recorder.write_raw_data(value)
                                self.raw_values.append(value)
                                if len(self.raw_values)>self.buffer_len:
                                    self.raw_values = self.raw_values[-self.buffer_len:]
                                left-=2

                            elif packet_code == 0x02: # Poor signal
                                a = yield
                                self.poor_signal = a
                                if a>0:
                                    pass 
                                left-=1

                            elif packet_code == 0x04: # Attention (eSense)
                                a = yield
                                if a>0:
                                    v = struct.unpack("b",chr(a))[0]
                                    if v>0:
                                        self.current_attention = v
                                        self.recorder.write_esense_attention(v)
                                left-=1

                            elif packet_code == 0x05: # Meditation (eSense)
                                a = yield
                                if a>0:
                                    v = struct.unpack("b",chr(a))[0]
                                    if v>0:
                                        self.current_meditation = v
                                        self.recorder.write_esense_meditation(v)
                                left-=1

                            elif packet_code == 0x16:
                                v = yield
                                self.current_blink_strength = v
                                self.recorder.write_esense_blink_strength(v)
                                left -= 1

                            elif packet_code == 0x83:
                                    vlength = yield
                                    self.current_vector = []
                                    for row in range(8):
                                        a = yield
                                        b = yield
                                        c = yield
                                        value = a*255*255+b*255+c
                                        self.current_vector.append(value)
                                    left-=vlength
                            packet_code = yield                    
                else:
                    pass # sync failed
            else:
                pass # sync failed
