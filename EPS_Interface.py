mport time
from smbus import SMBus

class EPS:
    """Interface for Clyde Space EPS Board
        
    """

    i2c_bus = SMBus(1)
    slave_address = 0x2B;

    def _init_(status):
        self.i2c_status = status

    def get_board_status():
        return self.i2c_bus.read_byte_data(slave_address,0x01)

    def get_board_status():
        return self.i2c_bus.read_byte_data(slave_address,0x01)

    def get_telemetry_verbose():
        return self.i2c_bus.read_byte_data(slave_address,0x10)
