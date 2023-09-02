#!/usr/bin/env python
from time import sleep
from datetime import datetime
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import json
import sys
sys.path.append('/home/pi/smarteye/services/atg')
import sqlite_service
from datetime import datetime
sys.path.append('home/pi/smarteye/helpers')
import helper
import main_logger
my_logger=main_logger.get_logger(__name__)
# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT=0

client = ModbusClient(method='rtu', port='/dev/MTC_SERIAL', timeout=1,baudrate=9600)
status=client.connect()
print("connection status is: ",status)
log.debug("Reading Coils")

def get_analog_tank_config():
    tanks = json.loads(sqlite_service.get_device_config_by_slug('TANK_DETAILS')[0])
    analog_tanks_index = [tank['Tank_index'] for tank in tanks if tank['Control_mode'] == 'S']
    return analog_tanks_index


def get_converter_readings():
    MAC = helper.get_device_mac_address()
    channels=get_analog_tank_config()
    print(channels)
    my_logger.debug('these are the channels: {}'.format(channels))
    for channel in channels:
        try:
            print('channel is: {}'.format(channel))
            my_logger.debug('channel is: {}'.format(channel))
            retry=3
            for _ in range(retry):
                print(_)
                register = client.read_holding_registers(channel-1,1, unit=UNIT)
                if hasattr(register,'registers'):
                    register=register.registers[0]
                    break
            print('register is: {}'.format(register))
            my_logger.debug('register is: {}'.format(register))
            current= str(float(register)/100)
            payload = {
                'tank_index': channel,
                'device_address': MAC,
                'controller_address': 1,
                'controller_type': 'S',
                'current(mA)': current,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            my_logger.debug('the payload for channel: {} is {}'.format(channel,payload))
            if payload:
                try:
                    sqlite_service.hydrostatic_sensor_insert_one(payload)
                    print(payload)
                    my_logger.debug('data inserted successfully for tank: {}'.format(channel))
                except Exception as e:
                    print(e)
                    my_logger.exception(e)

                
        except Exception as e:
            print(e)
            client.close()
            my_logger.exception(e)

if __name__ == '__main__':
    get_converter_readings()



