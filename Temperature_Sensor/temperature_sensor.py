import time
from   smbus import SMBus

class TEMP_SENSOR:
    '''
    TEMP class
    I2C interface class written for MCP9808
    Data Sheet: https://ww1.microchip.com/downloads/en/DeviceDoc/25095A.pdf

    Functionality:
    - Set/Get Critical Temperature
    - Get Temperature
    '''
    i2c_bus = SMBus(1)

    registers = {
        'slave' : 0x18,
        'config' : 0x01,
        't_upper' : 0x02,
        't_lower' : 0x03,
        't_crit' : 0x04,
        't_ambient' : 0x05,
        'manufacture_id' : 0x06,
        'device_id' : 0x07,
        'resolution' : 0x08
    }

    def __init__(self, i2c_status, crit_temperature = None, upper_temperature = None, lower_temperature = None):
        '''
        Initialization of RTC class
        
        Args:
            battery_state: 0 = backup battery off, 1 = backup battery on
            clock_state: 0 = clock off, 1 = clock on
        '''
        if crit_temperature:
            self.set_temperature()

        if upper_temperature:
            self.set_temperature()

        if lower_temperature:
            self.set_temperature()

        self.i2c_status = i2c_status

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
        Decodes register value from Temperature Sensor ambient
        temperature register to a user readable value.  
        
        Returns:
           Decoded ambient temperature value 
        '''
        ones = value % 10
        tens = int(value / 10)
        return (tens<<4 | ones)

    def get_ambient_temp(self):
        '''
        Decodes register value from temperature Sensor ambient
        temperature register to a user readable value.  
        
        Returns:
           Decoded ambient temperature value 
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

    def set_temperature(self, register, value):
        '''
        Return the decoded value of a temperature from a given register
        '''
        if value < 0:


    def get_temperature(self, register):
        '''
        Return the decoded value of a temperature from a given register
        '''
        temp_reg_data = self.i2c_bus.read_i2c_block_data(self.registers['slave'],register, 2)
        upper_byte =  temp_reg_data[0] & 0x1F
        lower_byte = (temp_reg_data[1]) >> 4
        if upper_byte & 0x10:
            upper_byte = (upper_byte & 0x0F) << 4
            return 256 - (upper_byte + lower_byte)
        else: 
            upper_byte = upper_byte << 4
            return upper_byte + lower_byte

    @property
    def ambient(self):
        return self.get_temperature(self.registers['t_ambient'])

    def get_ambient_temp(self):
        '''
        Decodes register value from temperature Sensor ambient
        temperature register to a user readable value.  
        
        Returns:
           Decoded ambient temperature value 
        '''
        temp_reg_data = self.i2c_bus.read_i2c_block_data(self.registers['slave'],self.registers['t_ambient'], 2)
        upper_byte =  temp_reg_data[0] & 0x1F
        lower_byte = temp_reg_data[1]/16
        if upper_byte & 0x10:
            upper_byte = (upper_byte & 0x0F)*16
            return 256 - (upper_byte + lower_byte)
        else: 
            upper_byte = upper_byte *16
            return upper_byte + lower_byte

temp_sensor = TEMP_SENSOR()
while 1:
    time.sleep(1)
    print(f"Current Temperature is :{temp_sensor.ambient}") 