import enum
# Using enum class create enumerations
class DFM_status(enum.Enum):
   '''This enumerator helps to better name and structure the different status of the DFM'''
   idle = 0
   optimal=1
   overload=2
   cheat=3
   negative=4
   interference=5
   not_supported=12
   no_fuel_rate=13
   error=14
   not_available=15
   reserved_1=6
   reserved_2=7
   reserved_3=8
   reserved_4=9
   reserved_5=10
   reserved_6=11
   
class Upload_type(enum.Enum):
    '''This enumerator here also helps to name the different types of upload operation, which could be for gen-hours or DFM'''
    sources=0
    dfm=1
    pm=2
