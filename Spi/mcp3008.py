import time
import os
import spidev

class MCP3008:
    '''SPI interface for the ADC MCP3008 

    Datasheet: https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf

    Features:
        -Set ADC Channel
        -Read ADC Channel
    '''

    sample_rate = 200000

    def __init__(self, spi_contoller, config_path='mcp3008_config.yml'):
        self.spi = spidev.SpiDev()
        try:
            self.open_yaml(mcp3008_config_path)
        except:
            raise Exception(f"Unable to open config file {mcp3008_config_path}")
        self.spi.spi_mode = self.config['spi mode'] 
        self.spi.max_speed_hz = self.config['speed'] 
        self.spi.bus = self.config['bus']
        self.chip_enable = self.config['chip_enable']
        self.channels = self.config['channels']

        self.spi.open(self.spi.bus,self.spi.chip_enable)

    def tx_mosi(data):
        msb = data >> 8
        lsb = data & 0xFF
        self.spi.xfer2([msb,lsb])

    def rx_miso():
        return self.spi.readbytes(self.sample_rate)

    def read_channel(channel):
        set_channel(channel)
        data = self.spi.readbytes(self.sample_rate)
        return data

    def open_yaml(self, config_path='mcp3008_config.yml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def set_channel(channel):
        if(channel == 0) and self.channels[0]:
            cmd = "1000"
        elif(channel == 1) and self.channels[1]:
            cmd = "1001"
        elif(channel == 2) and self.channels[2]:
            cmd = "1010"
        elif(channel == 3) and self.channels[3]:
            cmd = "1011"
        elif(channel == 4) and self.channels[4]:
            cmd = "1100"
        elif(channel == 5) and self.channels[5]:
            cmd = "1101"
        elif(channel == 6) and self.channels[6]:
            cmd = "1110"
        elif(channel == 7) and self.channels[7]:
            cmd = "1111"
        else:
            throw ValueError(f"Channel {channel}, does not exist or is not defined.")

        self.tx_mosi(cmd)
