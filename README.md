# temp_sensor

This is a summary of my microcontrol project. The actual hardware is a esp 8266 NodeMCU microcontrol running micropython with a DHT22 sensor connected to it. 

<!-- Tutorial used: http://docs.micropython.org/en/latest/esp8266/quickref.html -->


## Installation

Download micropython distribution for the esp8266 board at http://micropython.org/download#esp8266.

Esptool will be used to load micropython to the esp8266. Install esptool with
```
$ pip install esptool
```

Erase the flash using the following command
```
$ python3 esptool.py --port /dev/tty.usbserial-1410 erase_flash
```
<!-- /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/esptool.py -->

Deploy the new firmware using
```
$ python3 esptool.py --port /dev/tty.usbserial-1410 --baud 460800 write_flash --flash_size=detect 0 esp8266-20190125-v1.10.bin 
```

### Connect to the esp8266

Connect to the esp8266 running micropython through the terminal using
```
$ screen /dev/tty.usbserial-1410 115200
```

Once you want to end your termminal session simply exit by entering
```
Ctrl-a then k then y 
```

### Get IP of microcontrol
...

### Download and upload of files
Use the Web REPL to download and upload files to the esp8266 device. Start by enabling Web REPL on the device by entering the following command and follow the instructions:
```
$ import webrepl_setup
```

Clone Git repo https://github.com/micropython/webrepl to your computer or use the online web UI at http://micropython.org/webrepl/. This will enable you to download and upload files to the device.


To upload a file throught the command line using webrepl:
```
$ python3 webrepl_cli.py local-file-to-upload.py target-ip:uploaded-file-name.py
```

### Read values from the sensor
There seems to be a problem reading sensor values with 
´´´
pin = dht.DHT22(machine.Pin(2))
pin.measure()
´´´
after a reset of the microcontrol. This is normally fixed for some reason after re-wiring the sensor on the microcontrol.

### Problem with uploading files
Sometimes when trying to upload/download files with webrepl I get Connection refused. It seems like webrepl on the deamon on the microcontrol stopped. To get pass this I simply restart webrepl on the microcontrol
```
>>> import webrepl
>>> webrepl.start()
```