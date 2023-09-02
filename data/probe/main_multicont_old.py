import serial.tools.list_ports
import time
import datetime
import info_multicont
from helpers import helper
import sqlite3
from services import sqlite_service

def query_probes():
	#store all connected ports in a list
	portsInfo = serial.tools.list_ports.comports()
        
	ComPorts = []
	for i in range(len(portsInfo)):
		ComPorts.append(portsInfo[i].device)

	#USB PORTS
	usbPorts = [port for port in ComPorts if 'USB' in port]
	print(usbPorts)
	ser = []  #List of objects of Serial instances
	for port in range(len(usbPorts)):
		conn = serial.Serial(
		port=usbPorts[port],
		baudrate=9600,
		parity=serial.PARITY_ODD,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		)
		ser.append(conn)

	MAC = helper.get_device_mac_address()
	print(MAC)
	for conn in ser:
		if conn.port == '/dev/ttyUSB0':
			address = [1,2,3]
			for add in address: 
				try:
					Var = info_multicont.multiCont_Var()
					index = list(range(0,8))
					time.sleep(1)
					for i in index:
						try:	
							command = Var.command(add, i)
							conn.write(bytearray(command))
							time.sleep(0.8)
							res = conn.read(size=conn.in_waiting)
							data = Var.responseData(res)
							#determine the flag type based on last enterted value
							cursor = sqlite_service.get_last_entered_pv_value(data['PV'][0]['Tank'], data['PV'][0]['MultiCONT'],'MTC' )
							last_pv = 0

							for (value) in cursor: 
								last_pv = float(value[0])

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

							if  float(log['pv']) >= 1 or float(log['sv']) >= 1:
								sqlite_service.mtc_probe_log_insert_one(log)
								sqlite_service.update_tank_latest_reading(log)
						except IndexError:
                                                        log = {}
							#print('Tank {} not available.'.format(i))
				except IndexError:
					print('Cont address {} not available'.format(add))

def main():
	query_probes()

 
if __name__ == '__main__':
    main()














