#===========================================================
#imports
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep
import time, datetime, threading
import RPi.GPIO as GPIO

# define global variables
global chan
global runtime
global delay
#===========================================================
def setup():
    #Spi set up
    spi = busio.SPI(clock=board.SCK,MISO=board.MISO,MOSI=board.MOSI)

    #CS Line
    cs = digitalio.DigitalInOut(board.D5)

    global runtime
    runtime = 0

    global delay
    delay = 1

    # define button pin
    btn_toggle = 17 # GPIO 17 on pin 11

    # set up board in BCM mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(btn_toggle, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

    # add an event for button click 
    GPIO.add_event_detect(btn_toggle, GPIO.FALLING, callback= btn_toggle_pressed, bouncetime= 2200)
#============================================================
#Code

   # create MCP
    mcp = MCP.MCP3008(spi, cs)

    #analog input channel
    global chan
    chan = AnalogIn(mcp, MCP.P0)


    print(f'Raw ADC Value: {chan.value}')
    print(f'ADC Voltage: {str(chan.voltage)} V')
    line =  ('Runtime',"Temp Reading", "Temp")
    print("{0: <20} {1: <20} {2: <20}".format(*line))



#==============FUNCTIONS+++++++++++++++++++++++++++++++++++++
# button handler
def btn_toggle_pressed(channel):
    print('pressed')


#Threaded function to get the reading every delay amount of seconds
def getReading():
    global runtime
    global delay
    global chan
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
   setup()
   getReading()
   while True:
       pass
