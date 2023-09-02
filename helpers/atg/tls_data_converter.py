from __future__ import division
from datetime import datetime

# from .main_tls import 
def tank_split(Mylist, size):
	for i in range(0, len(Mylist), size):
		yield Mylist[i: i+size]

def dataFloat(values):
    #values = "".join(values_list)
    try:
        values = int(values, 16)
        if values == 0:
            return 0
        bin_list = format(values, '08b')
        if len(bin_list)==31:
            bin_list = '0'+bin_list
        S = int(bin_list[0], 2)
        E = bin_list[1:9]
        M = bin_list[9:]

        E = int(E, 2)
        E = 2**(E-127)

        M = int(M, 2)
        M = M/(8388608)
        
        frac = 1.0+M
        
        if S==1:
            return (-1)*E*frac
        else:
            return (1)*E*frac
    except Execption as e:
        print(e)
        return 0

def dataDate(value):
    date = value[:6]
    time = value[6:]
    new_date = date[:2]+'-'+date[2:4]+'-'+date[4:]
    new_time = time[:2]+':'+time[2:]

    return new_date+' '+new_time

class Inventory:
    def __init__(self):
        self.function_code = "i20100"
        self.no_of_data_fields = 7
        self.no_of_data_chars = 65

    def command(self):
        code = "\x01"+self.function_code
        return code
    
    def response(self, serialOutput):
        #remove function code from serial output
        data = serialOutput.replace(self.function_code, '')
        #Extract date
        date = data[:11]
        data = data[11:]
        #Extract data before '&&'
        data = data[0:data.find('&&')]
        tank_data = tuple(tank_split(data, self.no_of_data_chars))
        data_list = []
        for tank in range(len(tank_data)):
            data_dict = {
                "Tank index": tank_data[tank][:2],
                "Read_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),              
                "Volume":dataFloat(tank_data[tank][9:17]),
                "TC Volume":dataFloat(tank_data[tank][17:25]),
                "Height":dataFloat(tank_data[tank][33:41]),
                "Water":dataFloat(tank_data[tank][41:49]),
                "Temperature":dataFloat(tank_data[tank][49:57]),
                "Water_Volume":dataFloat(tank_data[tank][57:65])
            }
            data_list.append(data_dict)
        
        return data_list


class Delivery:
    def __init__(self):
        self.function_code = "i20C00"
        self.no_of_data_fields = 10
        self.no_of_data_chars = 155

    def command(self):
        code = "\x01"+self.function_code
        return code
    
    def response(self, serialOutput):
        #remove function code from serial output
        data = serialOutput.replace(self.function_code, '')
        #Extract date
        date = data[:11]
        data = data[11:]
        #Extract data before '&&'
        data = data[0:data.find('&&')]
        tank_data = tuple(tank_split(data, self.no_of_data_chars))
        data_list = []
        for tank in range(len(tank_data)):
            data_dict = {
                "Tank index": tank_data[tank][:2],
                "Starting Time": dataDate(tank_data[tank][5:15]),
                "Ending Time": dataDate(tank_data[tank][15:25]),
                "Read_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),              
                "Starting Volume":dataFloat(tank_data[tank][27:35]),
                "Starting TC Volume":dataFloat(tank_data[tank][35:43]),
                "Starting Water":dataFloat(tank_data[tank][43:51]),
                "Starting Temp":dataFloat(tank_data[tank][51:59]),
                "Ending Volume":dataFloat(tank_data[tank][59:67]),
                "Ending TC Volume":dataFloat(tank_data[tank][67:75]),
                "Ending Water":dataFloat(tank_data[tank][75:83]),
                "Ending Temp":dataFloat(tank_data[tank][83:91]),
                "Starting Height":dataFloat(tank_data[tank][91:99]),
                "Ending Height":dataFloat(tank_data[tank][99:107])
            }
            data_list.append(data_dict)
        # return data
        return data_list
