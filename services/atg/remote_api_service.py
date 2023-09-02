import sys
sys.path.append('/home/pi/smarteye/helpers/atg')
import sqlite_service
import re
import helper
import json
import datetime
import requests
from mysql.connector import MySQLConnection, Error

REMOTE_API_URL = 'https://api.smarteye.com.au/api/v1/'
def upload_probe_log():
     #get current local config for transmit interval
    transmit= json.loads(sqlite_service.get_device_config_by_slug('DEVICE_DETAILS')[0])['active']
    if transmit:
        data = sqlite_service.get_probe_logs_not_uploaded()
        id_list = []
        for value in data:
            id = []
            id.append(value[0])
            id_list.append(tuple(id))
         #print(data)
        try:
            if len(data) > 0:
                 json_data = json.dumps(data)
                 post_data = []
                 post_data.append(json_data)
                 print(json_data)
                 headers = {'Content-type': 'application/json'}
                 print(REMOTE_API_URL +'data_logger/')
                 r = requests.post(REMOTE_API_URL +'data_logger/', data = json_data, headers = headers)
                 if(r.status_code == 200):
                     print('data saved remotely')
                     sqlite_service.update_probe_logs_not_uploaded(id_list)
                 else:
                     print(r.content.decode())

            else:
             print('no item saved locally')         
        except Error as e:
            print('Error:', e)
        except Exception as e:
            print ('Exception:', e)
                
                
def upload_sensor_log():
    transmit= json.loads(sqlite_service.get_device_config_by_slug('DEVICE_DETAILS')[0])['active']
    if transmit:
        data = sqlite_service.get_sensor_logs_not_uploaded()
        id_list = []
        for value in data:
            id = []
            id.append(value[0])
            id_list.append(tuple(id))
         #print(data)
        try:
            if len(data) > 0:
                 json_data = json.dumps(data)
                 post_data = []
                 post_data.append(json_data)
                 print(json_data)
                 headers = {'Content-type': 'application/json'}
                 print(REMOTE_API_URL +'sensor_data_logger/')
                 r = requests.post(REMOTE_API_URL +'sensor_data_logger/', data = json_data, headers = headers)
                 if(r.status_code == 200):
                     print('data saved remotely')
                     sqlite_service.update_sensor_logs_not_uploaded(id_list)
                 else:
                     print(r.status_code)

            else:
             print('no item saved locally')         
        except Error as e:
            print('Error:', e)
        except Exception as e:
            print ('Exception:', e)

def get_device_config():
    MAC = helper.get_device_mac_address()
    #MAC="b8:27:eb:fb:31:fc"
    r = requests.post(REMOTE_API_URL+'devices/remote_config/', data={"mac_address": MAC})
    if(r.status_code == 200):
        return r.json()['data']
        
    else:
        return {}
        
        
def upload_delivery_log():
    #get current local config for transmit interval
    transmit= json.loads(sqlite_service.get_device_config_by_slug('DEVICE_DETAILS')[0])['active']
    if transmit:
        data = sqlite_service.get_probe_deliveries_not_uploaded()
        id_list = []
        for value in data:
            id = []
            id.append(value[0])
            id_list.append(tuple(id))
         #print(data)
        try:
            if len(data) > 0:
                 json_data = json.dumps(data)
                 post_data = []
                 post_data.append(json_data)
                 print(json_data)
                 headers = {'Content-type': 'application/json'}
                 r = requests.post(REMOTE_API_URL +'delivery_logger/', data = json_data, headers = headers)
                 if(r.status_code == 200):
                     print('data saved remotely')
                     sqlite_service.update_delivery_logs_not_uploaded(id_list)
                 else:
                     print(r.status_code)

            else:
             print('no item saved locally')         
        except Error as e:
            print('Error:', e)
        except Exception as e:
            print ('Exception:', e)

def main():
    print(upload_delivery_log())
 
#db_host = '34.246.63.12'
#db_username = 'niyio'
#db_password = 'tu@r7r7brA+a'
#db_name = 'station_manager'

db_host = '34.240.137.86'
db_username = 'samuel.j'
db_password = 'Tr-3re@Aza4r'
db_name = 'atg_integration_db'

if __name__ == '__main__':
    main()
