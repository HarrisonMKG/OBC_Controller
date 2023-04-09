import Yaml
import RTC 
import Temperature_Sensor
import argparse

class OBC_Contoller:
    """This is a class to contain various fucntions and operations of the on board controller. This class is meant to be used through a CLI.
        
        Functionality:
            1) Yaml file configurability 
            2) Aquire telemetry from multiple devices
    """
    @staticmethod
    get_config():
        pass

    @staticmethod
    init_rtc():
        config = get_config()
        rtc_config = config["rtc"]
        return RTC(rtc_config['battery_state'],rtc_config['clock_state'],rtc_config['status'])

    @staticmethod
    init_temp():
        config = get_config()
        temp_config = config["temperature_sensor"]
        return Temperature_Sensor(temp_config["status"],temp_config["critical_temp"],temp_config["upper_temperature",temp_config["lower_temperature"])


    @staticmethod
    def get_telemetry(verbose):
        temp_sense_contoller = init_temp()
        rtc_controller = init_rtc() 
