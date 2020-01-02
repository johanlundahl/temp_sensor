import config
import ujson
import sensor
import utime

def connect_and_subscribe():
    global client_id
    client = MQTTClient(client_id, config.mqtt_server)
    client.connect()
    client.check_msg()  # handle messages form server
    print('Connected to', config.mqtt_server, 'MQTT broker with id', client_id)
    return client

def restart_and_reconnect():
    print('Resetting microcontrol...')
    time.sleep(10)
    machine.reset()

def deep_sleep(msecs):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP) #configure RTC.ALARM0 to be able to wake the device
    rtc.alarm(rtc.ALARM0, msecs)    # set RTC.ALARM0 to fire after Xmilliseconds, waking the device
    machine.deepsleep()

start_time = utime.time() 
try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

for i in range(3):
    try:
        time.sleep(config.message_retry)
        temperature, humidity = sensor.read()
        reading = { 'temperature': temperature, 'humidity': humidity, 'name': config.sensor_name }
        client.publish(config.topic_pub, ujson.dumps(reading))
        print('Published', reading, 'to topic on server', config.mqtt_server)
        break
    except OSError as e:
        print('Failing to read and send value:', e)

print('Disconnecting client...')
client.disconnect()

end_time = utime.time() 
execution_time = end_time - start_time

print('Deep sleep for', config.deep_sleep_interval-execution_time, 'seconds')
deep_sleep((config.deep_sleep_interval-execution_time)*1000)