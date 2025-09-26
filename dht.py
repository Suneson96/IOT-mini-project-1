import time
import board
import adafruit_dht
import json
import atexit


class DHTSensor:
    def __init__(self, pin):
        self.dhtDevice = adafruit_dht.DHT11(pin)

    def read(self):
        try:
            temperature_c = self.dhtDevice.temperature
            temperature_f = round(temperature_c * (9 / 5) + 32, 1)
            humidity = self.dhtDevice.humidity
            return {
                "temperature_f": temperature_f,
                "temperature_c": temperature_c,
                "humidity": humidity
            }
        except RuntimeError as error:
            print(error.args[0])
            return {
                "temperature_f": None,
                "temperature_c": None,
                "humidity": None
            }
        except Exception as error:
            self.dhtDevice.exit()
            raise error

if __name__ == "__main__":
    Sensor = DHTSensor(board.D4)
    while True:
        data = Sensor.read()
        print(json.dumps(data))
        time.sleep(2.0)
