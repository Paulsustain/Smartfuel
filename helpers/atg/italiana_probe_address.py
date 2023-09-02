import json
import sys
sys.path.append('/home/pi/smarteye/services/atg')
import sqlite_service

def get_addresses():
    tanks = json.loads(sqlite_service.get_device_config_by_slug('TANK_DETAILS')[0])
    print(tanks)
    addresses=[]
    for tank in tanks:
        if tank['Tank_controller']=='STL':
            addresses.append(tank['Tank_index'])
    print(addresses)
    return addresses

if __name__=="__main__":
    get_addresses()