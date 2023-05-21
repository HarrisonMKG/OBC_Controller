from stm32 import STM32

expected_bytes = 4 
stm32 = STM32(0x15)

print(stm32.recieve(expected_bytes))

data = [stm32.defined_bits.get('BAD_BYTE'),0x5,0x7,0x15,0x8]
stm32.transmit(data)

print(stm32.recieve(expected_bytes))
