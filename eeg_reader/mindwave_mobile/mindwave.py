from bluetooth.btcommon import BluetoothError
from parser import Parser
import bluetooth
import json
import time

class MindwaveBluetooth:

    def __init__(self, mac_addr=None):
        self.address = mac_addr
        self.bluetooth_socket = None
        self.parser = Parser(record_readings=True)
        self.connected = False

        if self.address is None:
            self.connect_magic()
        else:
            self.connect(self.address)
    
    def connect(self, addr):
        for i in range(5):
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            try:
                sock.connect((addr, 1))
                sock.setblocking(False)
            except BluetoothError, e:
                print e
            else:
                self.bluetooth_socket = sock
                self.connected = True
                break
            finally:
                time.sleep(1)

    def connect_magic(self):
        """ Tries to connect to the first MindWave Mobile it can find"""
        nearby_devices = bluetooth.discover_devices(lookup_names = True, duration=5)

        for addr, name in nearby_devices:
            if name == "MindWave Mobile":
                print("Found Mindwave Mobile at %s. Attempting to connect" % addr)
                connect(addr)

    def autoconnect(self):
        """Assumes that the bluetooth socket is attached to the mindwave"""
        AUTOCONNECT_CODE = "\xc2"
        self.bluetooth_socket.send(AUTOCONNECT_CODE)

    def disconnect(self):
        DISCONNECT_CODE = "\xc2"
        self.bluetooth_socket.send(DISCONNECT_CODE)

    def update(self, byte_size=1000):
        data = self.bluetooth_socket.recv(byte_size)
        self.parser.parse(data)

    def write(self, data):
        self.bluetooth_socket.send(data)

    def get_meditation_value(self):
        return self.parser.current_meditation

    def get_attention_value(self):
        return self.parser.current_attention

    def get_blink_strength_value(self):
        return self.parser.current_blink_strength
        
