import sys
sys.path.append('/home/pi/smarteye/services/atg')
import remote_api_service

def sensor_remote_logger():
    try:
        remote_api_service.upload_sensor_log()
    except:
        print('Unable to upload sensor data to remote db')
		
def main():
    sensor_remote_logger()

if __name__ == '__main__':
    main()
