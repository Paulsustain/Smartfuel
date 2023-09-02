import sys
sys.path.append('/home/pi/smarteye/data/probe')
import main_delivery_tls

def log_tls_delivery_data():
    try:
        main_delivery_tls.query_probes()
    except:
        print("could not log data to remote db")

def main():
    log_tls_delivery_data()

if __name__ == '__main__':
    main()
