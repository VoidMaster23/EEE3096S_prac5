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
global thread
global count
global vref
global two16

#===========================================================
def setup():
    #Spi set up
    spi = busio.SPI(clock=board.SCK,MISO=board.MISO,MOSI=board.MOSI)

    #CS Line
    cs = digitalio.DigitalInOut(board.D5)

    global runtime
    runtime = 0

    global count
    count = 0 

    global delay
    delay = 10

    global vref
    vref = 3.3
    
    global two16
    two16 = 2**16

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


#    print(f'Raw ADC Value: {chan.value}')
 #   print(f'ADC Voltage: {str(chan.voltage)} V')
    line =  ('Runtime',"Temp Reading", "Temp")
    print("{0: <20} {1: <20} {2: <20}".format(*line))
    sleep(3)


#==============FUNCTIONS+++++++++++++++++++++++++++++++++++++
# button handler
def btn_toggle_pressed(channel):
    # count keeps track of how many times button has been pushed
    global count
    count = count + 1

    global delay
    if count==0:
        delay = 10

    if count==1:
        delay = 5

    if count==2:
        delay = 1

    if count==3:
        delay = 10 # revert to default delay
        count = 0 # reset counter


# function to process raw sensor data and print output
def getReading():
    global runtime
    global chan
    global vref
    global two16

    value = chan.value
    temp = (vref/(two16*0.01))*(value - (two16*0.5)/vref)
    line = (f'{runtime}s',value, f'{temp} {chr(176)}C')
    print("{0: <20} {1: <20} {2: <20}".format(*line))


# function that executes threads based on current delay value
def InterruptCurrentThread():
    global runtime
    global delay
    global thread

    # start timing since output has been displayed
    start_time = time.time()

    # initialised elapsed time variable
    elapsed_time = time.time() - start_time

    # wait until elapsed time is greater than the delay
    while elapsed_time<delay:
        elapsed_time = time.time() - start_time # update elapsed time

    # update runtime with correct delay
    runtime = runtime + int(elapsed_time)

    # start new thread that executes without any delay
    thread = threading.Timer(0, getReading)
    thread.daemon = True
    thread.start()

    # update the runtime
    #runtime += delay

#+++++++++++++++++++++Run the Program++++++++++++++++++++++++++
if __name__ == "__main__":
   setup()
   getReading() # get first reading at 0 seconds
   while True:
       InterruptCurrentThread()

