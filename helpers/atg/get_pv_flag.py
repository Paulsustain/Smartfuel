import sys
sys.path.append('/home/pi/smarteye/services/atg')
import sqlite_service

def pv_flag(combined_data):
    last_row =sqlite_service.get_last_entered_pv_value_italiana(combined_data['probe_address'],combined_data['controller_type']) #NOTE: The function "get_last_entered_pv_value_italiana", is for all probes
    #last_row=last_row.fetchall()
    if not last_row:
        return 1
    old_sv=last_row[0]
    print('this is the last row: ',old_sv)
    pv_flag=get_flag(combined_data['product_float_level'],old_sv)
    print( 'pv_flag is: ',pv_flag)
    print('*' *50)
    return pv_flag

def get_flag(new_sv,old_sv):
    new_sv=float(new_sv)
    old_sv=float(old_sv)
    if (old_sv-5 <= new_sv <= old_sv+10):
        pv_flag = 1 #same value

    elif(new_sv < old_sv-5):
        pv_flag = 2 #consumption

    else:#(new_sv > old_sv+10):
        #Tolerance of 10 litres to account for noise
        pv_flag = 3 #delivery
    return pv_flag
