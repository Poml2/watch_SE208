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

#Graphic parameters
lcd = LCD_0inch96()   # Initializing the scree n
lcd.fill(BLACK)       # clearing any exsiting diplay

WIDTH_SCREEN = 160    # width of the screen  
HEIGHT_SCREEN = 80    # height of the screen

HEIGHT_GRAPHIC = 60   # height of the graphic
WIDTH_GRAPHIC = WIDTH_SCREEN    # width of the graphic  
  
#ADC parameters
ADC_PIN = 26
ADC_MAX_VALUE = 2**16
ADC_VOLTAGE = 3.3

#FFT parameters
Fe = 80                  # Sampling frequency HZ
window_size = 400                   # number of samples
windowed_signal = [0]*window_size

# get the ADC value and display it on the screen
def interruption_handler(pin):
    analog_read = adc.read_u16()
    #print(analog_read)

    windowed_signal.append(analog_read)
    windowed_signal.pop(0)

    # this function must give to us the bpm value
    bpm = getbpm(); 
    #print(bpm)
    # function to display over the screen
    lcd.fill(BLACK)
    
    display_bpm(bpm)
    display_tension(from_adc_to_voltage(analog_read))
    print(from_adc_to_voltage(analog_read))
    print(',')
    #display_frame()
    #display_signal()
    display_point(79,39,RED)

    lcd.display()

def from_adc_to_voltage(analog_read) : 
    return analog_read * ADC_VOLTAGE / ADC_MAX_VALUE

# display the value on the screen
def display_tension(analog_read) : 
    lcd.text("Voltage : "+str(analog_read),5,20,GREEN)
    

# get the bpm value by using the ADC value
def getbpm() :
    signal = windowed_signal
    # Calcul de la moyenne du signal sur cette fenêtre
    average = sum(signal) / len(signal)

    '''
    En étudiant plusieurs électrocardiogrammes, nous avons remarqué que le signal d'une onde R
    allait de son minimum à son maximum en au plus 0,1 secondes.
    Donc pour détecter un front montant, on compare la valeur de signal[i] à la moyenne,
    et celle de signal[i + delta] à la moyenne, où:
    i correspond à un échantillon donné
    delta correspond au nombre d'échantillons pendant 0,1 secondes: delta = 0,1*Fe
    '''
    delta = int(round(0.25 * Fe))
    peak_indices = [0] * delta  # Cette liste va servir à stocker les indices des fronts montants
    peak_flag = 0  # Flag servant à éviter les erreurs de comptage

    for k in range(delta, len(signal)):
        if (signal[k - delta] < average) and (signal[k] > average) and (peak_flag == 0):
            peak_indices.append(1)
            peak_flag = delta  # Pendant delta échantillons, on ne cherche plus de fronts montants
        else:
            if peak_flag > 0:
                peak_flag -= 1
            peak_indices.append(0)

    peak_counter = sum(peak_indices)  # Compteur de fronts montants
    # Rythme cardiaque
    return 60 * peak_counter * Fe / len(signal)

# display the value on the screen
def display_bpm(bpm = 0) : 
    lcd.text("BPM : "+str(bpm),5,5,GREEN)

# display a frame on the border screen
def display_frame() : 
    # display the frame
    # argument : x,y,lenght,color
    lcd.hline(0,0,160,BLUE)
    lcd.hline(0,79,160,BLUE)
    lcd.vline(0,0,80,BLUE)
    lcd.vline(159,0,80,BLUE)

# display the signal on the screen 
def display_signal() : 
    # display the signal
    for i in range(0,WIDTH_GRAPHIC) : 
        lcd.vline(i,HEIGHT_SCREEN-1,1,RED)
    
    for i in range(0,HEIGHT_GRAPHIC) : 
        lcd.vline(0,HEIGHT_SCREEN-i,1,RED)

# display the point
# argument : x,y,color
def display_point(x,y,color) : 
    lcd.vline(x,y,1,color)
     
#Main function
if __name__ == "__main__":
    adc = ADC(Pin(ADC_PIN, mode=Pin.IN))
    soft_timer = Timer(mode=Timer.PERIODIC, freq = 80, callback=interruption_handler)


    
