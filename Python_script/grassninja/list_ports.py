#python3
#

from pyftdi.ftdi import Ftdi

Ftdi.show_devices()
resp = Ftdi.list_devices()
print(resp)
