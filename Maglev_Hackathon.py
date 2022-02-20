import RPi.GPIO as GPIO                         # For raspberry pi ports
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


GPIO.setmode(GPIO.BCM)                          # Configures raspberry pi ports

GPIO_TRIGGER = 18                               # Sets GPIO trigger port input
GPIO_ECHO = 24                                  # Sets GPIO echo port input

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)              # Sets Sonar and ports
GPIO.setup(GPIO_ECHO, GPIO.IN)

def equilibrium_additonal_force():                                 # Function finds additional force needed

    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.0001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    
    TimeElapsed = StopTime - StartTime                      # Time to travel to object and back
    distance = (TimeElapsed * 34000) / 2                    # 34300cm/s is speed of sound, Divided by two since has to travel to object and back

    additional_force = (neutral_force*((minimum_height-distance)**2))/(minimum_height**2)        # Uses magnetic force ratio to find force
    return additional_force

def animate(i):                                             # Creates a live data view
    plt.cla()
    plt.ylim(0,85000)
    plt.bar('Force Calculated with Sonar Sensor to reach most Efficient Height',equilibrium_additonal_force())
    plt.title('Additional Force required for Equilibrium Levitation')
    plt.ylabel('Additional Force in N')
    plt.grid(True)

mass = float(input('Estimated Mass of Magnetic Levitating Body in kg: '))
neutral_force = ((9.81)*(mass))
minimum_height = int(input('Please enter the minimum distance to safely levitate in cm: '))     # Given by manufacturers

if __name__ == '__main__':
    try:
        while True:
            sleep_time = 0                                          # To change graph frequency if wanted
            time.sleep(sleep_time)

            animation = FuncAnimation(plt.gcf(), animate, interval = 5)
            plt.show()