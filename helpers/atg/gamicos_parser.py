import struct
import sys
#import crc16
from crccheck.crc import Crc16Modbus as crc_modbus
sys.path.append('/home/pi/smarteye/services/atg')
import sqlite_service
import json

GAMICOS_UNIT_LIST={
                    0:"Mpa",
                    1:"kpa",
                    2:"pa",
                    3:"bar",
                    4:"mbar",
                    5:"kg/cm3",
                    6:"psi",
                    7:"mH20",
                    8:"mmH20",
                    9:"oC"
                    }

def get_crc(data_byte):
#    crc=crc16.crc16xmodem(bytes(data_byte))
#    #print('crc is: {}'.format(crc))
#    return crc
    tester=0xff
    crc_byte=bytearray([])
    crc_int=crc_modbus.calc(data_byte)
    temp=crc_int&tester
    #print(hex(temp),temp)
    crc_byte.append(temp)
    temp=(crc_int&(tester<<8))>>8
    #print(hex(temp),temp)
    crc_byte.append(temp)
    ##print(crc_byte)
    return crc_byte


def get_read_command(address,controller_type):
    
    if controller_type =='GMC-485-D': #GMC-485-D stands for Gamicos Magnetosrtictive double-float probe
##        command=bytearray([address,0x03,0x00,0x02,0x00,0x04,0xE5,0xC9])
        command=bytearray([address,0x03,0x00,0x02,0x00,0x04])
        command=command+get_crc(command)
        ##print(command)
    elif controller_type == 'GMC-485-S': #GMC-485-S stands for Gamicos Magnetosrtictive single-float probe
        #command=bytearray([address,0x03,0x00,0x02,0x00,0x04,0xE5,0xC9])
        #command=bytearray([address,0x03,0x00,0x04,0x00,0x02])
        command=bytearray([address,0x03,0x00,0x04,0x00,0x02])
        command=command+get_crc(command)
        ##print(command)
    elif controller_type == 'GMC-485-U': #GMC-485-U stands for Gamicos Ultrasonic probe
        command=bytearray([address,0x03,0x00,0x01,0x00,0x08])
        command=command+get_crc(command)
        ##print(command)
    elif controller_type == 'GMC-485-H': #GMC-485-H stands for Gamicos Hydrostatic probe RS485
        command=bytearray([address,0x03,0x00,0x02,0x00,0x03])
        command=command+get_crc(command)
        ##print(command)
    else:
        command=None
    return command

def parse(data,controller_type):
    if controller_type == 'GMC-485-S':
        return parse_single_float(data)
    elif controller_type == 'GMC-485-D':
        return parse_double_float(data)
    elif controller_type == 'GMC-485-U':
        return parse_ultrasonic(data)
    elif controller_type == 'GMC-485-H':
        return parse_hydrostatic_serial(data)
    else:
        return None
    #binary_to_float(data_list[3:7])
    
    
def parse_hydrostatic_serial(data):
    data_list=data
    #print(type(data_list))
    address=data_list[0]
    data_length=data_list[2]
    #print('data length is: {}'.format(data_length))
    unit=data_list[3]<<8|data_list[4]
    if unit == 1: print("unit is: {} which corresponds to kpa".format(unit))
    decimal_point_offset=data_list[5]<<8|data_list[6]
    decimal_point_offset=10**(-1*decimal_point_offset)
    #print('decimal part 1 is :{}'.format(float_2_decimal))
    real_time_measurement_value=data_list[7]<<8|data_list[8]
    sensor_output=real_time_measurement_value*decimal_point_offset
    data_dict={
            'probe_address':address,
            'unit':GAMICOS_UNIT_LIST[unit],
            'pressure':sensor_output,
            'decimal_point_offset':decimal_point_offset,
            'real_time_measurement_value':real_time_measurement_value
           }
    return data_dict

def parse_single_float(data):
    data_list=data
    #print(type(data_list))
    address=data_list[0]
    data_length=data_list[2]
    #print('data length is: {}'.format(data_length))
    float_2_int=data_list[3]<<8|data_list[4]
    float_2_decimal=data_list[5]<<8|data_list[6]
    #print('decimal part 1 is :{}'.format(float_2_decimal))
##    float_1_int=data_list[7]<<8|data_list[8]
##    float_1_decimal=data_list[9]<<8|data_list[10]
    #print('decimal part 2 is :{}'.format(float_1_decimal))
    #print('controller type is: {}'.format(controller_type))
    product_float_level= float_2_int+ float(float_2_decimal/65535)
    #water_float_level= float_1_int+ float(float_1_decimal/65535)
    data_dict={
            'probe_address':address,
#                'data_length':data_length,
            #'product_float_integer':float_2_int,
            #'product_float_decimal':float_2_decimal,
            #'water_float_integer':float_1_int,
            #'water_float_decimal':float_1_decimal,
            'product_float_level':product_float_level,
            'water_float_level':0,
#                'checksum':checksum
           }
    return data_dict


    
def parse_double_float(data):
    data_list=data
    #print(type(data_list))
    address=data_list[0]
    data_length=data_list[2]
    #print('data length is: {}'.format(data_length))
    float_2_int=data_list[3]<<8|data_list[4]
    float_2_decimal=data_list[5]<<8|data_list[6]
    #print('decimal part 1 is :{}'.format(float_2_decimal))
    float_1_int=data_list[7]<<8|data_list[8]
    float_1_decimal=data_list[9]<<8|data_list[10]
    #print('decimal part 2 is :{}'.format(float_1_decimal))
    #print('controller type is: {}'.format(controller_type))
    product_float_level= float_2_int+ float(float_2_decimal/65535)
    water_float_level= float_1_int+ float(float_1_decimal/65535)
    data_dict={
            'probe_address':address,
#                'data_length':data_length,
            #'product_float_integer':float_2_int,
            #'product_float_decimal':float_2_decimal,
            #'water_float_integer':float_1_int,
            #'water_float_decimal':float_1_decimal,
            'product_float_level':product_float_level,
            'water_float_level':water_float_level,
#                'checksum':checksum
           }

    return data_dict
    
def parse_ultrasonic(data):
    address=data[0]
    data_length=data[2]
    main_data=data[3:(3+data_length)]
    print(main_data.hex())
    crc=data[-2:]
    local_tank_config = json.loads(sqlite_service.get_device_config_by_slug('TANK_DETAILS')[0])
    print(local_tank_config)
    tank_height=None
    for tank in local_tank_config:
        if tank ['Tank_controller']== 'GMC-485-U':
            tank_height= tank['Tank_height']
#    int_form=struct.unpack('l',main_data)[0]
#    #print('this is int form: {}'.format(int_form))
#    #print(struct.pack('>q',int_form))
    level=struct.unpack('>f',main_data[:4])[0]
    temperature=struct.unpack('>f',main_data[4:8])[0]
    sound=struct.unpack('>f',main_data[8:12])[0]
    current=struct.unpack('>f',main_data[12:16])[0]
    ##print('this is real data: ',real_data)
    
    print('This is tank height: {}'.format(tank_height))
    if tank_height:
        level= (tank_height - (level*1000))
    else:
        level = level*1000
        print('no tank height!')
                
    parsed={ 
        'probe_address':address,
        'product_float_level': level,
        'temperature':temperature,
        'water_float_level':0,
        #'sound':sound,
        #'current':current,
        #'crc':crc.hex()
        }
    return parsed

if __name__ == "__main__":
    get_crc(bytearray([0x00,0x06,0x00,0x020,0x00,0x02]))    
    
