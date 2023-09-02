import sys
import os
import io
import sqlite3
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
conn = sqlite3.connect(dir_path+'/store.db')
c = conn.cursor()
###################################***********************
#MIGRATION 1    
c.execute('''CREATE TABLE IF NOT EXISTS atg_primary_log
             (id integer primary key AUTOINCREMENT, device_address VARCHAR(50) DEFAULT NULL,
             multicont_polling_address INT DEFAULT NULL ,
             tank_index INT DEFAULT NULL ,
    		 sv VARCHAR(50) DEFAULT NULL ,
    		 pv VARCHAR(50) DEFAULT NULL ,
             pv_flag VARCHAR(50) DEFAULT NULL ,
    		 db_fill_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    		 read_at VARCHAR(50) DEFAULT NULL,
             uploaded int)''')

#MIGRATION 2
c.execute('''CREATE TABLE IF NOT EXISTS device_config
             (id integer primary key AUTOINCREMENT, slug text, value VARCHAR(50), updated_at text default NULL)''')

#MIGRATION 3
query = "SELECT value FROM device_config where slug = 'CAN_TRANSMIT'"
result=c.execute(query)

if(len(c.fetchall()) == 0): 
    c.execute("INSERT INTO device_config (slug, value) VALUES('CAN_TRANSMIT', 1)")

#MIGRATION 4
query = "SELECT value FROM device_config where slug = 'TRANSMIT_INTERVAL'"
result=c.execute(query)

if(len(c.fetchall()) == 0): 
    c.execute("INSERT INTO device_config (slug, value) VALUES('TRANSMIT_INTERVAL', 180)")

#MIGRATION 5
query = "SELECT value FROM device_config where slug = 'FIRMWARE_VERSION'"
result=c.execute(query)

if(len(c.fetchall()) == 0):   
    c.execute("INSERT INTO device_config (slug, value) VALUES('FIRMWARE_VERSION', '1.0.0' )")

query = "SELECT value FROM device_config where slug = 'ADC_SENSOR_COUNT'"
result=c.execute(query)

if(len(c.fetchall()) == 0):   
    c.execute("INSERT INTO device_config (slug, value) VALUES('ADC_SENSOR_COUNT', '1' )")

#MIGRATION 6 Table for logging latest Volume of each tank 
c.execute('''CREATE TABLE IF NOT EXISTS last_entered_tank_readings
             (id integer primary key AUTOINCREMENT, device_address VARCHAR(50) DEFAULT NULL,
             multicont_polling_address INT DEFAULT NULL ,
             tank_index INT DEFAULT NULL ,
    		 sv VARCHAR(50) DEFAULT NULL ,
    		 pv VARCHAR(50) DEFAULT NULL ,
    		 db_fill_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    		 read_at VARCHAR(50) DEFAULT NULL)''')

#MIGRATION 7 Deliveries   
c.execute('''CREATE TABLE IF NOT EXISTS deliveries
             (id integer primary key AUTOINCREMENT, 
             device_address VARCHAR(50) DEFAULT NULL,
             polling_address INT DEFAULT NULL ,
             tank_index INT DEFAULT NULL ,
    		 volume VARCHAR(50) DEFAULT NULL ,
    		 tc_volume VARCHAR(50) DEFAULT NULL ,
             system_start_time VARCHAR(50) DEFAULT NULL ,
             system_end_time VARCHAR(50) DEFAULT NULL ,
             start_height VARCHAR(50) DEFAULT NULL ,
             end_height VARCHAR(50) DEFAULT NULL ,
             start_volume VARCHAR(50) DEFAULT NULL ,
             end_volume VARCHAR(50) DEFAULT NULL ,
             controller_type VARCHAR(50) DEFAULT NULL ,
    		 read_at VARCHAR(50) DEFAULT NULL,
             uploaded int)''')

#MIGRATION 8 Table for logging latest DELIVERY Volume of each tank 
c.execute('''CREATE TABLE IF NOT EXISTS last_entered_delivery
             (id integer primary key AUTOINCREMENT, 
             device_address VARCHAR(50) DEFAULT NULL,
             polling_address INT DEFAULT NULL ,
             tank_index INT DEFAULT NULL ,
    		 volume VARCHAR(50) DEFAULT NULL ,
             controller_type VARCHAR(50) DEFAULT NULL ,
    		 db_fill_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    		 read_at VARCHAR(50) DEFAULT NULL)''')

#MIGRATION 9, ADD TLS COLUMNS
try:
    c.execute("ALTER TABLE last_entered_tank_readings ADD controller_type VARCHAR(50) DEFAULT NULL NULL")
    c.execute("ALTER TABLE atg_primary_log ADD water VARCHAR(50) DEFAULT NULL NULL")
    c.execute("ALTER TABLE atg_primary_log ADD temperature VARCHAR(50) DEFAULT NULL NULL")
    c.execute("ALTER TABLE atg_primary_log ADD tc_volume VARCHAR(50) DEFAULT NULL NULL")
    c.execute("ALTER TABLE atg_primary_log ADD controller_type VARCHAR(50) DEFAULT NULL NULL")

except :
    print("likely added already")

#MIGRATION 10, Table for logging AT_Commands
c.execute('''CREATE TABLE IF NOT EXISTS at_command_info
             (id integer primary key AUTOINCREMENT, 
             device_address VARCHAR(50) DEFAULT NULL,
             network_provider VARCHAR(50) DEFAULT NULL,
             phone_number VARCHAR(50) DEFAULT NULL,
             data_balance TEXT DEFAULT NULL,
             signal_strength INT DEFAULT NULL,
    		 signal_level VARCHAR(50) DEFAULT NULL ,
    		 db_fill_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    		 log_time VARCHAR(50) DEFAULT NULL)''')

#MIGRATION 11, ADD COLUMN FOR AIRTIME BALANCE
try:
    c.execute("ALTER TABLE at_command_info ADD airtime_balance TEXT DEFAULT NULL")
except:
    print("airtime_balance likely supported")

#MIGRATION 12, CREATE SENSOR LOGS TABLE
c.execute('''CREATE TABLE IF NOT EXISTS sensor_logs
             (id integer primary key AUTOINCREMENT, 
             controller_address INT DEFAULT NULL ,
             tank_index INT DEFAULT NULL ,
    		 current VARCHAR(50) DEFAULT NULL ,
    		 voltage VARCHAR(50) DEFAULT NULL,
             controller_type VARCHAR(50) DEFAULT NULL ,
    		 db_fill_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    		 read_at VARCHAR(50) DEFAULT NULL,
    		 uploaded int)''')
try:
    c.execute("ALTER TABLE sensor_logs ADD device_address VARCHAR(50) DEFAULT NULL NULL")

except :
    print("device address likely added already to sensor table")


#MIGRATION 13, UPDATE DEVICE CONFIG TABLE
import json

query = "SELECT value FROM device_config where slug = 'TANK_DETAILS'"
result=c.execute(query)
if(len(c.fetchall()) == 0):
    tank_details = [
        {"Name": "Test_MTC", "Control_mode": "C", "Tank_controller": "MTC", "Controller_polling_address": 1, "Tank_index": 1},
        {"Name": "Test_TLS", "Control_mode": "C", "Tank_controller": "TLS", "Controller_polling_address": 1, "Tank_index": 1},
        {"Name": "Test_Analog", "Control_mode": "S", "Tank_controller": "HYD", "Controller_polling_address": 1, "Tank_index": 1}
    ]
    tank_details = json.dumps(tank_details)
    c.execute("INSERT INTO device_config (slug, value) VALUES(?, ?)", ('TANK_DETAILS', tank_details))

query = "SELECT value FROM device_config where slug = 'DEVICE_DETAILS'"
result=c.execute(query)
if(len(c.fetchall())==0):
    device_details = {'transmit_interval': 120, 'active': True}
    device_details = json.dumps(device_details)
    c.execute("INSERT INTO device_config (slug, value) VALUES(?, ?)", ('DEVICE_DETAILS', device_details))

#MIGRATION 14 ADDITION OF ITALIANA PROBE COLUMNS
try:
    c.execute("ALTER TABLE atg_primary_log ADD status VARCHAR(50) DEFAULT NULL NULL")
    c.execute("ALTER TABLE atg_primary_log ADD probe_address VARCHAR(50) DEFAULT NULL NULL")

except :
    print("likely added already")

    
conn.commit()
conn.close()
print('done')
