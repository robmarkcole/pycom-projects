# main.py -- put your code here!
import pycom
from network import WLAN
pycom.heartbeat(False)
pycom.rgbled(0x00ff00) # make green

wlan = WLAN()