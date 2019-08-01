import config
import ujson
import sensor

def connect_and_subscribe():
    global client_id
    client = MQTTClient(client_id, config.mqtt_server)
    client.connect()
    print('Connected to %s MQTT broker' % (config.mqtt_server))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        time.sleep(config.message_interval)
        temperature, humidity = sensor.read()
        reading = { 'temperature': temperature, 'humidity': humidity, 'name': config.sensor_name }
        client.publish(config.topic_pub, ujson.dumps(reading))
        print('Published', reading, 'to topic')
    except OSError as e:
        restart_and_reconnect()