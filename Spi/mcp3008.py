import time
import SPI_Controller

class MCP3008:

    sample_rate = 200000

    def __init__(self, spi_contoller):
        self.spi_contoller = spi_contoller
        self.config = spi_contoller.config['mcp3008']
        self.chip_enable = spi_contoller['mcp3008']['chip_enable']
        self.channels = spi_contoller.config['mcp3008']['channels']

    def read_channel(channel):
        set_channel(channel)
        data = self.spi.readbytes(self.sample_rate)
        return data

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

        self.spi_contoller.send_data(channel)
