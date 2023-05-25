from STM32.stm32 import STM32
import yaml

class Comms(STM32):
    
    def __init__(self,config_path):
        self.config = self.get_config(config_path)["comms"]
        self.cmds = self.config["cmds"]
        super().__init__(self.config["address"])

    def get_config(self,config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def led_off(self):
        super().transmit(self.cmds["led_off"])

    def led_on(self):
        super().transmit(self.cmds["led_on"])

    def led_state(self):
        return super().receive(1)
