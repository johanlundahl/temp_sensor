import config
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
import webrepl

client_id = ubinascii.hexlify(machine.unique_id())
station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(config.wifi_name, config.wifi_password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())

webrepl.start()
