# PMS5003
* Air quality sensor, requires 5V supply so USB power supply.
* Publishes data over UART
* WIPY connections: P3 (G24) & P4 (G11)

To print byte stream, no imports required:
```python
import os
import machine
import pycom
import time

# Configure first UART bus to see the communication on the pc
uart = machine.UART(0, 115200)
os.dupterm(uart)

# Configure second UART bus on pins P3(TX1) and P4(RX1)
uart1 = machine.UART(1, baudrate=9600)
pycom.heartbeat(False)

while True:
    print(uart1.readline())  # read the response from the Arduino
    time.sleep(1)
```
