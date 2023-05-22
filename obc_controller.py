import yaml
from Real_Time_Clock.rtc import RTC 
from Temperature_Sensor.temperature_sensor import Temperature_Sensor
import argparse
from STM32.stm32 import STM32

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
    def init_rtc(config):
        rtc_config = config["rtc"]
        return RTC(rtc_config['battery_state'],rtc_config['clock_state'],rtc_config['i2c_status'],rtc_config['datetime'])

    @staticmethod
    def init_temp(config):
        temp_config = config["temperature_sensor"]
        return Temperature_Sensor(temp_config["i2c_status"],temp_config["critical_temperature"],temp_config["upper_temperature"],temp_config["lower_temperature"])

    @staticmethod
    def init_hardware():
        config = OBC_Controller.get_config()
        OBC_Controller.init_rtc(config)
        OBC_Controller.init_rtc(config)

    @staticmethod
    def get_comms_data():
        config = OBC_Controller.get_config()
        comms_board = STM32(config["comms"]["address"])
        expected_bytes = 4
        rx = comms_board.receive(expected_bytes)
        print(rx)

    @staticmethod
    def set_comms_data():
        config = OBC_Controller.get_config()
        comms_board = STM32(config["comms"]["address"])
        data = [9,5,1,2]
        comms_board.transmit(data)

    @staticmethod
    def get_telemetry():
        temp_interface = Temperature_Sensor()
        rtc_interface = RTC() 

        print(f"Time: {rtc_interface.datetime}")
        print(f"OBC Ambient Temperature: {temp_interface.ambient} °C")

if __name__  == '__main__':
    FUNCTION_MAP =  {
        'telemetry': OBC_Controller.get_telemetry,
        'init': OBC_Controller.init_hardware,
        'stm_tx': OBC_Controller.set_comms_data,
        'stm_rx': OBC_Controller.get_comms_data,
        }
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=FUNCTION_MAP.keys())
    args = parser.parse_args()

    func = FUNCTION_MAP[args.cmd]
    func()
