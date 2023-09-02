import datetime
import os
# Make it work for Python 2+3 and with Unicode
import io
import sqlite3
import sys
sys.path.append('/home/pi/smarteye/helpers')
import helper
import main_logger
my_logger=main_logger.get_logger(__name__)
db_path = '/home/pi/smarteye/db/atg/store.db'

# def atg_readings_insert_one(data):

# 	conn = sqlite3.connect(db_path)
# 	cur = conn.cursor()
# 	done = cur.execute("INSERT INTO atg_readings (read_at, log, uploaded) values (?, ?,?)", ( data['read_at'], data['log'], 0))
# 	conn.commit()
# 	conn.close()
# 	return done

# def get_atg_readings_not_uploaded():
# 	conn = sqlite3.connect(db_path)
# 	cur = conn.cursor()
# 	# result = cur.execute("SELECT log, read_at FROM atg_readings where uploaded = ? ", 0)
# 	result=cur.execute("SELECT id, read_at, log FROM atg_readings WHERE uploaded=?", (0))
# 	rows = result.fetchall()
# 	conn.commit()
# 	conn.close()
# 	return rows

# def update_atg_readings_not_uploaded(data):
# 	conn = sqlite3.connect(db_path)
# 	cur = conn.cursor()
# 	query = "UPDATE atg_readings SET uploaded = 1 where id = ? and read_at = ? and log = ?"
# 	result=cur.executemany(query, data)
# 	conn.commit()
# 	conn.close()
# 	return result

def tls_probe_delivery_insert_one(data):

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    done = cur.execute("INSERT INTO deliveries (read_at, device_address, polling_address, tank_index, volume, tc_volume, system_start_time, uploaded, system_end_time, start_height, end_height, start_volume, end_volume, controller_type) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    (data['read_at'], data['device_address'], data['polling_address'], data['tank_index'],
    data['volume'],data['tc_volume'], data['system_start_time'], 0, data['system_end_time'], data['start_height'], data['end_height'] , data['start_volume'], data['end_volume'], 'TLS'))
    conn.commit()
    conn.close()
    return done
    
def get_last_entered_delivery_volume_value(tank, polling_address, controller_type):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT volume FROM last_entered_delivery where tank_index = ? and polling_address = ? and controller_type = ? ORDER BY id DESC LIMIT 1"
    result=cur.execute(query, (tank,polling_address,controller_type, ))
    return result

def update_tank_latest_delivery(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("UPDATE last_entered_delivery SET volume = ? WHERE polling_address = ? AND tank_index = ? AND controller_type = ? ", (data['volume'], data['polling_address'], data['tank_index'],data['controller_type'],))
    if cur.rowcount == 0:
            cur.execute("INSERT INTO last_entered_delivery (read_at, device_address, polling_address, tank_index,controller_type, volume) values (?,?,?,?,?,?)",
            (data['read_at'], data['device_address'], data['polling_address'], data['tank_index'],data['controller_type'], data['volume'],))
    
    conn.commit()
    cur.close()
    conn.close()

def get_probe_deliveries_not_uploaded():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # result = cur.execute("SELECT log, read_at FROM atg_readings where uploaded = ? ", 0)
    result=cur.execute("SELECT id, read_at, device_address, polling_address, tank_index, volume, tc_volume, system_start_time, system_end_time, start_height, end_height, start_volume, end_volume, controller_type  FROM deliveries WHERE uploaded=?", (0,))
    rows = result.fetchall()
    conn.commit()
    conn.close()
    return rows

def update_delivery_logs_not_uploaded(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "UPDATE deliveries SET uploaded = 1 where id = ?"
    result=cur.executemany(query, data)
    conn.commit()
    conn.close()
    return result

def delete_delivery_logs_after_upload(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "DELETE FROM deliveries  WHERE id = ?"
    result=cur.executemany(query, data)
    conn.commit()
    conn.close()
    return result

def tls_probe_log_insert_one(data):

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    done = cur.execute("INSERT INTO atg_primary_log (read_at, device_address, multicont_polling_address, tank_index, pv, pv_flag, sv, uploaded, tc_volume, temperature, water, controller_type) values (?,?,?,?,?,?,?,?,?,?,?,?)",
    (data['read_at'], data['device_address'], data['multicont_polling_address'], data['tank_index'],
    data['pv'],data['pv_flag'], data['sv'], 0, data['tc_volume'], data['temperature'], data['water'], 'TLS'))
    conn.commit()
    conn.close()
    return done

def mtc_probe_log_insert_one(data):

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    done = cur.execute("INSERT INTO atg_primary_log (read_at, device_address, multicont_polling_address, tank_index, pv, pv_flag, sv, uploaded, controller_type) values (?,?,?,?,?,?,?,?,?)",
    (data['read_at'], data['device_address'], data['multicont_polling_address'], data['tank_index'],
    data['pv'],data['pv_flag'], data['sv'], 0, 'MTC'))
    conn.commit()
    conn.close()
    return done
    
def adc_sensor_insert_one(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    done = cur.execute("INSERT INTO sensor_logs(read_at, controller_address, current, tank_index, voltage, uploaded, controller_type, device_address) values (?,?,?,?,?,?,?,?)",
    (data['timestamp'], data['controller_address'], data['current(mA)'], data['tank_index'],
    data['voltage'],0, data['controller_type'], data['device_address']))
    conn.commit()
    conn.close()
    return done
    
def italiana_probe_insert_one(payload):
    #print("got into insert values")
    #print('payload value is: {}'.format(payload))
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = 'INSERT INTO atg_primary_log(device_address,probe_address,sv,water,temperature,status,read_at,controller_type,tank_index,pv_flag,uploaded,multicont_polling_address) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'
    cur.execute(
        sql,
        (payload["mac_address"],
         payload["probe_address"],
         payload["product_float_level"],
         payload["water_float_level"],
         payload["temperature"],
         payload["status"],
         payload["read_at"],
         payload["controller_type"],
         payload['tank_index'],
         payload['pv_flag'],
         0,
         1
         )
    )
    conn.commit()
    cur.close()
    conn.close()
    print("committed")
    
def gamicos_mag_probe_insert_one(payload):
    #print("got into insert values")
    #print('payload value is: {}'.format(payload))
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = 'INSERT INTO atg_primary_log(device_address,probe_address,sv,water,read_at,controller_type,tank_index,pv_flag,uploaded,multicont_polling_address) VALUES(?,?,?,?,?,?,?,?,?,?)'
    cur.execute(
        sql,
        (payload["mac_address"],
         payload["probe_address"],
         payload["product_float_level"],
         payload["water_float_level"],
         payload["read_at"],
         payload["controller_type"],
         payload['tank_index'],
         payload['pv_flag'],
         0,
         1
         )
    )
    conn.commit()
    cur.close()
    conn.close()
    print("committed")
    
def get_sensor_logs_not_uploaded():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # result = cur.execute("SELECT log, read_at FROM atg_readings where uploaded = ? ", 0)
    result=cur.execute("SELECT id, controller_address, tank_index,current, voltage,device_address, controller_type,read_at FROM sensor_logs WHERE uploaded=? ORDER BY read_at DESC LIMIT 50", (0,))
    rows = result.fetchall()
    conn.commit()
    conn.close()
    return rows

def get_italiana_logs_not_uploaded():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = ''' SELECT id,device_address,sv,water,temperature,status,read_at FROM atg_primary_log WHERE uploaded = 0 ORDER BY read_at DESC LIMIT 50'''
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_probe_logs_not_uploaded():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # result = cur.execute("SELECT log, read_at FROM atg_readings where uploaded = ? ", 0)
    result=cur.execute("SELECT id, read_at, pv, pv_flag, sv, device_address, multicont_polling_address, tank_index, tc_volume, water, temperature, controller_type,status,probe_address FROM atg_primary_log WHERE uploaded=? ORDER BY read_at DESC LIMIT 50", (0,))
    rows = result.fetchall()
    #print(rows)
    conn.commit()
    conn.close()
    return rows

def update_probe_logs_not_uploaded(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "UPDATE atg_primary_log SET uploaded = 1 where id = ?"
    result=cur.executemany(query, data)
    conn.commit()
    conn.close()
    return result

def update_sensor_logs_not_uploaded(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "UPDATE sensor_logs SET uploaded = 1 where id = ?"
    result=cur.executemany(query, data)
    conn.commit()
    conn.close()
    return result

def update_italiana_logs_not_uploaded():
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    conn = sqlite3.connect(db_path)
    sql = ''' UPDATE italiana_logs SET uploaded = 1 WHERE id = ?'''
    cur = conn.cursor()
    cur.executemany(sql,indexes)
    conn.commit()
    conn.close()

def hydrostatic_sensor_insert_one(data):
	conn = sqlite3.connect(db_path)
	cur = conn.cursor()
	done = cur.execute("INSERT INTO sensor_logs(read_at, controller_address, current, tank_index, uploaded, controller_type, device_address) values (?,?,?,?,?,?,?)",
	(data['timestamp'], data['controller_address'], data['current(mA)'], data['tank_index'],
	0, data['controller_type'], data['device_address']))
	conn.commit()
	conn.close()
	return done
    
def get_hydrostatic_logs_not_uploaded():
	conn = sqlite3.connect(db_path)
	cur = conn.cursor()
	# result = cur.execute("SELECT log, read_at FROM atg_readings where uploaded = ? ", 0)
	result=cur.execute("SELECT id, controller_address, tank_index,current, voltage,device_address, controller_type,read_at FROM sensor_logs WHERE uploaded=? ORDER BY read_at DESC LIMIT 50", (0,))
	rows = result.fetchall()
	conn.commit()
	conn.close()
	return rows
    
def update_hydrostatic_logs_not_uploaded(data):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        query = "UPDATE sensor_logs SET uploaded = 1 where id = ?"
        result=cur.executemany(query, data)
        conn.commit()
        conn.close()
        return result


def delete_probe_logs_after_upload(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "DELETE FROM atg_primary_log  WHERE id = ?"
    result=cur.executemany(query, data)
    conn.commit()
    conn.close()
    return result



def get_device_config_by_slug(slug):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT value FROM device_config where slug = ?"
    cur.execute(query, (slug,))
    return cur.fetchone()

def get_last_entered_pv_value_italiana(address,controller_type): #NOTE: This function is for all probes
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT sv FROM last_entered_tank_readings where tank_index = ? and controller_type = ? ORDER BY id DESC LIMIT 1"
    result=cur.execute(query, (address,controller_type, ))
    return result.fetchone()

def get_last_entered_pv_value(tank, polling_address, controller_type):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT pv FROM last_entered_tank_readings where tank_index = ? and multicont_polling_address = ? and controller_type = ? ORDER BY id DESC LIMIT 1"
    result=cur.execute(query, (tank,polling_address,controller_type, ))
    #print(result.fetchone())
    return result.fetchone()

def update_tank_latest_reading(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("UPDATE last_entered_tank_readings SET pv = ?, sv = ? WHERE multicont_polling_address = ? AND tank_index = ? AND controller_type = ? ", (data['pv'], data['sv'], data['multicont_polling_address'], data['tank_index'],data['controller_type'],))
    if cur.rowcount == 0:
            cur.execute("INSERT INTO last_entered_tank_readings (read_at, device_address, multicont_polling_address, tank_index,controller_type, pv, sv) values (?,?,?,?,?,?,?)",
            (data['read_at'], data['tank_index'], data['multicont_polling_address'], data['tank_index'],data['controller_type'], data['pv'], data['sv'],))
    
    conn.commit()
    cur.close()
    conn.close()
    
def update_tank_latest_reading_italiana(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    #print('data in update',data)
    cur.execute("UPDATE last_entered_tank_readings SET sv = ? WHERE tank_index = ? AND controller_type = ? ", (data['product_float_level'],data['probe_address'],data['controller_type'],))
    if cur.rowcount == 0:
            print('no data to update')
            cur.execute("INSERT INTO last_entered_tank_readings (read_at, device_address, tank_index,controller_type, sv) values (?,?,?,?,?)",
            (data['read_at'], data['mac_address'], data['probe_address'],data['controller_type'], data['product_float_level'],))
            print('data inserted')
    conn.commit()
    cur.close()
    conn.close()
    
    conn.close()
    
def update_tank_latest_reading_gamicos(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    #print('data in update',data)
    cur.execute("UPDATE last_entered_tank_readings SET sv = ? WHERE tank_index = ? AND controller_type = ? ", (data['product_float_level'],data['probe_address'],data['controller_type'],))
    if cur.rowcount == 0:
            print('no data to update')
            cur.execute("INSERT INTO last_entered_tank_readings (read_at, device_address, tank_index,controller_type, sv) values (?,?,?,?,?)",
            (data['read_at'], data['mac_address'], data['probe_address'],data['controller_type'], data['product_float_level'],))
            print('data inserted')
    conn.commit()
    cur.close()
    conn.close()


def update_device_config(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    print(data)
    device = cur.execute("UPDATE device_config SET value = ? WHERE slug = 'CAN_TRANSMIT'", (data['active'],))
    device = cur.execute("UPDATE device_config SET value = ?  WHERE slug = 'TRANSMIT_INTERVAL'", (data['transmit_interval'], ))
    conn.commit()
    conn.close()
    return device

def new_update_device_config(slug,data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("UPDATE device_config SET value = ? WHERE slug = ?", (data, slug))
    conn.commit()
    conn.close()

def update_device_firmware_version(version_number):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    print(version_number)
    device = cur.execute("UPDATE device_config SET value = ? WHERE slug = 'FIRMWARE_VERSION'", (version_number,))
    conn.commit()
    conn.close()
    return device

def update_at_command_info(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
                                            UPDATE at_command_info SET 
                                            network_provider = ?,
                                            phone_number = ?,
                                            data_balance = ?,
                                            signal_strength = ?,
                                            signal_level = ?,
                                            log_time = ?,
                                            airtime_balance = ?
                                            WHERE device_address = ?
                                            ''', (data["Network_provider"],data["Phone_number"],data["Data_balance"],
                                            data["Signal_details"]["Signal_value(0-30)"],data["Signal_details"]["Signal_condition"],
                                            data["timestamp"],data["Airtime_balance"],data["device_address"],))
    if (cur.rowcount == 0):
            cur.execute("INSERT INTO at_command_info (device_address,network_provider,phone_number,data_balance,signal_strength,signal_level,log_time, airtime_balance) values(?,?,?,?,?,?,?,?)",
            (data["device_address"],data["Network_provider"],data["Phone_number"],data["Data_balance"],data["Signal_details"]["Signal_value(0-30)"],data["Signal_details"]["Signal_condition"],data["timestamp"],data["Airtime_balance"],))
    conn.commit()
    cur.close()
    conn.close()

def get_at_command_info():
    MAC = helper.get_device_mac_address()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # result = cur.execute("SELECT log, read_at FROM atg_readings where uploaded = ? ", 0)
    result=cur.execute("SELECT device_address, network_provider,phone_number,data_balance,signal_strength,signal_level,log_time,airtime_balance FROM at_command_info WHERE device_address = '"+MAC+"'")
    rows = result.fetchall()
    conn.commit()
    conn.close()
    return rows

def get_total_number_of_logs():
    try:
        con,cur=connect_db()
        sql_query="""
                    select  count(id) from atg_primary_log;
        
        """
        cur.execute(sql_query)
        total_number_of_logs=cur.fetchall()[0][0]
        print('all_rows are: {}'.format(total_number_of_logs))
        con.close()
        #my_logger.debug('transaction end details inserted successfully')
        return total_number_of_logs
    except Exception as e:
        print(e)
        my_logger.exception(e)
        return False   

def get_number_of_uploaded_logs():
    try:
        con,cur=connect_db()
        sql_query="""
                    select  count(id) from atg_primary_log where uploaded = 1;
        
        """
        cur.execute(sql_query)
        total_number_of_logs=cur.fetchall()[0][0]
        print('all_rows are: {}'.format(total_number_of_logs))
        con.close()
        #my_logger.debug('transaction end details inserted successfully')
        return total_number_of_logs
    except Exception as e:
        print(e)
        my_logger.exception(e)
        return False   

def get_number_of_unuploaded_logs():
    try:
        con,cur=connect_db()
        sql_query="""
                    select  count(id) from atg_primary_log where uploaded = 0;
        
        """
        cur.execute(sql_query)
        total_number_of_logs=cur.fetchall()[0][0]
        print('all_rows unuploaded are: {}'.format(total_number_of_logs))
        con.close()
        #my_logger.debug('transaction end details inserted successfully')
        return total_number_of_logs
    except Exception as e:
        print(e)
        my_logger.exception(e)
        return False   
def delete_chunk_of_uploaded_logs(number):
    try:
        con,cur=connect_db()
        sql_query="""
                    delete  from atg_primary_log where id in (select id from  atg_primary_log  where uploaded = 1 order by id asc limit ? );
        
        """
        cur.execute(sql_query,number)
        con.commit()
        con.close()
        print('{number} number of logs were deleted')
        #my_logger.debug('transaction end details inserted successfully')
        return True
    except Exception as e:
        print(e)
        my_logger.exception(e)
        return False   

def delete_chunk_of_unuploaded_logs(number):
    try:
        con,cur=connect_db()
        sql_query="""
                    delete  from atg_primary_log where id in (select id from  atg_primary_log  where uploaded = 0 order by id asc limit ? );
        
        """
        cur.execute(sql_query,number)
        con.commit()
        con.close()
        print('{number} number of logs were deleted')
        #my_logger.debug('transaction end details inserted successfully')
        return True
    except Exception as e:
        print(e)
        my_logger.exception(e)
        return False    

if __name__ == '__main__':
    print(get_device_config_by_slug('TANK_DETAILS'))