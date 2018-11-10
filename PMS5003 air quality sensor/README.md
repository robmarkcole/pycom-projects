# PMS5003
* PMS5003 Air quality sensor, see a teardown and technical info [here](https://aqicn.org/sensor/pms5003-7003/).
* Pick up online for cheap via [Amazon](https://www.amazon.co.uk/iHaospace-PMS5003-Digital-Particle-Detection/dp/B071J5LL8V/ref=sr_1_1?s=electronics&ie=UTF8&qid=1541838268&sr=1-1&keywords=pms5003) or [Ali-express](https://www.aliexpress.com/wholesale?catId=0&initiative_id=SB_20181110002531&SearchText=pms5003).
* Publishes data over serial (UART) - read data with Wipy on expansion board connections: P3 (G24 & TX) & P4 (G11 & RX)
* Wipy only optputs 3.3V but sensor requires 5V so power from USB using the GND/5V outputs on a [USB/UART connector](https://www.amazon.co.uk/gp/product/B01CYBHM26/ref=oh_aui_search_detailpage?ie=UTF8&psc=1).
* Modified the code from https://learn.adafruit.com/pm25-air-quality-sensor/circuitpython-code
* Important advice for MQTT: use a unique `client_id` for each device on your MQTT network.

<p align="center">
<img src="https://github.com/robmarkcole/pycom-projects/blob/master/PMS5003%20air%20quality%20sensor/pms_wipy.jpg" width="500">
</p>


<p align="center">
<img src="https://github.com/robmarkcole/pycom-projects/blob/master/PMS5003%20air%20quality%20sensor/pms_atom.png" width="1000">
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
I get good readings with the sensor in the kitchen, below next to the toaster. I'm powering the wipy and PMS5003 from a USB charge pack, which outputs at 5V.

<p align="center">
<img src="https://github.com/robmarkcole/pycom-projects/blob/master/PMS5003%20air%20quality%20sensor/toasting.jpg" width="800">
</p>

Analytics of the data are shown in [ha_data_analytics.ipynb](https://github.com/robmarkcole/pycom-projects/blob/master/PMS5003%20air%20quality%20sensor/ha_data_analytics.ipynb)
