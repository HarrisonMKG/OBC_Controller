class SPI_Controller:

    @staticmethod
    def list_enable():
        return os.system('ls /dev/*spi*')

    def init(self, config_path):
        self.spi = spidev.SpiDev()
        self.open_yaml(config_path)
        self.spi.open(self.spi.bus,self.spi.chip_enable)

    def open_yaml(self, config_path):
        with open('config.yml', 'r') as file:
            self.config = yaml.safe_load(file)
        self.devices =  self.config['devices'] 
        self.spi.spi_mode = self.config['spi mode'] 
        self.spi.max_speed_hz = self.config['speed'] 
        self.spi_init()
    
    def transmit(data):
        msb = data >> 8
        lsb = data & 0xFF
        self.spi.xfer2([msb,lsb])

    def recieve(sample_rate):
        return self.spi.readbytes(sample_rate)

