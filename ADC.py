#===========================================================
#imports
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep
import time, datetime, threading
#===========================================================
#Spi set up
spi = busio.SPI(clock=board.SCK,MISO=board.MISO,MOSI=board.MOSI)

#CS Line
cs = digitalio.DigitalInOut(board.D5)

runtime = 0
delay = 1
#============================================================
#Code

#create MCP
mcp = MCP.MCP3008(spi, cs)

#analog input channel
chan = AnalogIn(mcp, MCP.P0)


print(f'Raw ADC Value: {chan.value}')
print(f'ADC Voltage: {str(chan.voltage)} V')
line =  ('Runtime',"Temp Reading", "Temp")
print("{0: <20} {1: <20} {2: <20}".format(*line))



#==============FUNCTIONS+++++++++++++++++++++++++++++++++++++

#Threaded function to get the reading every delay amount of seconds
def getReading():
    global runtime
    global delay
    value = chan.value
    line = (f'{runtime}s',value, f'{chan.voltage}V')
    print("{0: <20} {1: <20} {2: <20}".format(*line))
    runtime += delay
    thread = threading.Timer(delay, getReading)
    thread.daemon = True
    thread.start()


#TODO: Implement Interrupt funcionality

#TODO:HANDLE conversion


#+++++++++++++++++++++Run the Program++++++++++++++++++++++++++
if __name__ == "__main__":
   getReading()
   while True:
       pass
