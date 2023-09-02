import sys
sys.path.append('/home/pi/smarteye/data/probe')
import main_tls

def log_tls_data():
    try:
        main_tls.query_probes()
    except:
        print("could not log data to remote db")

def main():
    log_tls_data()

if __name__ == '__main__':
    main()
