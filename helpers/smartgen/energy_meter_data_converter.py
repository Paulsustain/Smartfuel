import sys
sys.path.append('/home/pi/smarteye/helpers')
from helper import get_device_mac_address as get_mac_address
import struct
import datetime as dt

def process_energy_data(energy_meter_data,flowmeter_data=None):
    #serial_number=energy_meter_data[1]['serial_number']
    #equipment_id=energy_meter_data[1]['equipment']
    ct=dt.datetime.now()
    current_time = ct.strftime('%Y-%m-%d %H:%M:%S')
    print('date time is: {}'.format(current_time))
    energy_meter_payload={"timestamp":current_time,"mac_address":get_mac_address()}
    energy_meter_payload.update(energy_meter_data[0])
    print('This is energy meter payload: {}'.format(energy_meter_payload))
    return energy_meter_payload
    print(energy_meter_payload)
