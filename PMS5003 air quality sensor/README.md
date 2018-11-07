# PMS5003
* Air quality sensor, requires 5V supply so sensor using USB power supply.
* Publishes data over UART
* WIPY expansion board connections: P3 (G24 & TX) & P4 (G11 & RX)
* Modified the code from https://learn.adafruit.com/pm25-air-quality-sensor/circuitpython-code
* Important advice: use a unique `client_id` for each device on your MQTT network.

<p align="center">
<img src="https://github.com/robmarkcole/pycom-projects/blob/master/PMS5003%20air%20quality%20sensor/pms_wipy.jpg" width="500">
</p>


<p align="center">
<img src="https://github.com/robmarkcole/pycom-projects/blob/master/PMS5003%20air%20quality%20sensor/pms_atom.png" width="800">
</p>

## Home-Assistant
For MQTT broker I am using the Hassio [MQTT Server & Web client](https://github.com/hassio-addons/addon-mqtt/blob/master/README.md) addon with config:

```yaml
{
  "log_level": "info",
  "certfile": "",
  "keyfile": "",
  "web": {
    "enabled": true,
    "username": "xxx",
    "password": "xxx",
    "ssl": false
  },
  "broker": {
    "enabled": true,
    "enable_ws": true,
    "enable_mqtt": true,
    "enable_ws_ssl": false,
    "enable_mqtt_ssl": false,
    "allow_anonymous": true
  },
  "mqttusers": [
    {
      "username": "xxx",
      "password": "xxx",
      "readonly": false,
      "topics": [
        "#"
      ]
    }
  ]
}
```
Note that the addon web UI requires port 1884

In my HA config, to add the pycom board MQTT feed, publishing to port 1883 I have:

```yaml
mqtt:
  client_id : homeassistant
  broker : my_broker_ip
  username : xxx
  password : xxx
  port : 1883

sensor:
  - platform: mqtt
    state_topic: "wipy/"
```
