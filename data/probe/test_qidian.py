#!/usr/bin/env python
from time import sleep
from datetime import datetime
"""
Pymodbus Synchronous Client Examples
--------------------------------------------------------------------------

The following is an example of how to use the synchronous modbus client
implementation from pymodbus.

It should be noted that the client can also be used with
the guard construct that is available in python 2.5 and up::

    with ModbusClient('127.0.0.1') as client:
        result = client.read_coils(1,10)
        print result
"""
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# from pymodbus.client.sync import ModbusUdpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

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
##rr = client.read_holding_registers(30, 1, unit=UNIT)
##log.debug(rr)
##print(rr)
##sleep(3)
##rr = client.read_coils(0, 1, unit=255)
##log.debug(rr)
##print(rr)
while True:
    try:
        #print(k)
        rr = client.read_holding_registers(0,4, unit=UNIT)
        #print(rr)
        
#        #rr = client.read_holding_registers(26,2, unit=UNIT)
#        #rr = client.read_holding_registers(11,1, unit=UNIT)
#        #rr = client.read_holding_registers(50,10, unit=UNIT)
        print("this is rr: {}".format(rr))
#        #log.debug(rr)
#        #for k in range(10):
#        ##rr = client.read_holding_registers(0,81, unit=UNIT)
#            #print('this is from DFM '+str(k)+'th register',rr.registers[k])
###        for k in range(81):
###            print('this is from DFM '+str(k)+'th register',rr.registers[k])
        for index,registers in enumerate(rr.registers):
            #print(index,registers)
            current_val= float(registers)/100
            print('current value of channel {} is: {}'.format(index,current_val))
        print('read at: {}'.format(datetime.now()))
#        total_liters=(high_word+low_word)/1000
#        print("total fuel consumed  for flowmeter with address {} is: {}".format(UNIT,total_liters))
#        high_word=rr.registers[26]
#        #print("high word is: {}".format(high_word))
#        low_word=rr.registers[27]
#        #print("low word is: {}".format(low_word))
###        lower_word=rr.registers[2]
###        print("low word is: {}".format(lower_word))
#        total_times=(high_word+low_word+lower_word)
#        print("total engine hours for flowmeter with address {} is: {}".format(UNIT,total_times))
        #print("DFM mode is {}".format(high_word))
        
    except Exception as e:
        print(e)
    sleep(5)
        #print(Exception)
##try:
##    #rr = client.read_holding_registers(4,2, unit=UNIT)
##    rr = client.read_holding_registers(0,81, unit=UNIT)
##    log.debug(rr)
##    for k in range(81):
##        print('this is from DFM '+str(k)+'th register',rr.registers[k])
####        high_word=rr.registers[0]
####        low_word=rr.registers[1]
####        total_liters=(high_word+low_word)/1000
####        print("total fuel consumed is: ",total_liters)
##    sleep(1)
##except Exception:
##    pass
##    #print(Exception)



