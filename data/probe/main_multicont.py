import serial.tools.list_ports
import time
import json
import datetime
import sys

sys.path.append('/home/pi/smarteye/helpers')
import helper
from atg import info_multicont
import sqlite3

sys.path.append('/home/pi/smarteye/services/atg')
import sqlite_service

sys.path.append('/home/pi/smarteye/helpers')
import main_logger
my_logger=main_logger.get_logger(__name__)


def get_mtc_tank_config():
    tank_config = json.loads(sqlite_service.get_device_config_by_slug('TANK_DETAILS')[0])
    mtc_tanks = [tank for tank in tank_config if tank['Tank_controller'] == 'MTC']
    return mtc_tanks

def query_probes():
    #store all connected ports in a list
    #portsInfo = serial.tools.list_ports.comports()
    
    #ComPorts = []
    #for i in range(len(portsInfo)):
    #    ComPorts.append(portsInfo[i].device)

    #USB PORTS
    #usbPorts = [port for port in ComPorts if 'USB' in port]
    #print(usbPorts)
    #er = []  #List of objects of Serial instances
    
    conn = serial.Serial(
            port='/dev/MTC_SERIAL',
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        #ser.append(conn)
    #print(conn)
    MAC = helper.get_device_mac_address()
    #MAC="b8:27:eb:fb:31:fc"
    print(MAC)
    mtc_tanks = get_mtc_tank_config()
    print(mtc_tanks)
    my_logger.debug(mtc_tanks)
    #mtc_tanks = [{'Controller_polling_address': 2, 'Tank_index': 1}]
    for tank in mtc_tanks: 
        try:
            cont_address = tank['Controller_polling_address']
            tank_index = tank['Tank_index']
            Var = info_multicont.multiCont_Var()	
            command = Var.command(cont_address, tank_index-1) #multicont tank address is zero-indexed, but our tank index from config is 1-indexed
            conn.write(bytearray(command))
            time.sleep(0.8)
            res = conn.read(size=conn.in_waiting)
            data = Var.responseData(res)
            my_logger.debug('the data obtained from probe in Tank: {} is: {}'.format(tank_index,data))
            #determine the flag type based on last enterted value
            cursor = sqlite_service.get_last_entered_pv_value(data['PV'][0]['Tank'], data['PV'][0]['MultiCONT'],'MTC' )
            last_pv = 0
            print(cursor)
            my_logger.debug('last pv from db for tank: {} is: {}'.format(tank_index,cursor))
            if cursor:
                for (value) in cursor: 
                        last_pv = float(value)

            pv_flag = 0
            #print(data['PV'][0]['Value'])
            print('last pv '+' '+str(last_pv)+' new '+str(data['PV'][0]['Value']))
            if (last_pv-5 <= data['PV'][0]['Value'] <= last_pv+10):
                    pv_flag = 1 #same value

            elif(data['PV'][0]['Value'] < last_pv-5):
                    pv_flag = 2 #consumption
            
            else:#(data['PV'][0]['Value'] > last_pv+10):
                    #Tolerance of 10 litres to account for noise
                    pv_flag = 3 #delivery

            log = {
            "read_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "device_address": MAC,
            "multicont_polling_address": data['PV'][0]['MultiCONT'],
            "tank_index": data['PV'][0]['Tank'],
            "pv": data['PV'][0]['Value'],
            "pv_flag": pv_flag,
            "sv": data['SV'][0]['Value'],
            "controller_type" : 'MTC'
            }
            print(log)
            my_logger.debug('logs to be inserted in db is: {}'.format(log))
            print('****got here****')
            if float(log['pv']) >= 1 or float(log['sv']) >= 1:
                try:
                    sqlite_service.mtc_probe_log_insert_one(log)
                    sqlite_service.update_tank_latest_reading(log)
                    my_logger.debug('Multicont Insert done successfully')
                except Exception as e:
                    my_logger.debug(e)
        except IndexError:
            log = {}
           
                            

def main():
    query_probes()

 
if __name__ == '__main__':
    main()















