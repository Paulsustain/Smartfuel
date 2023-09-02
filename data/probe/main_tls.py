import sys
import telnetlib
import time
import json
import datetime
import os
import io
import threading
import sys
sys.path.append('/home/pi/smarteye/helpers')
from atg.tls_data_converter import Inventory
import helper
import sqlite3
sys.path.append('/home/pi/smarteye/services/atg')
import sqlite_service

import main_logger
my_logger=main_logger.get_logger(__name__)

class TelnetThread (threading.Thread):
    
    def __init__(self, name, HOST, PORT, TLS_INDEX):
      threading.Thread.__init__(self)
      self.name = name
      self.HOST = HOST
      self.PORT = PORT
      self.TLS_INDEX = TLS_INDEX

    def run(self):
      print ("Starting " + self.name)
      query_address(self.name, self.HOST, self.PORT, self.TLS_INDEX)
      print("Exiting " + self.name)

def query_address(threadName, HOST, PORT, TLS_INDEX):
    try:
      telnet = telnetlib.Telnet(HOST, PORT)
      inventory = Inventory()
      command_code = inventory.command()
      my_logger.debug('this is the command code: {}'.format(command_code))
      telnet.write(command_code.encode('ascii') + b"\n")
      logs=telnet.read_until(b'')
      response = inventory.response(logs.decode("utf-8"))
      my_logger.debug('this is the response: {}'.format(response))
      for log in response:
        insert_to_db(log, TLS_INDEX)
    except: 
      print("could not reach host")
      
def insert_to_db(data, TLS_INDEX):
  MAC = helper.get_device_mac_address()
	#determine the flag type based on last enterted value
  cursor = sqlite_service.get_last_entered_pv_value(data['Tank index'], TLS_INDEX, 'TLS')
  print(data['Tank index'], TLS_INDEX, 'TLS')
  #print(cursor[0])
  #my_logger.debug('last pv from db for tank: {} is: {}'.format(tank_index,cursor))
  last_pv = 0
  if cursor:
      for (value) in cursor:
        print(value)
        last_pv = float(value)
    #print(last_pv,'************')
  #PV FLAG CODE
  #PV -- 1: the same level i.e new level = old level
  #PV -- 2: Consumption i.e new level < old level
  #PV -- 3: Delivery i.e new level > old_level
  pv_flag = 0
  print(data)
  new_pv = float(data['Volume'])
  new_sv = float(data['Height'])
  temperature = float(data['Temperature'])
  read_at = (data['Read_at'])
  water = float(data['Water'])
  tc_volume = float(data['TC Volume'])
  tank_index = data['Tank index']
  print('last pv {} last_pv new {}'.format(last_pv,new_pv))
    
  if (last_pv-10 <= new_pv <= last_pv+10):
    pv_flag = 1 #same value
  elif(new_pv < last_pv-10):
    pv_flag = 2 #consumption					
  else:
      #(data['PV'][0]['Value'] > last_pv+10):
		  #Tolerance of 10 litres to account for noise
    pv_flag = 3 #delivery
  log = {
            "read_at": read_at,
            "device_address": MAC,
            "multicont_polling_address": TLS_INDEX,
            "tank_index": tank_index,
            "pv": new_pv,
            "pv_flag": pv_flag,
            "sv": new_sv,
            "controller_type" : 'TLS',
            "water": water,
            "tc_volume": tc_volume,
            "temperature": temperature
        }
  my_logger.debug('logs to be inserted in db is: {}'.format(log))
  #print(log)
  if log['pv'] >= 1 or log['sv'] >= 1:
    try:
      sqlite_service.tls_probe_log_insert_one(log)
      sqlite_service.update_tank_latest_reading(log)  
      my_logger.debug('Data inserted successfully')
      print("okay")
    except Exception as e:
      my_logger.exception(e)
 				
print("Exiting Main Thread")

def query_probes():
  # Create new threads
  #os.system("sudo ifconfig eth0 192.168.0.100 netmask 255.255.255.0 ")
  #os.system("sudo ifconfig eth0 up")
  #sleep for 3 seconds to allow change sync, esle wahala
  #time.sleep(3)
  threadLock = threading.Lock()
  threads = []

  thread1 = TelnetThread("TLS-1", "192.168.0.40", 10001, "1")
  thread2 = TelnetThread("TLS-2", "192.168.0.41", 10001, "2")
  thread3 = TelnetThread("TLS-3", "192.168.0.42", 10001, "3")


  # Start new Threads
  thread1.start()
  thread2.start()
  thread3.start()
  # Add threads to thread list
  threads.append(thread1)
  threads.append(thread2)
  threads.append(thread3)

  for t in threads:
    t.join()
  #os.system("sudo ifconfig eth0 down")
  #time.sleep(2)
  print("Exiting Main Thread")
  
if __name__ == "__main__":
    query_probes()
