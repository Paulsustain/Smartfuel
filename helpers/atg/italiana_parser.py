def parse(probe_data):
    probe_data=str(probe_data)
    splitted=probe_data.split('=')
    address=splitted[0]
    status=splitted[1]
    temperature=splitted[2]
    product_float_level=splitted[3]
    water_float_level=splitted[4]
    checksum=splitted[5]
    
    data_dict={
                'probe_address':address[2:],
                'status':get_status(status),
                'temperature':get_temperature(temperature),
                'product_float_level':get_product_float_level(product_float_level),
                'water_float_level':water_float_level
               }
    return data_dict
    
def get_status(status):
    if status == '0': return "OK"
    elif status == '1' : return "looking for signal or lack of float"
    elif status == '2': return "error of data linearization"
    elif status == '3' : return "error in parameter"
    else: return "unknown error"
    
def get_temperature(temperature):
    temperature =int(temperature)
    return str(temperature/10) #dividing by 10 since temperature is in 10th of degree.
    
    
def get_product_float_level(product_float_level):
    product_int=int(product_float_level)/10 #dividing by 10 since the product float value is in 10th of mm.
    return str(product_int)
    
