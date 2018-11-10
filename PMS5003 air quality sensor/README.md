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

In my HA config, to add the pycom board MQTT feed, using a value_template to break-out the individual readings:

```yaml
mqtt:
  client_id : homeassistant
  broker : my_broker_ip
  username : xxx
  password : xxx
  port : 1883

  sensor:
    - platform: mqtt
      name: particles_03um
      state_topic: "wipy/"
      value_template: "{{ value_json.particles_03um }}"
      unit_of_measurement: 03um
    - platform: mqtt
      name: particles_05um
      state_topic: "wipy/"
      value_template: "{{ value_json.particles_05um }}"
      unit_of_measurement: 05um
    - platform: mqtt
      name: particles_10um
      state_topic: "wipy/"
      value_template: "{{ value_json.particles_10um }}"
      unit_of_measurement: 10um
    - platform: mqtt
      name: particles_25um
      state_topic: "wipy/"
      value_template: "{{ value_json.particles_25um }}"
      unit_of_measurement: 25um
    - platform: mqtt
      name: particles_50um
      state_topic: "wipy/"
      value_template: "{{ value_json.particles_50um }}"
      unit_of_measurement: 50um
    - platform: mqtt
      name: particles_100um
      state_topic: "wipy/"
      value_template: "{{ value_json.particles_100um }}"
      unit_of_measurement: 100um
```

<p align="center">
<img src="https://github.com/robmarkcole/pycom-projects/blob/master/PMS5003%20air%20quality%20sensor/ha_view.png" width="500">
</p>

## In use in the kitchen
I get good readings with the sensor in the kitchen, below next to the toaster.

<p align="center">
<img src="https://github.com/robmarkcole/pycom-projects/blob/master/PMS5003%20air%20quality%20sensor/toasting.jpg" width="500">
</p>

Analytics of the data are shown in [ha_data_analytics.ipynb](https://github.com/robmarkcole/pycom-projects/blob/master/PMS5003%20air%20quality%20sensor/ha_data_analytics.ipynb)
