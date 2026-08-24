import machine
from onewire import OneWire
from ds18x20 import DS18X20
from time import sleep, sleep_ms

from config import DS18B20_PIN, PHOTO_PIN

class Sensors:
    def __init__(self):
        # DS18B20 
        machine.Pin(DS18B20_PIN, machine.Pin.OUT, value=1)
        self.sensor_ds = DS18X20(OneWire(machine.Pin(10)))
        self.device = self.sensor_ds.scan()
        
        # PHOTORESITOR
        self.photo = machine.ADC(PHOTO_PIN)
    
    def ds18b20(self):
        # MEASURE TEMP
        self.sensor_ds.convert_temp()
        return self.sensor_ds.read_temp(self.device[0])
    
    def photoresitor(self):
        # MEASURE BRIGTHNESS
        value = self.photo.read_u16()
        value = round(value/65535*100)
        return value

