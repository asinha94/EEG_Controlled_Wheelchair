import parser
import pyeeg
import sys

addr = "A0:E6:F8:F7:B9:58"
p = parser.Parser()
p.connect(addr)

if not p.device_connected:
    print("Couldn't connect to device connceted. Try again.")
    sys.exit(1)

while True:
    p.update()
    print("Blink Strength: %s" % str(p.current_blink_strength))
    


