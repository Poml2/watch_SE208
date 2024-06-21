from machine import Pin,SPI,PWM,Timer, Pin, ADC
from ST7735 import LCD_0inch96
import framebuf
import time

# !  Important !
# run : ./pyboard.py --device /dev/ttyACM0 code.py 
# get_data_throught serial port : cat /dev/ttyACM0 

#color is BGR
RED = 0x00F8
GREEN = 0xE007
BLUE = 0x1F00
WHITE = 0xFFFF
BLACK = 0x0000

lcd = LCD_0inch96()   # Initializing the scree n
lcd.fill(BLACK)       # clearing any exsiting diplay
WIDTH_SCREEN = 160    # width of the screen  
HEIGHT_SCREEN = 80    # height of the screen

#ADC parameters
ADC_PIN = 26
ADC_MAX_VALUE = 2**16
ADC_VOLTAGE = 3.3

# get the ADC value and display it on the screen
def interruption_handler(pin):
    analog_read = adc.read_u16()
    print(analog_read)

    # function to display over the screen
    lcd.fill(BLACK)

    display_tension(from_adc_to_voltage(analog_read))
    display_bpm(10)
    display_frame()
    display_point(79,39,RED)
    
    lcd.display()

def from_adc_to_voltage(analog_read) : 
    return analog_read * ADC_VOLTAGE / ADC_MAX_VALUE

# display the value on the screen
def display_tension(analog_read) : 
    lcd.text("Voltage : "+str(analog_read),5,5,GREEN)

# display the value on the screen
def display_bpm(bpm) : 
    lcd.text("BPM : "+str(bpm),5,20,GREEN)

# display a frame on the border screen
def display_frame() : 
    # display the frame
    # argument : x,y,lenght,color
    lcd.hline(0,0,160,BLUE)
    lcd.hline(0,79,160,BLUE)
    lcd.vline(0,0,80,BLUE)
    lcd.vline(159,0,80,BLUE)

def display_point(x,y,color) : 
    # display the point
    # argument : x,y,color
    lcd.vline(x,y,1,color)
     
#Main function
if __name__ == "__main__":
    adc = ADC(Pin(ADC_PIN, mode=Pin.IN))
    soft_timer = Timer(mode=Timer.PERIODIC, period=1, callback=interruption_handler)


    
