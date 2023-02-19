import time
from   smbus import SMBus

class TEMP_SENSOR:
    '''
    TEMP class
    I2C interface class written for MCP9808
    Data Sheet: https://ww1.microchip.com/downloads/en/DeviceDoc/25095A.pdf

    Functionality:
    - Set/Get Crtical Tempreature
    - Get Tempreature
    '''
    i2c_bus = SMBus(1)

    registers = {
        'slave' : 0x18,
        'config' : 0x01,
        't_upper' : 0x02,
        't_lower' : 0x03,
        't_crit' : 0x04,
        't_ambient' : 0x05,
        'manufactuer_id' : 0x06,
        'device_id' : 0x07,
        'resolution' : 0x08
    }

    def __init__(self, battery_state, clock_state):
        '''
        Initiazation of RTC class
        
        Args:
            battery_state: 0 = backup battery off, 1 = backup battery on
            clock_state: 0 = clock off, 1 = clock on
        '''
        self.battery = battery_state 
        self.clock = clock_state 

    def reset(self):
        '''
        Reset the clock's time to zero, and battery to zero 

        Returns:
            -1: The RTC was unable to be reset
            0: The RTC was able to be reset
        '''
        for self.rtc_register in self.registers:
            try:
                self.current_time = 0
                self.battery = 0
            except:
               print("Unable to reset RTC") 
               return -1
        return 0   
    
    def __decode_ambient(self,value):
        '''
        Decodes register value from Tempreature Sensor ambient
        tempreature regiester to a user readable value.  
        
        Returns:
           Decoded ambient tempreature value 
        '''
        ones = value % 10
        tens = int(value / 10)
        return (tens<<4 | ones)

    def get_ambient_temp(self):
        '''
        Decodes register value from tempreature Sensor ambient
        temperature register to a user readable value.  
        
        Returns:
           Decoded ambient tempreature value 
        '''
        temp_reg_data = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['t_ambient'])
        sign_bit =   temp_reg_data &  (0b1 << 12)
        temp_reg_data =   temp_reg_data &  0b1111,1111,1111
        power = -4
        converted_temp = 0
        while(temp_reg_data != 0):
            converted_temp =+ 2 ** power
            power =+ 1
            temp_reg_data = temp_reg_data>>1 
        if sign_bit > 0:
            return converted_temp*-1
        else:
            return converted_temp

temp_sensor = TEMP_SENSOR()
while 1:
    time.sleep(1)
    print(f"Current Tempreature is :{temp_sensor.get_ambient_temp()}") 