import dht
import machine

pin_nbr = 14
pin = dht.DHT22(machine.Pin(pin_nbr, machine.Pin.IN, machine.Pin.PULL_UP))

def read():
    try:
        pin.measure()
        return pin.temperature(), pin.humidity()
    except:
        print('Could not read sensor :(')
        return None, None

if __name__ == '__main__':
    t, h = read()
    print('temperature:', t, 'humidity:', h)
