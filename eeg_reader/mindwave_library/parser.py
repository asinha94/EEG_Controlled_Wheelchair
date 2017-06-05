import struct
from time import time
from numpy import mean # Remove?
import mindwave_bluetooth
from recorders import recorders

dongle_state = None
DONGLE_STANDBY= "Standby"

class Parser:
    def __init__(self, record_readings=True):
        self.parser = self.run()
        self.parser.next()
        self.current_vector = []
        self.raw_values = []
        self.current_meditation = 0
        self.current_attention= 0
        self.current_blink_strength = 0
        self.current_spectrum = []
        self.sending_data = False
        self.state ="initializing"
        self.device_connected = False
        self.recorder = recorders()

        if record_readings:
            self.recorder.start_raw_serial_recording()
            self.
            

    def connect(self, mac_address=None):
        if mac_address is None:
            self.mindwaveMobileSocket, self.address = mindwave_bluetooth.connect_magic()
        else:
            self.mindwaveMobileSocket, self.address = mindwave_bluetooth.connect_bluetooth_addr(mac_address)

            if self.mindwaveMobileSocket is not None:
                self.device_connected = True
            
    def update(self):
        bytes = self.mindwaveMobileSocket.recv(1000)
        for b in bytes:
            self.file_handle.write("%s\n" % hex(ord(b)))
            self.parser.send(ord(b))    # Send each byte to the generator

    def write_serial(self, string):
        self.mindwaveMobileSocket.send(string)
    

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
                        self.dongle_state= "standby"
                    elif packet_code == 0xd0:
                        self.dongle_state = "connected"
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
