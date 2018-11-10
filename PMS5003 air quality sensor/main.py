import os
import machine
import pycom
import time
import struct
from ujson import dumps
from mqtt import MQTTClient
from machine import RTC

## LED
pycom.heartbeat(False)
GREEN = 0x001500
RED = 0x150000
pycom.rgbled(RED) # the default state.

# Setup MQTT
def settimeout(duration):
   pass

client_id = "wipy"
broker = "192.168.1.84"
user = "xxx"
password = "xxx"
port = 1883

client = MQTTClient(client_id=client_id,
                    server=broker,
                    user=user,
                    password=password,
                    port=port)

client.settimeout = settimeout

try:
    client.connect()
except Exception as e:
    print("Unable to connect to MQTT broker")
    print(e)

# Configure first UART bus to see the communication on the pc
uart = machine.UART(0, 115200)
os.dupterm(uart)
# Configure second UART bus on pins P3(TX1) and P4(RX1)
uart1 = machine.UART(1, baudrate=9600)

buffer = []

while True:
    data = uart1.read(32)  # read up to 32 bytes
    if data:
        data = list(data)
        buffer += data

    while buffer and buffer[0] != 0x42:
        buffer.pop(0)

    if len(buffer) > 200:
        buffer = []  # avoid an overrun if all bad data
    if len(buffer) < 32:
        continue

    if buffer[1] != 0x4d:
        buffer.pop(0)
        continue

    frame_len = struct.unpack(">H", bytes(buffer[2:4]))[0]
    if frame_len != 28:
        buffer = []
        continue

    frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:]))

    pm10_standard, pm25_standard, pm100_standard, pm10_env, \
        pm25_env, pm100_env, particles_03um, particles_05um, particles_10um, \
        particles_25um, particles_50um, particles_100um, skip, checksum = frame

    check = sum(buffer[0:30])

    if check != checksum:
        buffer = []
        continue

    data_dict = {}
    data_dict['particles_03um'] = particles_03um
    data_dict['particles_05um'] = particles_05um
    data_dict['particles_10um'] = particles_10um
    data_dict['particles_25um'] = particles_25um
    data_dict['particles_50um'] = particles_50um
    data_dict['particles_100um'] = particles_100um
    data_json = dumps(data_dict) # Get a json string.

    # Print/publish the data
    print(data_json)
    try:
        client.publish("wipy/", data_json)
        pycom.rgbled(GREEN)
        time.sleep(0.2)
        pycom.rgbled(RED)
        time.sleep(2)
    except Exception as e:
        print(e)
        pass

    buffer = buffer[32:]
