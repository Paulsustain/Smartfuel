import sys
sys.path.append('/home/pi/smarteye/helpers')
from helper import get_device_mac_address as get_mac_address
import struct
import datetime as dt
def bin_to_float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

def process_power_data(power_meter_data):
    register=power_meter_data[0]
    address=power_meter_data[1]['address']
    serial_number=power_meter_data[1]['serial_number']
    equipment_id=power_meter_data[1]['equipment']
    current_high_byte=register.registers[0]
    current_low_byte=register.registers[1]
    total_byte=current_high_byte<<16|current_low_byte
    float_value_current=bin_to_float(bin(total_byte))
    print("The current value in float is: {0}".format(float_value_current))
    voltage_high_byte=register.registers[2]
    voltage_low_byte=register.registers[3]
    total_voltage_byte=voltage_high_byte<<16|voltage_low_byte
    float_value_voltage=bin_to_float(bin(total_voltage_byte))
    print("The voltage value in float is: {0}".format(float_value_voltage))
    power_high_byte=register.registers[4]
    power_low_byte=register.registers[5]
    total_power_byte=power_high_byte<<16|power_low_byte
    float_value_power=bin_to_float(bin(total_power_byte))
    print("The power value in float is: {0}".format(float_value_power))
    ct=dt.datetime.now()
    current_time = ct.strftime('%Y-%m-%d %H:%M:%S')
    print('date time is: {}'.format(current_time))
    power_meter_payload={"address":address,
                         "current":abs(float_value_current),
                         "voltage":abs(float_value_voltage),
                         "power":abs(float_value_power),
                         "timestamp":current_time,
                         "equipment":equipment_id,
                         "mac_address":get_mac_address()
                         }
    print('This is power meter payload: {}'.format(power_meter_payload))
    return power_meter_payload
