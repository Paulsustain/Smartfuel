import time
import datetime as dt
import sys

sys.path.append('/home/pi/smarteye/services/smartgen')
import sqlite_service
sys.path.append('/home/pi/smarteye/helpers')
from helper import get_device_mac_address as get_mac_address
from smartgen.DFM_enumerators import DFM_status


def get_previous_dfm_log_status(address, serial_number):
    log = sqlite_service.get_previous_dfm_log(address, serial_number)
    if log:
        return log[0]
    else:
        return 0

def get_previous_dfm_log_liters(address, serial_number):
    log = sqlite_service.get_previous_dfm_log(address, serial_number)
    if log:
        return log[1]
    else:
        return 0

def get_previous_dfm_log_hours(address, serial_number):
    log = sqlite_service.get_previous_dfm_log(address, serial_number)
    if log:
        return log[2]
    else:
        return 0

def get_status(mode):
    #check if there is fuel flow in the DFM. All values lesser than interference.value which is 5 means that fuel is flowing through the DFM
    if mode <= DFM_status.interference.value:
        status = True
    else:
        status = False
    return status

def process_dfm_data(flowmeter_data):
    #extract status (mode) register value and check if engine is running
    register=flowmeter_data[0]
    address=flowmeter_data[1]['address']
    serial_number=flowmeter_data[1]['serial_number']
    equipment_id=flowmeter_data[1]['equipment']
    bundled=(register,address,serial_number,equipment_id)
    dfm_mode = register.registers[11]
    #print(dfm_mode)
    status = get_status(dfm_mode)
    print(status)
    previous_log_status = get_previous_dfm_log_status(address, serial_number)
    print('previous log status is: {}'.format(previous_log_status))
    payload=None
    if status or previous_log_status:
        payload = get_dfm_logs_payload(bundled)
    return payload

            
    
def get_dfm_logs_payload(bundled):
    register=bundled[0]
    address=bundled[1]
    serial_number=bundled[2]
    equipment_id=bundled[3]
    ct=dt.datetime.now()
    current_time = ct.strftime('%Y-%m-%d %H:%M:%S')
    
    dfm_mode = register.registers[11]
    status = get_status(dfm_mode)
    mode = DFM_status(dfm_mode).name
    #get all data
    engine_fuel_rate=register.registers[0]
    engine_total_fuel_used_high=register.registers[1]
    engine_total_fuel_used_low=register.registers[2]
    engine_fuel_temperature=register.registers[3]
    high_resolution_total_fuel_used_high=register.registers[4]
    high_resolution_total_fuel_used_low=register.registers[5]
    engine_total_idle_fuel_used_high=register.registers[6]
    engine_total_idle_fuel_used_low=register.registers[7]
    engine_total_idle_hours_high=register.registers[8]
    engine_total_idle_hours_low=register.registers[9]
    engine_total_average_fuel_rate=register.registers[10]
    engine_mode_by_fuel_rate=register.registers[11]
    chamber_fuel_rate_in_supply_chamber=register.registers[12]
    chamber_fuel_rate_in_return_chamber=register.registers[13]
    chamber_working_mode_supply_chamber=register.registers[14]
    chamber_working_mode_return_chamber=register.registers[15]
    high_resolution_engine_total_fuel_used_idle_high=register.registers[16]
    high_resolution_engine_total_fuel_used_idle_low=register.registers[17]
    high_resolution_engine_total_fuel_used_optimal_high=register.registers[18]
    high_resolution_engine_total_fuel_used_optimal_low=register.registers[19]
    high_resolution_engine_total_fuel_used_optimal_high_second=register.registers[20]
    high_resolution_engine_total_fuel_used_overload_low=register.registers[21]
    high_resolution_engine_total_fuel_used_cheating_high=register.registers[22]
    high_resolution_engine_total_fuel_used_cheating_low=register.registers[23]
    high_resolution_engine_total_fuel_used_negative_high=register.registers[24]
    high_resolution_engine_total_fuel_used_negative_low=register.registers[25]
    engine_hours_of_operation_high=register.registers[26]
    engine_hours_of_operation_low=register.registers[27]
    engine_hours_of_operation_idle_high=register.registers[28]
    engine_hours_of_operation_idle_low=register.registers[29]
    engine_hours_of_operation_optimal_high=register.registers[30]
    engine_hours_of_operation_optimal_low=register.registers[31]
    engine_hours_of_operation_overload_high=register.registers[32]
    engine_hours_of_operation_overload_low=register.registers[33]
    engine_hours_of_operation_cheating_high=register.registers[34]
    engine_hours_of_operation_cheating_low=register.registers[35]
    engine_hours_of_operation_negative_high=register.registers[36]
    engine_hours_of_operation_negative_low=register.registers[37]
    engine_hours_of_operation_interferenece_high=register.registers[38]
    engine_hours_of_operation_interference_low=register.registers[39]
    high_resolution_engine_total_fuel_used_forward_high=register.registers[40]
    high_resolution_engine_total_fuel_used_forward_low=register.registers[41]
    high_resolution_engine_total_fuel_used_forward_idle_high=register.registers[42]
    high_resolution_engine_total_fuel_used_forward_idle_low=register.registers[43]
    high_resolution_engine_total_fuel_used_forward_optimal_high=register.registers[44]
    high_resolution_engine_total_fuel_used_forward_optimal_low=register.registers[45]
    high_resolution_engine_total_fuel_used_forward_overload_high=register.registers[46]
    high_resolution_engine_total_fuel_used_forward_overload_low=register.registers[47]
    high_resolution_engine_total_fuel_used_forward_cheating_high=register.registers[48]
    high_resolution_engine_total_fuel_used_forward_cheating_low=register.registers[49]
    flowmeter_chamber_time_counter_forward_low=register.registers[50]
    flowmeter_chamber_time_counter_forward_high=register.registers[51]
    flowmeter_chamber_time_counter_forward_idle_low=register.registers[52]
    flowmeter_chamber_time_counter_forward_idle_high=register.registers[53]
    flowmeter_chamber_time_counter_forward_optimal_low=register.registers[54]
    flowmeter_chamber_time_counter_forward_optimal_high=register.registers[55]
    flowmeter_chamber_time_counter_forward_overload_low=register.registers[56]
    flowmeter_chamber_time_counter_forward_overload_high=register.registers[57]
    flowmeter_chamber_time_counter_forward_cheating_low=register.registers[58]
    flowmeter_chamber_time_counter_forward_cheating_high=register.registers[59]
    high_resolution_engine_total_fuel_used_return_high=register.registers[60]
    high_resolution_engine_total_fuel_used_return_low=register.registers[61]
    high_resolution_engine_total_fuel_used_return_idle_high=register.registers[62]
    high_resolution_engine_total_fuel_used_return_idle_low=register.registers[63]
    high_resolution_engine_total_fuel_used_return_optimal_high=register.registers[64]
    high_resolution_engine_total_fuel_used_return_optimal_low=register.registers[65]
    high_resolution_engine_total_fuel_used_return_overload_high=register.registers[66]
    high_resolution_engine_total_fuel_used_return_overload_low=register.registers[67]
    high_resolution_engine_total_fuel_used_return_cheating_high=register.registers[68]
    high_resolution_engine_total_fuel_used_return_cheating_low=register.registers[69]
    flowmeter_chamber_time_counter_return_low=register.registers[70]
    flowmeter_chamber_time_counter_return_high=register.registers[71]
    flowmeter_chamber_time_counter_return_idle_low=register.registers[72]
    flowmeter_chamber_time_counter_return_idle_high=register.registers[73]
    flowmeter_chamber_time_counter_return_optimal_low=register.registers[74]
    flowmeter_chamber_time_counter_return_optimal_high=register.registers[75]
    flowmeter_chamber_time_counter_return_overload_low=register.registers[76]
    flowmeter_chamber_time_counter_return_overload_high=register.registers[77]
    flowmeter_chamber_time_counter_return_cheating_low=register.registers[78]
    flowmeter_chamber_time_counter_return_cheating_high=register.registers[79]
    engine_total_average_fuel_rate=register.registers[80]
    #engine_total_average_fuel_economy=register.registers[81]
    
    
    
    # get total consumption by adding registers 4 and 5 which correspond to higher and lower word of the values
    reading_sum = (65536 * high_resolution_total_fuel_used_high) + high_resolution_total_fuel_used_low
    liters = reading_sum/1000
    
    # get temperature by subtracting 40 from the read value in register 3
    temperature = engine_fuel_temperature - 40
    
    # get total engine hours by adding registers 26 and 27 which correspond to higher and lower word of the values
    hours = 65536*engine_hours_of_operation_high +  engine_hours_of_operation_low
    forward_liters=(65536*high_resolution_engine_total_fuel_used_forward_high +high_resolution_engine_total_fuel_used_forward_low)/1000
    backward_liters=(65536*high_resolution_engine_total_fuel_used_return_high +high_resolution_engine_total_fuel_used_return_low)/1000
    forward_fuel_rate= chamber_fuel_rate_in_supply_chamber*0.05
    backward_fuel_rate= chamber_fuel_rate_in_return_chamber*0.05
    differential_fuel_rate=engine_fuel_rate*0.05
    
    prev_liters = get_previous_dfm_log_liters(address, serial_number)
    prev_hours = get_previous_dfm_log_hours(address, serial_number)
    
    # if previous liters and the present liters are same, set average to zero
    print("hours of dfm {}, is: {} while previous value is: {}".format(address, hours, prev_hours))
    print("liters of dfm {}, is: {} while previous value is: {}".format(address, liters, prev_liters))
    if prev_hours == 0 and prev_liters == 0:
        average = 0
    else:
        try:
            average = 3600*(liters - prev_liters)/(hours - prev_hours)
        except:
            print("Division Error")
            average=0
        
    
    #put the dfm values in a dict called payload
##    payload = {
##            "mac_address": get_mac_address(),
##            "dfm_address": address,
##            "liters": liters,
##            "hours": hours,
##            "average": average,
##            "temperature": temperature,
##            "engine_running": status,
##            "mode": mode,
##            "timestamp": current_time  
##        }
    payload = {
        "mac_address": get_mac_address(),
        "dfm_address": address,
        "liters": liters,
        "hours": hours,
        "forward_liters":forward_liters,
        "backward_liters":backward_liters,
        "forward_fuel_rate":forward_fuel_rate,
        "backward_fuel_rate":backward_fuel_rate,
        "average": average,
        "differential_fuel_rate": differential_fuel_rate,
        "temperature": temperature,
        "engine_running": status,
        "mode": mode,
        "timestamp": current_time,
        "serial_number": serial_number,
        "equipment": equipment_id
    }
    
    print("this is the payload: ",payload)
    print("payload size is: "+str(sys.getsizeof(payload))+ " bytes")
    return payload
     
    