import temperature_sensor
import time

temp_sensor = temperature_sensor()

while 1:
    time.sleep(1)
    temperature = temp_sensor.get_ambient_temp
    print(f"Current Temperature is :{temp_sensor.ambient}") 