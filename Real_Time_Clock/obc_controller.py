import yaml
from rtc import RTC 
from temperature_sensor import Temperature_Sensor
import argparse

class OBC_Controller:
    """This is a class to contain various fucntions and operations of the on board controller. This class is meant to be used through a CLI.
        
        Functionality:
            1) Yaml file configurability 
            2) Aquire telemetry from multiple devices
    """
    config_path =  "controller_config.yml"

    @staticmethod
    def get_config():
        with open(OBC_Controller.config_path, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def init_rtc():
        config = OBC_Controller.get_config()
        rtc_config = config["rtc"]
        return RTC(rtc_config['battery_state'],rtc_config['clock_state'],rtc_config['i2c_status'])

    @staticmethod
    def init_temp():
        config = OBC_Controller.get_config()
        temp_config = config["temperature_sensor"]
        return Temperature_Sensor(temp_config["i2c_status"])
        #return Temperature_Sensor(temp_config["i2c_status"],temp_config["critical_temperature"],temp_config["upper_temperature"],temp_config["lower_temperature"])

    @staticmethod
    def get_telemetry():
        temp_interface = OBC_Controller.init_temp()
        rtc_interface = OBC_Controller.init_rtc() 

        print(f"Time: {rtc_interface.datetime}")
        print(f"OBC Ambient Temperature: {temp_interface.ambient} °C")


    def test():
        print("hello")

if __name__  == '__main__':
    FUNCTION_MAP =  {
        'telemetry': OBC_Controller.get_telemetry,
        'test' : OBC_Controller.test,
        }
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=FUNCTION_MAP.keys())
    args = parser.parse_args()

    func = FUNCTION_MAP[args.cmd]
    func()
