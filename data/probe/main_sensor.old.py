import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import json
import sys
sys.path.append('/home/pi/smarteye/services/atg')
import sqlite_service
from datetime import datetime
sys.path.append('home/pi/smarteye/helpers')
import helper
import traceback


def get_analog_tank_config():
    tanks = json.loads(sqlite_service.get_device_config_by_slug('TANK_DETAILS')[0])
    analog_tanks_index = [tank['Tank_index'] for tank in tanks if tank['Control_mode'] == 'S']
    return analog_tanks_index
class Sensor:
    def __init__(self):
        # Create the I2C bus
        self.channels = get_analog_tank_config()
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        self.ads = ADS.ADS1115(self.i2c)
        self.ads.gain=2/3
        self.controller_type='S'
        self.controller_address=1
    
    def calc_current(self,voltage):
        return voltage/250
    
    def adc_readings(self):
        MAC = helper.get_device_mac_address()
        print(self.channels)
        for ch in self.channels:
            try:
                chan = AnalogIn(self.ads, ch-1)
                voltage = chan.voltage
                current = self.calc_current(voltage)
                payload = {
                    'tank_index': ch,
                    'device_address': MAC,
                    'controller_address': self.controller_address,
                    'controller_type': self.controller_type,
                    'current(mA)': str(current*1000),
                    'voltage': str(voltage),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                if payload:
                    sqlite_service.adc_sensor_insert_one(payload)
                    print(payload)
                    
            except Exception:
                traceback.print_exc()

if __name__ == '__main__':
    Sensor().adc_readings()