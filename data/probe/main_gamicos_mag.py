"""
This is gamicos module, it helps to get data from Gamicos probes.

Currently we have integrated the following probes:

1. Gamicos single float RS485
2. Gamicos double float RS485
3. Gamicos Ultrasonic
4. Gamicos Hydrostatic RS485

"""
import sys
sys.path.append('/home/pi/smarteye/helpers/atg')
import gamicos_parser as parser
import serial
from time import sleep
from datetime import datetime
sys.path.append('/home/pi/smarteye/helpers')
import main_logger
my_logger=main_logger.get_logger(__name__)
client=serial.Serial(port='/dev/MTC_SERIAL',baudrate=9600,parity=serial.PARITY_NONE,timeout=1)

##print(sys.path)
##print('*' *20)
##print(parser.__file__)

#probe_address=
#probe_command='M36246\r\n'
def read_probe(address=1,controller_type='GMC-485-U'): #GMC-485-U stands for Gamicos Ultrasonic probe.
    """
        This function helps identify the probe and returns measured/read data.
    """
    probe_command=parser.get_read_command(address,controller_type)
    print('this is the command sent: {}'.format(probe_command.hex()))
    my_logger.debug('this is the command sent: {}'.format(probe_command.hex()))
    client.write(probe_command)
    sleep(1)
    start_time=datetime.now()
    received_data=client.read(1)
    while client.inWaiting():
        received_data+=client.read()
        sleep(0.05)
    current_time=datetime.now()
    print('this is the received data: {}'.format(received_data.hex()))
    my_logger.debug('this is the received data: {}'.format(received_data.hex()))
##        difference = current_time - start_time
##        if difference.total_seconds() >= 2: return None
##    print('time taken in seconds is: {}'.format(difference))
##    print('this is the received data: {}'.format(received_data))
    if not received_data:
        return None
    parsed_data=parser.parse(received_data,controller_type)
    print('parsed_data is: {}'.format(parsed_data))
    my_logger.debug('parsed_data is: {}'.format(parsed_data))
    #client.close()
    return parsed_data
    
if __name__ == '__main__':
    read_probe()

