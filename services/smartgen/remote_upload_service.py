import sys
sys.path.append('/home/pi/smarteye/services/smartgen')
import sqlite_service
sys.path.append('/home/pi/smarteye/helpers/smartgen')
from uploader import UploaderClass
from DFM_enumerators import Upload_type
sys.path.append('/home/pi/smarteye/helpers')
import helper
import requests


def upload_dfm():
    ''' This function enable us to only logs that have not been uploaded before to the cloud'''   
    #use the enumerator of upload type to specifiy that you are uploading for dfm
    dfmUploader = UploaderClass(Upload_type.dfm)
    #check if there are unuploaded logs, if there are, upload it
    unuploaded_logs = sqlite_service.get_unuploaded_dfm_logs()
    if unuploaded_logs:
        status = dfmUploader.push_log(unuploaded_logs)
        print("there are unuploaded dfm logs")
        if status:
            #change the status of unuploaded logs to uploaded
            sqlite_service.update_unuploaded_dfm_logs(dfmUploader.un_uploaded_indexes)
            print("logs_updated_succesfully")
        
def upload_di_hours():
    ''' This function enable us to only logs that have not been uploaded before to the cloud'''   
    #use the enumerator of upload type to specifiy that you are uploading for dfm
    diUploader = UploaderClass(Upload_type.sources)
    #check if there are unuploaded logs, if there are, upload it
    unuploaded_logs = sqlite_service.get_unuploaded_di_hour_logs()
    if unuploaded_logs:
        status = diUploader.push_log(unuploaded_logs)
        print("there are unuploaded di logs")
        if status:
            #change the status of unuploaded logs to uploaded
            sqlite_service.update_unuploaded_di_hour_logs(diUploader.un_uploaded_indexes)
            print("logs_updated_succesfully")

def get_device_config():
    MAC = helper.get_device_mac_address()
    r = requests.post("https://api.smarteye.com.au/api/v1/devices/remote_config/", data={"mac_address": MAC})
    if(r.status_code == 200):
        return r.json()['data']
    else:
        return {}
    
def main():
    #upload_dfm()
    #upload_di_hours()
    get_device_config()

if __name__ == '__main__':
    main()
