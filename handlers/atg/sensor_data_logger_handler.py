import sys
sys.path.append('/home/pi/smarteye/data/probe')
import main_sensor

def log_sensor_data_to_db():
    try:
        main_sensor.get_converter_readings()
    except:
        print('could not log sensor data to local db')

def main():
    log_sensor_data_to_db()


if __name__ == '__main__':
    main()
