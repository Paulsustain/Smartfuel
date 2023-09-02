import datetime
import os
# Make it work for Python 2+3 and with Unicode
import io
import sqlite3
from sqlite3 import Error

db_path = '/home/pi/smarteye/db/smartgen/sqlite.db'

def get_dfm_config_by_slug(slug):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = 'SELECT value FROM dfm_config WHERE slug = ?'
    cur.execute(query, (slug,))
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result

def update_dfm_config(slug,data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("UPDATE dfm_config SET value = ? WHERE slug = ?", (data, slug))
    conn.commit()
    conn.close()
    print("DFM_CONFIG updated")
    
def get_previous_dfm_log(address, serial_number):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = 'SELECT EngineRunning, Liters, Hours FROM last_inserted_dfm_reading WHERE DFM_Address = ? AND serial_number = ?'
    cur.execute(query, (address,serial_number))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return result
    else:
        return None

##def get_previous_dfm_log(address):
##    conn = sqlite3.connect(db_path)
##    cur = conn.cursor()
##    query = 'SELECT EngineRunning, Liters, Hours FROM last_inserted_dfm_reading WHERE DFM_Address = ?'
##    cur.execute(query, (address,))
##    result = cur.fetchone()
##    cur.close()
##    conn.close()
##    if result:
##        return result
##    else:
##        return None
    
##def update_dfm_logs_current_value(payload):
##    conn = sqlite3.connect(db_path)
##    cur = conn.cursor()
##    cur.execute("UPDATE last_inserted_dfm_reading SET EngineRunning = ?, Liters = ?, Hours = ?, Average=?, Temperature=?, Mode=?, Timestamp=? WHERE DFM_Address = ?",
##                (payload["engine_running"],
##                 payload["liters"],
##                 payload["hours"],
##                 payload["average"],
##                 payload["temperature"],
##                 payload["mode"],
##                 payload["timestamp"],
##                 payload["dfm_address"]
##                 ))
##    if cur.rowcount == 0:
##        sql = 'INSERT INTO last_inserted_dfm_reading (MacAddress,DFM_Address,Liters,Hours,Average,Temperature,EngineRunning,Mode,TimeStamp) VALUES(?,?,?,?,?,?,?,?,?)'
##        cur.execute(
##            sql,
##            (payload["mac_address"],
##             payload["dfm_address"],
##             payload["liters"],
##             payload["hours"],
##             payload["average"],
##             payload["temperature"],
##             payload["engine_running"],
##             payload["mode"],
##             payload["timestamp"])
##        )
##    conn.commit()
##    cur.close()
##    conn.close()
    
def update_dfm_logs_current_value(payload):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("UPDATE last_inserted_dfm_reading SET EngineRunning = ?, Liters = ?, Hours = ?, ForwardLiters=?,BackwardLiters=?,ForwardFuelRate=?,BackwardFuelRate=?,Average=?, DifferentialFuelRate=?, Temperature=?, Mode=?, Timestamp=? WHERE DFM_Address = ? AND serial_number = ?",
                (payload["engine_running"],
                 payload["liters"],
                 payload["hours"],
                 payload["forward_liters"],
                 payload["backward_liters"],
                 payload["forward_fuel_rate"],
                 payload["backward_fuel_rate"],
                 payload["average"],
                 payload["differential_fuel_rate"],
                 payload["temperature"],
                 payload["mode"],
                 payload["timestamp"],
                 payload["dfm_address"],
                 payload["serial_number"]
                 ))
    if cur.rowcount == 0:
        sql = 'INSERT INTO last_inserted_dfm_reading (MacAddress,DFM_Address,Liters,Hours,ForwardLiters,BackwardLiters,ForwardFuelRate,BackwardFuelRate,Average,DifferentialFuelRate,Temperature,EngineRunning,Mode,TimeStamp, serial_number) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cur.execute(
            sql,
            (payload["mac_address"],
             payload["dfm_address"],
             payload["liters"],
             payload["hours"],
             payload["forward_liters"],
             payload["backward_liters"],
             payload["forward_fuel_rate"],
             payload["backward_fuel_rate"],
             payload["average"],
             payload["differential_fuel_rate"],
             payload["temperature"],
             payload["engine_running"],
             payload["mode"],
             payload["timestamp"],
             payload["serial_number"])
        )
    conn.commit()
    cur.close()
    conn.close()


def dfm_logs_insert(payload):
    print("got into insert values")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = 'INSERT INTO dfm_logs(MacAddress,DFM_Address,Liters,Hours,ForwardLiters,BackwardLiters,ForwardFuelRate,BackwardFuelRate,Average,DifferentialFuelRate,Temperature,EngineRunning,Mode,TimeStamp, serial_number,equipmentID,UUID) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    cur.execute(
        sql,
        (payload["mac_address"],
         payload["dfm_address"],
         payload["liters"],
         payload["hours"],
         payload["forward_liters"],
         payload["backward_liters"],
         payload["forward_fuel_rate"],
         payload["backward_fuel_rate"],
         payload["average"],
         payload["differential_fuel_rate"],
         payload["temperature"],
         payload["engine_running"],
         payload["mode"],
         payload["timestamp"],
         payload['serial_number'],
         payload["equipment"],
         payload["UUID"]
         )
    )
    conn.commit()
    cur.close()
    conn.close()
    print("committed")
    
##def dfm_logs_insert(payload):
##    print("got into insert values")
##    conn = sqlite3.connect(db_path)
##    cur = conn.cursor()
##    sql = 'INSERT INTO dfm_logs(MacAddress,DFM_Address,Liters,Hours,Average,Temperature,EngineRunning,Mode,TimeStamp) VALUES(?,?,?,?,?,?,?,?,?)'
##    cur.execute(
##        sql,
##        (payload["mac_address"],
##         payload["dfm_address"],
##         payload["liters"],
##         payload["hours"],
##         payload["average"],
##         payload["temperature"],
##         payload["engine_running"],
##         payload["mode"],
##         payload["timestamp"])
##    )
##    conn.commit()
##    cur.close()
##    conn.close()
def energy_logs_insert(payload):
    print("got into power meter insert values")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = 'INSERT INTO pm_logs(MacAddress,pmAddress,equipmentID,Timestamp,UUID,voltage_a,voltage_b,voltage_c,current_a,current_b,current_c,power_a,power_b,power_c,power_total,frequency,power_factor,active_energy,meter_type,EngineRunning) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    cur.execute(
        sql,
        (payload["mac_address"],
         payload["address"],
         payload["equipment"],
         payload["timestamp"],
         payload["UUID"],
         payload["voltage_a"],
         payload["voltage_b"],
         payload["voltage_c"],
         payload["current_a"],
         payload["current_b"],
         payload["current_c"],
         payload["power_a"],
         payload["power_b"],
         payload["power_c"],
         payload["power_total"],
         payload["frequency"],
         payload["power_factor"],
         payload["active_energy_delivered"],
         'DPM',
         payload["engine_running"]
         )
    )
    conn.commit()
    cur.close()
    conn.close()
    print("committed")
    
def pm_logs_insert(payload):
    print("got into power meter insert values")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = 'INSERT INTO pm_logs(MacAddress,pmAddress,current,voltage,power,equipmentID,Timestamp,UUID,meter_type) VALUES(?,?,?,?,?,?,?,?,?)'
    cur.execute(
        sql,
        (payload["mac_address"],
         payload["address"],
         payload["current"],
         payload["voltage"],
         payload["power"],
         payload["equipment"],
         payload["timestamp"],
         payload["UUID"],
         'DPP'
         )
    )
    conn.commit()
    cur.close()
    conn.close()
    print("committed")
    
def di_hours_logs_insert(payload):
    print("got into insert values")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = "INSERT INTO di_hours(MacAddress,lineID,Status,TimeStamp) VALUES(?,?,?,?)"
    print(payload)
    cur.execute(sql, payload)
    conn.commit()
    cur.close()
    conn.close()
    print('di inserted')
    
def get_unuploaded_dfm_logs():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = ''' SELECT * FROM dfm_logs WHERE uploaded = 0 '''
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_unuploaded_di_hour_logs():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = ''' SELECT * FROM di_hours WHERE uploaded = 0 '''
    cur.execute(sql)
    rows = cur.fetchall()  
    cur.close()
    conn.close()
    return rows

def get_unuploaded_pm_logs():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = ''' SELECT * FROM pm_logs WHERE uploaded = 0 '''
    cur.execute(sql)
    rows = cur.fetchall()  
    cur.close()
    conn.close()
    #print(rows)
    return rows


def update_unuploaded_dfm_logs(indexes):
    conn = sqlite3.connect(db_path)
    sql = ''' UPDATE dfm_logs SET uploaded = 1 WHERE id = ?'''
    cur = conn.cursor()
    cur.executemany(sql,indexes)
    conn.commit()
    conn.close()
    
def update_unuploaded_pm_logs(indexes):
    conn = sqlite3.connect(db_path)
    sql = ''' UPDATE pm_logs SET uploaded = 1 WHERE id = ?'''
    cur = conn.cursor()
    cur.executemany(sql,indexes)
    conn.commit()
    conn.close()

def update_unuploaded_di_hour_logs(indexes):
    conn = sqlite3.connect(db_path)
    sql = ''' UPDATE di_hours SET uploaded = 1 WHERE id = ?'''
    cur = conn.cursor()
    cur.executemany(sql,indexes)
    conn.commit()
    conn.close()

def view_all():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = ''' SELECT * FROM dfm_logs'''
    #print("This is the cur",cur)
    cur.execute(sql)
    rows=cur.fetchall()
    for row in rows:
        print(row)
    conn.close()
    
def get_dfm_last_log_by_equipment_address(equipment_address):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = ''' SELECT * FROM dfm_logs where equipmentID = ? order by id desc limit 1'''
    #print("This is the cur",cur)
    cur.execute(sql,(equipment_address,))
    rows=cur.fetchone()
    print(rows)
    conn.close()
    #print('got here')
    return rows

def get_pm_last_log_by_equipment_address(equipment_address):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = ''' SELECT * FROM pm_logs where equipmentID = ? order by id desc limit 1'''
    #print("This is the cur",cur)
    cur.execute(sql,(equipment_address,))
    rows=cur.fetchone()
    print(rows)
    conn.close()
    #print('got here')
    return rows
    
if __name__ == '__main__':
    #print(get_previous_dfm_log(111))
    #print(get_pm_last_log_by_equipment_address(1))
    get_unuploaded_pm_logs()

        

