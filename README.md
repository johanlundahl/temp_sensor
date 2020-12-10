# Temp Sensor

This is a summary of my microcontrol project. The actual hardware is a esp 8266 NodeMCU microcontrol running micropython with a DHT22 sensor connected to it. Once its setup the microcontrol will publish temperature and humidity to a MQTT broker.

This project is suitable to run on a Raspberry Pi and is intended to use with [Home Monitor](http://github.com/johanlundahl/home_monitor), [Home Store](http://github.com/johanlundahl/home_store), [Home Eye](http://github.com/johanlundahl/home_eye) and [Mosquitto MQTT Broker](https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/).

![NodeMCU and DHT22](img/nodemcu_dht22.jpg)

<!-- Tutorial used: http://docs.micropython.org/en/latest/esp8266/quickref.html -->

## Wire the thing
Connect the DHT22 sensor to the ESP8266 according to:
* the `VCC` pin (marked `+`) connects to a `3V` pin on the microcontrol 
* the `DATA` pin (marked `Out`) connects to the `D5` pin (i.e. `GPIO14`) on the microcontrol
* the `GND` pin (marked `-`) connects to a `G` pin on the microcontrol

If the microcontrol shall be powered by battery then the `Do` pin (i.e. `GPIO16`) needs to connect to the `RST` pin so that the microcontrol can wake itself up. If you will power the microcontrol by USB then jump to the next section. See this [blog post](
https://randomnerdtutorials.com/micropython-esp8266-deep-sleep-wake-up-sources/) for more information on deep sleep and wake up functionality.

## Install MicroPython

Clone this git repo

```
$ git clone https://github.com/johanlundahl/temp_sensor
```

Esptool will be used to load micropython to the esp8266. Install this and all other required python modules
```
$ sudo pip3 install -r requirements.txt
```

Connect the esp8266 with USB. Erase the flash using the following command
```
$ sudo python3 esptool.py --port /dev/tty.usbserial-1410 erase_flash
```
<!-- /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/esptool.py -->

Download micropython distribution for the esp8266 board at http://micropython.org/download/esp8266/. Deploy the downloaded firmware using
```
$ sudo python3 esptool.py --port /dev/tty.usbserial-1410 --baud 460800 write_flash --flash_size=detect 0 esp8266-20190125-v1.10.bin 
```

## Setup the application on the microcontrol

### File transfers

Use the Web REPL to download and upload files to the esp8266 device. This will enable you to download and upload files to the device. Files can be uploaded or downloaded with or without wire.

#### Using Wifi
A fresh install of MicroPython has a Wifi AP. Read the following to figure out the IP of the microcontrol and how to connect to it http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#wifi

When connected to the Wifi of the microcontrol then files can be downloaded and uploaded with the online web UI at http://micropython.org/webrepl/.

1. Open http://micropython.org/webrepl/ in a browser with Internet connection
2. Connect to microcontrol wifi
3. Connect and give the password
4. Download a file that you want to edit
5. Upload the changed file
6. Restart the microcontrol using

```
>>> import machine
>>> machine.reset()
```

#### Using wire

Clone Git repo https://github.com/micropython/webrepl to your computer. 

Start by enabling Web REPL on the device by entering the following command and follow the instructions:
```python
$ import webrepl_setup
```

To download a file through the command line using webrepl:
```
$ python3 webrepl_cli.py target-ip:file-to-download.py .
```

To upload a file throught the command line using webrepl:
```
$ python3 webrepl_cli.py local-file-to-upload.py target-ip:uploaded-file-name.py
```

### Upload application

Make sure to specify the correct values in the config.py file so that the microcontrol will connect to the correct wifi and publish to right broker.

Edit the `temp_sensor/config.py` to set the following configuration parameters:
```python
wifi_name 			= 'wifi-ssid-name'
wifi_password 		= 'wifi-password'
mqtt_server 		= 'ip-address-of-mqtt-broker'
topic_pub 			= b'mqtt-topic-name'
message_retry 		= 60 # seconds to wait between publish failures
deep_sleep_interval = 60 # seconds to set device in deep sleep
sensor_name 		= 'name-of-the-sensor'
```

Upload the following files according to the [download and upload of files](https://github.com/johanlundahl/temp_sensor#download-and-upload-of-files) section. Upload the following files to the microcontrol:

```
temp_sensor/
│   boot.py
│   config.py
│   main.py
│   sensor.py
│   umqttsimple.py
```

If the microcontrol is powered by a battery then upload `temp_sensor/main_battery.py` as `main.py`instead. 


### Connect using Terminal

To connect to the microcontrol you need to connect it using a USB wire. Connect to the esp8266 running micropython through the terminal using
```
$ screen /dev/tty.usbserial-1410 115200
```

Once you want to end your termminal session simply exit by entering
```
Ctrl-a then k then y 
```

### Get IP of microcontrol
The IP of the microcontrol is needed when uploading files to the microcontrol. Log on to the microcontrol and enter the following from the command line:
```python
>>> import network
>>> station = network.WLAN(network.STA_IF)
>>> print(station.ifconfig())
```

## Start the microcontrol
Once the microcontrol is powered up it will start automatically and publish values to the configured MQTT broker at the given interval.
