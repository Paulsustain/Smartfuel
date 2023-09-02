import sys
sys.path.append('/home/pi/smarteye/helpers')
import smartgen.flowmeter_data_converter as flowmeter_data_converter
import smartgen.power_meter_data_converter as power_meter_data_converter
sys.path.append('/home/pi/smarteye/services/smartgen')
import sqlite_service
import uuid
from datetime import datetime as dt

def process_registers(flowmeter_data,power_meter_data):
    flowmeter_payload=power_meter_payload=None
    if flowmeter_data[0]:
        flowmeter_payload=flowmeter_data_converter.process_dfm_data(flowmeter_data)
    if power_meter_data[0]:
        power_meter_payload=power_meter_data_converter.process_power_data(power_meter_data)
    ct=dt.now()
    time_now = ct.strftime('%Y-%m-%d %H:%M:%S')
    main_uuid=str(uuid.uuid4())
    if flowmeter_payload:
##        average_time=(dt.strptime(flowmeter_payload["timestamp"],'%yyyy-%mm-%dd %HH:%MM:%SS')+dt.strptime(power_meter_payload["timestamp"],'%yyyy-%mm-%dd %HH:%MM:%SS'))/2
##        flowmeter_payload['timestamp']=average_time
##        power_meter_payload['timestamp']=average_time
        flowmeter_payload['UUID']=main_uuid
        sqlite_service.dfm_logs_insert(flowmeter_payload)
        #save the current values as the previous values
        sqlite_service.update_dfm_logs_current_value(flowmeter_payload)
    if power_meter_payload:
        flowmeter_payload['UUID']=main_uuid
        #merged_payload=merge_dict(flowmeter_payload,power_meter_payload)
        #print('This is the merged payload: {}'.format(merged_payload))
        #insert value in the dfm database
        sqlite_service.pm_logs_insert(power_meter_payload)
    
    
def merge_dict(dict_a,dict_b):
    merged=dict_a.copy()
    merged.update(dict_b)
    return merged