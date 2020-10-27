#===========================================================
#imports
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#===========================================================
#Spi set up
spi = busio.SPI(clock=board.SCK,MISO=board.MISO,MOSI=board.MOSI)

#CS Line
cs = digitalio.DigitalInOut(board.D5)

#============================================================
#Code

#create MCP
mcp = MCP.MCP3008(spi, cs)

#analog input channel
chan = AnalogIn(mcp, MCP.P0)


print(f'Raw ADC Value: {chan.value}')
print(f'ADC Voltage: {str(chan.voltage)} V')
