import struct
#import crc16
from crccheck.crc import Crc16Modbus as crc_modbus

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
    
    if controller_type =='GMC-485-D':
##        command=bytearray([address,0x03,0x00,0x02,0x00,0x04,0xE5,0xC9])
        command=bytearray([address,0x03,0x00,0x02,0x00,0x04])
        command=command+get_crc(command)
        ##print(command)
    elif controller_type == 'GMC-485-S':
        #command=bytearray([address,0x03,0x00,0x02,0x00,0x04,0xE5,0xC9])
        command=bytearray([address,0x03,0x00,0x04,0x00,0x02])
        command=command+get_crc(command)
        ##print(command)
    elif controller_type == 'GMC-485-U':
        command=bytearray([address,0x03,0x00,0x01,0x00,0x08])
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
    else:
        return None
    #binary_to_float(data_list[3:7])
    
    
    
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
#    int_form=struct.unpack('l',main_data)[0]
#    #print('this is int form: {}'.format(int_form))
#    #print(struct.pack('>q',int_form))
    level=struct.unpack('>f',main_data[:4])[0]
    temperature=struct.unpack('>f',main_data[4:8])[0]
    sound=struct.unpack('>f',main_data[8:12])[0]
    current=struct.unpack('>f',main_data[12:16])[0]
    ##print('this is real data: ',real_data)
    parsed={
        'probe_address':address,
        'product_float_level':level*1000,
        'temperature':temperature,
        'water_float_level':0,
        #'sound':sound,
        #'current':current,
        #'crc':crc.hex()
        }
    return parsed
get_crc(bytearray([0x00,0x06,0x00,0x020,0x00,0x02]))    
    
