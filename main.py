import ujson
import sensor

def connect_and_subscribe():
    global client_id, mqtt_server
    client = MQTTClient(client_id, mqtt_server)
    client.connect()
    print('Connected to %s MQTT broker' % (mqtt_server))
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
        time.sleep(message_interval)
        temperature, humidity = sensor.read()
        reading = { 'temperature': temperature, 'humidity': humidity, 'name': sensor_name }
        client.publish(topic_pub, ujson.dumps(reading))
        print('Published', reading, 'to topic')
    except OSError as e:
        restart_and_reconnect()