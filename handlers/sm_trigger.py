# Smartpump Sim Module Auto Restart Script
# Feature: This script performs hardware rebbot for the Sim Module whenever unuploaded data is greater or equal to 20 samples.
import sys
sys.path.append('/home/pi/smarteye/services/atg')
sys.path.append('/home/pi/smarteye/helpers')
import RPi.GPIO as GPIO
import time
#import sqlite_service
import json
import datetime
import requests
import main_logger
import sqlite_service
#from mysql.connector import MySQLConnection, Error
my_logger=main_logger.get_logger(__name__)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
 
GPIO.setup(37,GPIO.OUT)    # Gpio Pin 37 as digital output on the pi

def toggle_pin():          # Function to change the pin transition of the gpio from high to low
    try:
        print("Pin High")
        GPIO.output(37,GPIO.HIGH)   
        time.sleep(10)
        #print("Pin LOW")
        GPIO.output(37,GPIO.LOW)
       
    
    except Exception as e:
        print(e)
        

def run_sm():
    transmit= json.loads(sqlite_service.get_device_config_by_slug('DEVICE_DETAILS')[0])['active']     # Capture transmit interval
    if transmit:                                                                               # if trasmit interval is captured
        try:
            data = sqlite_service.get_number_of_unuploaded_logs()    # assign the unuploaded transaction to variable "data"
            #print(len(data))
            
            if data>=20:                                  # execute toggle_pin function if unuploaded data is greater than or eual to 20 samples
                
                my_logger.debug('sim module power cycle run successfully')
                print('sim moudle rebooted')
                return toggle_pin()
            else :
                print('No unuploaded data')
                return None
        except Exception as e:
            print('error')
            
       
    
#if __name__ =='__main__':
#sm_high()
run_sm()             # run this function
#toggle_pin()
    

