import sys
import telnetlib
import time
import json
import datetime
import os
# Make it work for Python 2+3 and with Unicode
import io
import threading
import sys
sys.path.append('/home/pi/smarteye/helpers')
from atg.tls_data_converter import Delivery
import helper
import sqlite3
sys.path.append('/home/pi/smarteye/services/atg')
import remote_api_service
import sqlite_service

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
        delivery = Delivery()
        command_code = delivery.command()
        telnet.write(command_code.encode('ascii') + b"\n")
        logs=telnet.read_until(b'')
        print("the logs are: {}".format(logs))
        response = delivery.response(logs.decode("utf-8"))
        print("the responses are: {}".format(response))
        for log in response:
            insert_to_db(log, TLS_INDEX)
    except: 
        print("could not reach host")


def insert_to_db(data, TLS_INDEX):
  MAC = helper.get_device_mac_address()
	#determine the flag type based on last enterted value
  cursor = sqlite_service.get_last_entered_delivery_volume_value(data['Tank index'], TLS_INDEX, 'TLS')
  print("the cursor is: {}".format(cursor))
  last_volume = 0

  for (value) in cursor:
    last_volume = float(value[0])
##    
##  system_start_time = (data['Starting Time'])
##  system_end_time = (data['Ending Time'])
  print("about to reformat time")
  try:
      system_start_time = datetime.datetime.strptime(data['Starting Time'], "%y-%m-%d %H:%M")
      system_start_time = datetime.datetime.strftime(system_start_time, "%Y-%m-%d %H:%M")
      
      system_end_time = datetime.datetime.strptime(data['Ending Time'], "%y-%m-%d %H:%M")
      system_end_time = datetime.datetime.strftime(system_end_time, "%Y-%m-%d %H:%M")
  except Exception as e:
      print(e)
  #print("start time is: {} and end time is: {}".format(system_start_time,system_end_time))
  start_height = float(data['Starting Height'])
  end_height = float(data['Ending Height'])
  start_volume = float(data['Starting Volume'])
  end_volume = float(data['Ending Volume'])
  volume = float(data['Ending Volume']) - float(data['Starting Volume'])
  tc_volume = float(data['Ending TC Volume']) - float(data['Starting TC Volume'])
  read_at = (data['Read_at'])
  tank_index = data['Tank index']
   
  if (last_volume-1 <= volume <= last_volume+1):
    print("same volume",system_start_time,system_end_time)					
  else:
    #new delivery
    log = {
            "read_at": read_at,
            "device_address": MAC,
            "polling_address": TLS_INDEX,
            "tank_index": tank_index,
            "volume": volume,
            "tc_volume": tc_volume,
            "controller_type" : 'TLS',
            "system_end_time": system_end_time,
            "system_start_time": system_start_time,
            "start_height": start_height,
            "end_height": end_height,
            "start_volume": start_volume,
            "end_volume": end_volume
        }
    print("new logs are: {}".format(log))
    sqlite_service.tls_probe_delivery_insert_one(log)
    sqlite_service.update_tank_latest_delivery(log)  
    print("okay")
 			
def query_probes():
  # Create new threads
  #os.system("sh ethernet_config_up.sh")
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
 # time.sleep(2)

  print("Exiting Main Thread")

  

if __name__ == "__main__":
    query_probes()
