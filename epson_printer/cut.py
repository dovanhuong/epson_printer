import os, time
from escpos.printer import Usb
p = Usb(0x04b8, 0x0e27,0)
p.cut()