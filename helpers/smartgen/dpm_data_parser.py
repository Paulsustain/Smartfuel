import struct
from serial import Serial
import serial
from crccheck.crc import Crc16Modbus as crc_modbus
from time import sleep

def get_crc(data_byte):
    tester=0xff
    crc_byte=bytearray([])
    crc_int=crc_modbus.calc(data_byte)
    temp=crc_int&tester
    print(hex(temp),temp)
    crc_byte.append(temp)
    temp=(crc_int&(tester<<8))>>8
    print(hex(temp),temp)
    crc_byte.append(temp)
    print(crc_byte)
    return crc_byte

def write_data(client,combined_command):
    received_data=''
    try:
        crc=get_crc(combined_command)
        print(crc.hex())
        combined_command+=crc
        print(combined_command.hex())
        for _ in range(2):
            client.write(combined_command)
            print( "write successful")
            sleep(0.1)
            received_data=client.read(1)
            print('received_data is: {}'.format(received_data))
            while(client.inWaiting()):
                received_data+=client.read()
            print(received_data.hex())
    except Exception as e:
        print(e)
    return received_data

def get_phase_voltage(client,address):
   command=bytearray([address,0x03,0x01,0x00,0x00,0x08])
   voltage_data=write_data(client,command)
   voltage_a= struct.unpack('>f',reverse_byte(voltage_data[3:7]))[0]
   voltage_b= struct.unpack('>f',reverse_byte(voltage_data[7:11]))[0]
   voltage_c= struct.unpack('>f',reverse_byte(voltage_data[11:15]))[0]
   voltage_av= struct.unpack('>f',reverse_byte(voltage_data[15:19]))[0]
   phase_voltage={
       'voltage_a':voltage_a,
       'voltage_b':voltage_b,
       'voltage_c':voltage_c,
       'voltage_av':voltage_av
       }
   return phase_voltage

def get_energy_data(client,address):
   command=bytearray([address,0x03,0x01,0x5C,0x00,0x10])
   energy_data=write_data(client,command)
   active_energy_delivered= struct.unpack('>I',reverse_byte(energy_data[3:7]))[0]
   active_energy_received= struct.unpack('>I',reverse_byte(energy_data[7:11]))[0]
   reactive_energy_delivered= struct.unpack('>I',reverse_byte(energy_data[11:15]))[0]
   reactive_energy_received= struct.unpack('>I',reverse_byte(energy_data[15:19]))[0]
   apparent_energy_delivered= struct.unpack('>I',reverse_byte(energy_data[19:23]))[0]
   apparent_energy_received= struct.unpack('>I',reverse_byte(energy_data[23:27]))[0]
   sum_active_energy= struct.unpack('>I',reverse_byte(energy_data[27:31]))[0]
   diff_active_energy= struct.unpack('>i',reverse_byte(energy_data[31:35]))[0]
   energy={
       'active_energy_delivered':active_energy_delivered,
       'active_energy_received': active_energy_received,
       'reactive_energy_delivered':reactive_energy_delivered,
       'reactive_energy_received':reactive_energy_received,
       'apparent_energy_delivered':apparent_energy_delivered,
       'apparent_energy_received':apparent_energy_received,
       'sum_active_energy':sum_active_energy,
       'diff_active_energy':diff_active_energy,
       }
   return energy

def get_active_power(client,address):
   command=bytearray([address,0x03,0x01,0x44,0x00,0x08])
   power_data=write_data(client,command)
   power_total= struct.unpack('>f',reverse_byte(power_data[3:7]))[0]
   power_a= struct.unpack('>f',reverse_byte(power_data[7:11]))[0]
   power_b= struct.unpack('>f',reverse_byte(power_data[11:15]))[0]
   power_c= struct.unpack('>f',reverse_byte(power_data[15:19]))[0]
   phase_power={
       'power_a':power_a,
       'power_b':power_b,
       'power_c':power_c,
       'power_total':power_total
       }
   return phase_power

def reverse_byte(bytes_data):
    #print('normal bytes is: {}'.format(bytes(bytes_data).hex()))
    reversed_data=[]
    for x in range(len(bytes_data)-2,-1,-2):
        reversed_data.append(bytes_data[x])
        reversed_data.append(bytes_data[x+1])
    #print('reversed bytes is: {}'.format(reversed_data))
    return bytearray(reversed_data)

def get_phase_current(client,address):
   command=bytearray([address,0x03,0x01,0x20,0x00,0x08])
   current_data=write_data(client,command)
   current_a= struct.unpack('>f',reverse_byte(current_data[3:7]))[0]
   current_b= struct.unpack('>f',reverse_byte(current_data[7:11]))[0]
   current_c= struct.unpack('>f',reverse_byte(current_data[11:15]))[0]
   current_av= struct.unpack('>f',reverse_byte(current_data[15:19]))[0]
   phase_current={
       'current_a':current_a,
       'current_b':current_b,
       'current_c':current_c,
       'current_av':current_av
       }
   return phase_current

def get_line_voltage(client,address):
   command=bytearray([address,0x03,0x01,0x08,0x00,0x08])
   voltage_data=write_data(client,command)
   voltage_ab= struct.unpack('>f',reverse_byte(voltage_data[3:7]))[0]
   voltage_bc= struct.unpack('>f',reverse_byte(voltage_data[7:11]))[0]
   voltage_ac= struct.unpack('>f',reverse_byte(voltage_data[11:15]))[0]
   voltage_av= struct.unpack('>f',reverse_byte(voltage_data[15:19]))[0]
   line_voltage={
       'voltage_ab':voltage_ab,
       'voltage_bc':voltage_bc,
       'voltage_ac':voltage_ac,
       'voltage_av_line':voltage_av
       }
   return line_voltage

   
def get_average_phase_voltage(client,address):
   command=bytearray([address,0x03,0x01,0x07,0x00,0x02])
   av_pv_data=write_data(client,command)
   av_pv= struct.unpack('>f',av_pv_data[3:7])[0]
   return av_pv

def get_average_phase_current(client,address):
   command=bytearray([address,0x03,0x01,0x27,0x00,0x02])
   av_pc_data=write_data(client,command)
   av_pc= struct.unpack('>f',av_pc_data[3:7])[0]
   return av_pc

def get_average_line_voltage(client,address):
   command=bytearray([address,0x03,0x01,0x0F,0x00,0x02])
   av_lv_data=write_data(client,command)
   av_lv= struct.unpack('>f',av_lv_data[3:7])[0]
   return av_lv

def get_power_factor(client,address):
   command=bytearray([address,0x03,0x01,0x32,0x00,0x02])
   power_factor_data=write_data(client,command)
   power_factor= struct.unpack('>f',reverse_byte(power_factor_data[3:7]))[0]
   return {'power_factor':power_factor}

def get_frequency(client,address):
   command=bytearray([address,0x03,0x01,0x42,0x00,0x02])
   frequency_data=write_data(client,command)
   frequency= struct.unpack('>f',reverse_byte(frequency_data[3:7]))[0]
   return {'frequency':frequency}

