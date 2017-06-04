import parser
import pyeeg
import sys
from time import sleep

addr = "A0:E6:F8:F7:B9:58"
p = parser.Parser()
p.connect(addr)

if not p.device_connected:
    print("Couldn't connect to device connceted. Try again.")
    sys.exit(1)

sleep(2)

while True:
    p.update()
    print("Blink Strength: %s" % str(p.current_blink_strength))
    print("Meditation    : %s" % str(p.current_meditation))
    print("Attention     : %s\n\n" % str(p.current_attention))
    sleep(1)
    


