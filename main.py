# main.py -- put your code here!
import pycom
import time
from network import WLAN
pycom.heartbeat(False)
pycom.rgbled(0x00ff00) # make green

wlan = WLAN()
print(wlan.isconnected())
