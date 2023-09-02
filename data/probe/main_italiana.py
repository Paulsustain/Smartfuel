import sys
sys.path.append('/home/pi/smarteye/helpers/atg')
import italiana_parser as parser
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
def read_probe(address='36246'): #Each Italiana probe has a unique probe address.
    """
        This function helps identify the probe address and returns measured/received data.
    """
    probe_command='M{}\r\n'.format(address)
    byte_to_send=probe_command.encode()
    print('this is the command sent: {}'.format(byte_to_send.hex()))
    my_logger.debug('this is the command sent: {}'.format(byte_to_send.hex()))
    client.write(byte_to_send)
    sleep(0.1)
    start_time=datetime.now()
    received_data=client.read(1)
    while received_data.find(b'\n\r') == -1:
        received_data+=client.read()
        current_time=datetime.now()
        difference = current_time - start_time
        if difference.total_seconds() >= 2: return None
    print('time taken in seconds is: {}'.format(difference))
    print('this is the received data: {}'.format(received_data))
    my_logger.debug('this is the received data: {}'.format(received_data))
    parsed_data=parser.parse(received_data)
    print('parsed_data is: {}'.format(parsed_data))
    my_logger.debug('parsed_data is: {}'.format(parsed_data))
    client.close()
    return parsed_data
    
if __name__ == '__main__':
    read_probe()
