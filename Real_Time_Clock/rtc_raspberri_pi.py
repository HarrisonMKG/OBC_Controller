#Maintainer Harrison Gordon
import time
from   smbus import SMBus
import datetime

class RTC:
    '''
    RTC class for MCP79410
    Data Sheet: http://ww1.microchip.com/downloads/en/devicedoc/20002266h.pdf

    Functionality:
    -Enable/Disable Internal Oscillator (Start and Stop Clock)
    -Get Date and Time from Clock
    -Enable/Disable Backup Battery
    -Reset Clock
    '''
    i2c_bus = SMBus(1)
    registers = {
        'slave' : 0x6F,
        'second': 0x00,
        'minute': 0x01,
        'hour' : 0x02,
        'wkday' : 0x3, #Regeister only utilized by battery
        'day' : 0x04,
        'month': 0x05,
        'year' : 0x06,
    }

    def _check_tick(self,clock_state):
        '''
        Args: clock_state: can either be 0, meaning off, or 1 meaning on
        Return: -2 if unable to check tick, -1 if clock is in an undesirable state, 0 if clock is in desired state
        '''
        try:
            tmp_second = self._second
            time.sleep(5)
            time_diff = self._second - tmp_second
            if clock_state == 1:
                if time_diff > 0:
                    print("Success: Clock is Ticking")
                    return 0
                else:
                    print("Fail: Clock is not ticking")
                    return -1
            elif clock_state == 0:
                if time_diff == 0:
                    print("Success: Clock is not Ticking")
                    return 0
                else:
                    print("Fail: Clock is still ticking")
                    return -1
        except:
            raise Exception("Unable to Check clock tick")

    @staticmethod
    def _encode(value):
        '''
        Encodes integer values into binary for the RTC's registers

        Returns:
            Bit encoding for RTC registers
        '''
        ones = value % 10
        tens = int(value / 10)
        return (tens<<4 | ones)

    def __init__(self, battery_state, clock_state):
        '''
        Initialization of RTC class

        Args:
            battery_state: 0 = backup battery off, 1 = backup battery on
            clock_state: 0 = clock off, 1 = clock on
        '''
        self.battery = battery_state
        self.clock = clock_state
        self.datetime = datetime.datetime()

    def reset(self):
        '''
        Reset the clock's time to zero, and battery to zero

        Returns:
            -1: The RTC was unable to be reset
            0: The RTC was able to be reset
        '''
        for self.rtc_register in self.registers:
            try:
                self.datetime = "0-1-0-0-0-0-0" 
                self.battery = 0 
            except:
               print("Unable to reset RTC")
               return -1
        return 0

    @property
    def clock(self):
        '''
        Get state of the internal oscillator of the RTC. This will control if the clock is ticking or not

        Return:
            0: Clock = OFF
            1: Clock = ON
        '''
        try:# if check_device_status is bad
            second_data = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['second'])
        except:
            raise Exception("Could not get clock state")
        return second_data >> 7 #Should return a 1 or a 0 (on or off)

    @clock.setter
    def clock(self,state):
        '''
        Set state of the internal oscillator of the RTC. This will control if the clock is ticking or not

        Args:
            State: 0 = Clock is OFF, 1 = Clock is ON
        '''
        second_data = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['second'])
        if state == 1:
            second_data = 0b10000000 | second_data
        elif state == 0:
            second_data = 0b01111111 & second_data
        else:
            raise Exception(f"Unable to set Clock. State entered must be 0 or 1, not {state}")
        self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['second'],second_data)
        self.__check_tick(state)

    @property
    def battery(self):
        '''
        Get state of the backup battery of the RTC. This will control if the backup battery or not

        Return:
            0: Battery = OFF
            1: Battery = ON
        '''
        try:
            tmp_battery = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['wkday'])
            return  (tmp_battery & 0b1000)>>3
        except:
            raise Exception("Unable to get Battery State")

    @battery.setter
    def battery(self,state):
        '''
        Set state of the backup battery of the RTC. This will control if the backup battery or not

        Args:
            state: 0 = Battery is OFF, 1 = Battery is ON
        '''
        try:
            if not (state == 0 or state == 1):
                raise Exception("Not valid value for battery, must be 0 (OFF) or 1 (ON)")
            tmp_battery = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['wkday'])
            if state == 0:
                tmp_battery = tmp_battery & 0b11110111
            else:
                tmp_battery = tmp_battery | 0b1000
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['wkday'],tmp_battery)
        except:
            raise Exception("Unable to Set Battery")

    @property
    def _second(self):
        '''
        Get seconds value from RTC register

        Return:
            Integer representing seconds data
        '''
        try:
            tmp_second = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['second'])
            tmp_second = tmp_second & 0b01111111 #Remove the start oscillation bit
            return (tmp_second>>4)*10 + (tmp_second & 0b00001111)
        except:
            print("Unable to Get Second")

    @second.setter
    def _second(self,value):
        '''
        Set seconds value from RTC register

        Args:
            Value: Integer value to set the seconds register to
        '''
        try:
            tmp_second = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['second']) & 0b10000000
            #^^^ could be replaced by clock_status()
            tmp_second = self.clock
            tmp_second = tmp_second | RTC._encode(value)
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['second'],tmp_second)
        except:
            print("Unable to Set second")

    @property
    def _minute(self):
        '''
        Get minute value from RTC register

        Return:
            Integer representing minute data
        '''
        try:
            tmp_minute =  self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['minute'])
            tmp_minute = tmp_minute & 0b01111111 #Remove uninitialized bit
            return (tmp_minute >>4)*10 + (tmp_minute & 0b00001111)
        except:
            print("Unable to Get minute")

    @minute.setter
    def _minute(self,value):
        '''
        Set minutes value from RTC register

        Args:
            Value: Integer value to set the minutes register to, must be eligible minute value (1-60)
        '''
        try:
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['minute'],RTC._encode(value) )
        except:
            print("Unable to set minute")

    @property
    def _hour(self): # AM/PM untested stick to 24hr time
        '''
        Get hour value from RTC register

        Return:
            Integer representing hour data
        '''
        try:
            tmp_hour =  self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['hour'])
            hour_format = tmp_hour >> 6 & 0x1
            if hour_format == 0:
                tmp_hour = ((tmp_hour>>4) & 0x03)*10 + (tmp_hour & 0x0F)
            else:
                tmp_hour = ((tmp_hour>>4) & 0x01)*10 + (tmp_hour & 0x0F)
                am_pm = (tmp_hour>>4) & 0x02
                if am_pm == 1:
                    am_pm = 'PM'
                else:
                    am_pm = 'AM'
                tmp_hour = str(tmp_hour) + am_pm
            return(tmp_hour)
        except:
            print("Unable to get current hour")

    @hour.setter
    def _hour(self,value):
        '''
        Set hour value from RTC register

        Args:
            Value: Integer value to set the hour register to, must be an eligible hour (1-60)
        '''
        try:
            tmp_hour =  (self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['hour']) & 0b11000000) | RTC._encode(value)
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['hour'],tmp_hour)
        except:
            print("Unable to Set Hours")

    @property
    def _day(self):
        '''
        Get day value from RTC register

        Return:
            Integer representing day data
        '''
        try:
            tmp_days = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['day'])
            tmp_days = tmp_days & 0b00111111 #Remove unused bits
            return (tmp_days >>4)*10 + (tmp_days & 0b00001111)
        except:
            print("Unable to Get Days")

    @day.setter
    def _day(self,value):
        '''
        Set day value from RTC register

        Args:
            Value: Integer value to set the day register to, must be an eligible amount for days in month
        '''
        try:
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['day'],RTC._encode(value))
        except:
            print("Unable to Set Days")

    @property
    def _month(self):
        '''
        Get month value from RTC register
        1 -> January
        2 -> February
        3 -> March
        4 -> April
        5 -> May
        6 -> June
        7 -> July
        8 -> August
        9 -> September
        10 -> October
        11 -> November
        12 -> December

        Return:
            Integer representing month data
        '''
        try:
            tmp_months = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['month'])
            tmp_months = tmp_months & 0b00011111 #Remove unused bits
            return (tmp_months >>4)*10 + (tmp_months & 0b00001111)
        except:
            print("Unable to Get Days")

    @month.setter
    def _month(self,value):
        '''
        Set month value from RTC register
        1 -> January
        2 -> February
        3 -> March
        4 -> April
        5 -> May
        6 -> June
        7 -> July
        8 -> August
        9 -> September
        10 -> October
        11 -> November
        12 -> December

        Args:
            Value: Integer value to set the month register to, must be an eligible month (1-12)
        '''
        try:
            tmp_month= RTC._encode(value) | (self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['month']) & 0b11100000)
            self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['month'],tmp_month)
        except:
            print("Unable to Set Month")

        @property
        def _year(self):
            '''
            Get year value from RTC register

            Args:
                Value: Integer value to set the year register to, must be eligible value (0-99 which maps to 2000-2099)
            '''
            try:
                tmp_years = self.i2c_bus.read_byte_data(self.registers['slave'],self.registers['year'])
                return (tmp_years >>4)*10 + (tmp_years & 0b00001111) + 2000
            except:
                print("Unable to Get Year")

        @year.setter
        def _year(self,value):
            '''
            Set year value from RTC register

            Args:
                Value: Integer value to set the year register to, must be eligible value (0-99 which maps to 2000-2099)
            '''
            try:
                value -= 2000
                self.i2c_bus.write_byte_data(self.registers['slave'],self.registers['year'],RTC._encode(value))
            except:
                print("Unable to Get Year")

        @property
        def datetime(self):
            return f"{self._year}-{self._month}-{self._day}-{self._hour}-{self._minute}-{self._second}" 

        @datetime.setter
        def datetime(self,datetime_raw):
            """Checks if datetime_raw entered is valid datetime. Sets the datetime of the RTC in terms of years, months, days, hours, minutes, and seconds

            Args:
                datetime_raw (string): datetime in format "%Y-%m-%d %H:%M:%S" 

            Raises:
                RuntimeError: _description_
            """
            try:
                datetime_split = value.split('-')
                datetime.datetime(datetime_split[0],datetime_split[1],datetime_split[2],datetime_split[3],datetime_split[4],datetime_split[5],0)
                self._second = datetime_split[5]
                self._minute = datetime_split[4]
                self._hour = datetime_split[3]
                self._day = datetime_split[2]
                self._month = datetime_split[1]
                self._year = datetime_split[0]
            except:
                raise RuntimeError(f"Unvalid datetime: {datetime_raw}")