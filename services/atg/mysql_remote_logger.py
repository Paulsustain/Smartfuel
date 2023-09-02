import sys
from mysql.connector import MySQLConnection, Error
sys.path.append('/home/pi/smarteye/helpers')
#from python_mysql_dbconfig import read_db_config
import sqlite_service
import re
import helper 
import datetime


def get_and_update_device_config():
    MAC = helper.get_device_mac_address()
    try:
        conn = MySQLConnection(user= db_username, password= db_password,
                                 host= db_host,
                                 database= db_name)
        if conn.is_connected():
            #MAC = re.escape(MAC)
            # execute remote
            query = "SELECT Active, transmit_interval FROM backend_devices  WHERE Device_unique_address = '"+MAC +"'"
            cursor = conn.cursor()
            cursor.execute(query)
            #cursor.fetchone()
            for (Active, transmit_interval ) in cursor:
                active = "{}".format(Active)
                interval= "{}".format(transmit_interval)
                if(int(active) >= 0 and int(interval) > 0 ):
                        #print(active)
                        config_dict = {"active": active, "transmit_interval": interval}
                        sqlite_service.update_device_config(config_dict)
                        return config_dict
            
            cursor.close()
            conn.close()

    except Error as e:
        print('Error:', e)
    except Exception as e:
        print ('Exception:', e)


def send_heartbeat_message_to_remote_server():
    MAC = helper.get_device_mac_address()
    ip_address = helper.get_device_ip_address()
    try:
        conn = MySQLConnection(user=db_username, password= db_password,
                                 host= db_host,
                                 database= db_name)
        if conn.is_connected():
            #MAC = re.escape(MAC)
            # execute remote
            last_time_online = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "UPDATE device_heartbeats SET last_time_online = '"+last_time_online+"', local_ip = '"+ip_address+"'  WHERE device_mac_address = '"+MAC +"'"
            cursor = conn.cursor()
            cursor.execute(query)
            print("updated")
            #cursor.fetchone()
            
            print(cursor.rowcount)
            if( cursor.rowcount == 0 ):
                print("inserted")
                query = "INSERT INTO device_heartbeats (last_time_online,device_mac_address,local_ip) VALUES(%s,%s,%s)"
                cursor = conn.cursor()
                cursor.execute(query, (last_time_online, MAC, ip_address, ))

            conn.commit()
            cursor.close()
            conn.close()    
                       
    except Error as e:
        print('Error:', e)
    except Exception as e:
        print ('Exception:', e)


def send_current_firmware_version_to_remote_server(version_number):
    MAC = helper.get_device_mac_address()
    try:
        conn = MySQLConnection(user=db_username, password= db_password,
                                 host= db_host,
                                 database= db_name)
        if conn.is_connected():
            #MAC = re.escape(MAC)

            last_time_online = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "UPDATE device_firmware_version SET version_number = '"+version_number+"', updated_at = '"+last_time_online+"'  WHERE device_mac_address = '"+MAC +"'"
            cursor = conn.cursor()
            cursor.execute(query)
                  
            if( cursor.rowcount  == 0 ):
                print("created new")
                query = "INSERT INTO device_firmware_version (version_number,device_mac_address) VALUES(%s,%s)"
                cursor = conn.cursor()
                cursor.execute(query, (version_number, MAC, ))

            conn.commit()   
            cursor.close()
            conn.close()

                       
    except Error as e:
        print('Error:', e)
    except Exception as e:
        print ('Exception:', e)


def upload_atg_reading():
    data = sqlite_service.get_atg_readings_not_uploaded()
    try:
        #db_config = read_db_config()
        #conn = MySQLConnection(**db_config)
        conn = MySQLConnection(user=db_username, password= db_password,
                                 host= db_host,
                                 database= db_name)
       
        if conn.is_connected():
            # execute remote
            query = "INSERT INTO atg_readings(local_id,read_at,log) VALUES(%s,%s,%s)"
            cursor = conn.cursor()
            cursor.executemany(query, data)
            # update local
            sqlite_service.update_atg_readings_not_uploaded(data)

            conn.commit()
            cursor.close()
            conn.close()

    except Error as e:
        print('Error:', e)
    except Exception as e:
        print ('Exception:', e)

def upload_probe_log():
    #get current local config for transmit interval
    transmit= sqlite_service.get_device_config_by_slug('CAN_TRANSMIT')
    for (value) in transmit: 
        can_transmit = int(value[0])
        if(can_transmit == 1):
            data = sqlite_service.get_probe_logs_not_uploaded()
            print(data)
            try:
                #db_config = read_db_config()
                #conn = MySQLConnection(**db_config)
                conn = MySQLConnection(user=db_username, password=db_password,
                                                host=db_host,
                                                database=db_name)
                
                if conn.is_connected():
                # execute remote
                    query = "INSERT INTO atg_primary_log (local_id, read_at, pv,pv_flag, sv, device_address, multicont_polling_address, tank_index, tc_volume, water, temperature, controller_type ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor = conn.cursor()
                    cursor.executemany(query, data)
                    # delete local
                    sqlite_service.update_probe_logs_not_uploaded(data)
                    sqlite_service.delete_probe_logs_after_upload(data)
                    conn.commit()
                    cursor.close()
                    conn.close()

                    print('saved')
            except Error as e:
                print('Error:', e)
            except Exception as e:
                print ('Exception:', e)



def get_latest_firmware_version_details(version_number):
    try:
        conn = MySQLConnection(user= db_username, password= db_password,
                                 host= db_host,
                                 database= db_name)
        if conn.is_connected():
            # execute remote
            query = "SELECT download_link, version_number, file_name FROM smarteye_firmware_log  where version_number = '"+version_number+"' LIMIT 1"
            cursor = conn.cursor()
            cursor.execute(query)
            #cursor.fetchone()
            for (download_link, version_number, file_name ) in cursor:
                v_n = "{}".format(version_number)
                d_l= "{}".format(download_link)
                f_n= "{}".format(file_name)
                config_dict = {"version_number": v_n, "download_link": d_l, "file_name": f_n}
                #sqlite_service.update_device_config(config_dict)
                return config_dict

            cursor.close()
            conn.close()

    except Error as e:
        print('Error:', e)
    except Exception as e:
        print ('Exception:', e)

    
def get_device_expected_version():
    MAC = helper.get_device_mac_address()
    try:
        conn = MySQLConnection(user= db_username, password= db_password,
                                 host= db_host,
                                 database= db_name)
        if conn.is_connected():
            # execute remote
            query = "SELECT version_number, expected_version_number FROM device_firmware_version  where device_mac_address = '"+MAC+"' LIMIT 1"
            cursor = conn.cursor()
            cursor.execute(query)
            #cursor.fetchone()
            for (version_number, expected_version_number ) in cursor:
                v_n = "{}".format(expected_version_number)
                config_dict = {"expected_version_number": v_n}
                #sqlite_service.update_device_config(config_dict)
                return config_dict

            cursor.close()
            conn.close()

    except Error as e:
        print('Error:', e)
    except Exception as e:
        print ('Exception:', e)


def upload_at_command_info():
    #get current local config for transmit interval
    MAC = helper.get_device_mac_address()
    transmit= sqlite_service.get_device_config_by_slug('CAN_TRANSMIT')
    for (value) in transmit: 
        can_transmit = int(value[0])
        if(can_transmit == 1):
            data = sqlite_service.get_at_command_info()
            mac = data[0][0]
            data_1 = list(data[0])
            
            try:
                #db_config = read_db_config()
                #conn = MySQLConnection(**db_config)
                conn = MySQLConnection(user=db_username, password=db_password,
                                                host=db_host,
                                                database=db_name)
                
                if conn.is_connected():
                # execute remote
                    last_time_online = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data_1.append(last_time_online)
                    query = "INSERT INTO at_command_info (device_address, network_provider,phone_number,data_balance,signal_strength,signal_level,log_time,airtime_balance,db_fill_time) VALUES(%s,%s,%s,%s,%s,%s,%s, %s, %s) ON DUPLICATE KEY UPDATE network_provider = VALUES(network_provider),phone_number =  VALUES(phone_number),data_balance =  VALUES(data_balance), signal_strength = VALUES(signal_strength),signal_level = VALUES(signal_level),log_time = VALUES(log_time), airtime_balance = VALUES(airtime_balance),db_fill_time= VALUES(db_fill_time)"
                    cursor = conn.cursor()
                    cursor.execute(query, data_1)
                    # delete local
                    conn.commit()
                    cursor.close()
                    conn.close()

                    print('saved')
            except Error as e:
                print('Error:', e)
            except Exception as e:
                print ('Exception:', e)                                                                                                         
 
def main():
    upload_probe_log()
 

db_host = '34.240.137.86'
db_username = 'samuel.j'
db_password = 'Tr-3re@Aza4r'
db_name = 'atg_integration_db'

if __name__ == '__main__':
    main()
