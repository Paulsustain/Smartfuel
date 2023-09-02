
'''
CD 0 - Read MultiCONT unique ID
CD 12 - Read MultiCONT message
CD 13 - Read MultiCONT TAG, Descriptor and Date
CD 16 - Read Final Assembly Number
CD 241 * CSD 0 - Read Transmitter PV(with time), percent, current
CD 241 * CSD 1 - Read Transmitter PV,SV,TV,QV (All with time)
CD 241 * CSD 2 - Read NIVELCO Transmitter Data
CD 241 * CSD 3 - Read some Transmitter Command 0 data
CD 241 * CSD 4 - Read Transmitter TAG, Descriptor and Date
CD 241 * CSD 5 - Read Transmitter message
CD 241 * CSD 200 - Read MultiCONT registers
CD 241 * CSD 201 - Read Error block
CD 241 * CSD 210 - Read Relay ID, TAG
CD 241 * CSD 211 - Read Relay setup, state
CD 241 * CSD 212 - Read Relay worktime, switching number
CD 241 * CSD 215 - Read current output ID, TAG
CD 241 * CSD 216 - Read current output setup, state 
CD 241 * CSD 220 - Read Interface module ID, TAG
CD 241 * CSD 225 - Read One binding
CD 242 - Remote programming of transmitters (HART over HART)

''' 


#Custom Classes

def clean(data):
	return ["{:02x}".format(ord(chr(c))) for c in data]

def dataFloat(data_bytes):
	bin_list = []
	for c in data_bytes:
	    temp = int(c, 16)
	    bin_list.append(format(temp, '08b'))

	S = int(bin_list[0][0], 2)
	E = bin_list[0][1:]+bin_list[1][0]
	M = bin_list[1][1:]+bin_list[2]+bin_list[3]

	E = int(E, 2)
	M = float(int(M, 2))
	M = M/(2**23)
	frac = 1.0+M
	if S==1:
	    return (-1)*(2**(E-127))*frac
	else:
	    return (1)*(2**(E-127))*frac

def dataDate(data_bytes):
	bin_list = []
	for c in data_bytes:
		temp = int(c, 16)
		bin_list.append(format(temp, '08b'))

	day = int(bin_list[0][3:], 2)
	month = int(bin_list[1][4:], 2)
	year = 1900 + int(bin_list[2],2)

	return '{}-{}-{}'.format(day, month, year)


def dataTime(data_bytes):
	bin_list = []
	for c in data_bytes:
		temp = int(c, 16)
		bin_list.append(format(temp, '08b'))

	hour = int(bin_list[0][3:], 2)
	minute = int(bin_list[1][2:], 2)
	second = int(bin_list[2][2:], 2)

	return '{}:{}:{}'.format(hour, minute, second)






#Read MultiCONT unique ID
class multiCont_ID: #input address in int
	add = 0
	idx = 0
	def command(self, address, index):
		PA = [0xff,0xff,0xff,0xff,0xff,0xff]	#Preamble
		SD = 0x02 							 	#Start Byte
		AD = 0x80 + address 					#Address Byte
		CD = 0x00								#Command Byte
		BC = 0x00								#Number of bytes in Status and
		FCS = SD^AD^CD^BC 						#Frame Check Sequence
		PA.extend([SD,AD,CD,BC,FCS])
		self.add =  address
		self.idx = index
		return PA

	def responseData(self, serialOutput):
		res = clean(serialOutput)
		data_hex = res[12:len(res)-1]

		data_text = {			'CONT address': self.add,
						'Manufacturer_ID': int(data_hex[1], 16),
						'Device_type_ID': int(data_hex[2], 16),
						'Device_ID': int("".join(data_hex[9:]), 16),	
					}
		return data_text


class multiCont_PV:
	address = 0
	index = 0
	def command(self, address, index):
		PA = [0xff,0xff,0xff,0xff,0xff,0xff]	#Preamble 
		SD = 0x02 							 	#Start Byte
		AD = 0x80 + address 					#Address Byte
		CD = 0xf1								#Command Byte
		BC = 0x02								#No of Data bytes
		CSD = 0x01								#Sub command byte
		idx = index							#Transmitter index no
		FCS = SD^AD^CD^BC^CSD^idx 			#Frame Check Sequence
		PA.extend([SD,AD,CD,BC,CSD,idx,FCS])
		self.address = address
		self.index = idx
		return PA

	def responseData(self, serialOutput):
		res = clean(serialOutput)
		data_hex = res[12:len(res)-1]

		data_text = {
						'MultiCONT': self.address,
						'Tank': self.index,
						'PV_Code': int(data_hex[15], 16),
						'Value': dataFloat(data_hex[16:20]),
						'Tank Content(%)': dataFloat(data_hex[26:30]),
						'Output current': dataFloat(data_hex[30:34]),
						'Date': dataDate(data_hex[20:23]),
						'Time': dataTime(data_hex[23:26])
					}

		return data_text



class multiCont_Var:
	address = 0
	index = 0
	def command(self, address, index):
		PA = [0xff,0xff,0xff,0xff,0xff,0xff]	#Preamble 
		SD = 0x02 							 	#Start Byte
		AD = 0x80 + address 					#Address Byte
		CD = 0xf1								#Command Byte
		BC = 0x02								#No of Data bytes
		CSD = 0x01								#Sub command byte
		idx = index							#Transmitter index no
		FCS = SD^AD^CD^BC^CSD^idx 			#Frame Check Sequence
		PA.extend([SD,AD,CD,BC,CSD,idx,FCS])
		self.address = address
		self.index = idx
		return PA

	def responseData(self, serialOutput):
		res = clean(serialOutput)
		data_hex = res[12:len(res)-1]

		data_text = {
						"PV": [
								{
								'MultiCONT': self.address,
								'Tank': self.index+1,
								'Code': int(data_hex[15], 16),
								'Value': dataFloat(data_hex[16:20]),
								'Date': dataDate(data_hex[20:23]),
								'Time': dataTime(data_hex[23:26])
								}
							],
						"SV": [
								{
								'MultiCONT': self.address,
								'Tank': self.index+1,
								'Code': int(data_hex[26], 16),
								'Value': dataFloat(data_hex[27:31]),
								'Date': dataDate(data_hex[31:34]),
								'Time': dataTime(data_hex[34:37])
								}
							],
						"TV": [
								{'Code': int(data_hex[37], 16)},
								{'Value': dataFloat(data_hex[38:42])},
								{'Date': dataDate(data_hex[42:45])},
								{'Time': dataTime(data_hex[45:48])}
								],
						"QV": [
								{'Code': int(data_hex[48], 16)},
								{'Value': dataFloat(data_hex[49:53])},
								{'Date': dataDate(data_hex[53:56])},
								{'Time': dataTime(data_hex[56:59])}
								]
					}
		return data_text

class multiCont_TAG:

	pass

	def command(self, address):
		PA = [0xff,0xff,0xff,0xff,0xff,0xff]	#Preamble 
		SD = 0x02 							 	#Start Byte
		AD = 0x80 + address 					#Address Byte
		CD = 0x0d								#Command Byte
		BC = 0x00								#Number of bytes in Status and 
		FCS = SD^AD^CD^BC 						#Frame Check Sequence
		PA.extend([SD,AD,CD,BC,FSC])
		return PA

	def responseData(self, serialOutput):
		pass




