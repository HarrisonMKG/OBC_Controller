from   smbus import SMBus

class Temperature_Sensor:
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
        Initialization of Temperature_Sensor class
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
            -1: The Tempreature Sensor was unable to be reset
            0: The Tempreature Sensor was able to be reset
        '''
        return 0   

    @staticmethod
    def bit_inverse(bit,binary):
        tmp = binary >> bit
        replacement = 1 << bit 

        if tmp & 0x1: #bit to replace is a 1
            replacement = ~replacement
            binary &= replacement
                
        else: #bit to replace is a 0
            binary |= replacement

        return binary 

    def set_temperature(self, register, value):
        '''
        Return the decoded value of a temperature from a given register
        '''
        upper_byte = int(value/ 16) >> 8 #isolate Upper bits
        lower_byte = (value * 16)

        if value < 0:
            for i in range(4):
                upper_byte = self.bit_inverse(i,upper_byte)
            for i in range(8):
                lower_byte = self.bit_inverse(i,lower_byte)
            upper_byte |= 0x10 # add sign bit
        pass
        self.i2c_bus.write_i2c_block_data(self.registers['slave'],register, [upper_byte,lower_byte])

    def get_temperature(self, register):
        '''
        Return the decoded value of a temperature from a given register
        '''
        temp_reg_data = self.i2c_bus.read_i2c_block_data(self.registers['slave'],register, 2)
        upper_byte =  temp_reg_data[0] & 0x1F
        lower_byte = (temp_reg_data[1]) / 16
        if upper_byte & 0x10:
            upper_byte = (upper_byte & 0x0F) * 16
            return 256 - (upper_byte + lower_byte)
        else: 
            upper_byte = upper_byte * 16
            return upper_byte + lower_byte

    @property
    def critcal_temp(self):
        return self.get_temperature(self.registers['t_crit'])

    @property
    def upper_temp(self):
        return self.get_temperature(self.registers['t_upper'])

    @upper_temp.setter
    def upper_temp(self,value):
        self.set_temperature(self.registers['t_upper'],value)

    @property
    def lower_temp(self):
        return self.get_temperature(self.registers['t_lower'])

    @property
    def ambient(self):
        return self.get_temperature(self.registers['t_ambient'])
