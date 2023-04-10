import time
import rtc

my_rtc = RTC(1,1,0) # Initalize RTC
my_rtc.datetime = "2021-2-5-0-15-34" # Set Time
while 1:
    time.sleep(1)
    print(f"{my_rtc.datetime}  |  [Year,Month,Day,Hour,Minute,Second]")
