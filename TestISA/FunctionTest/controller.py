import serial
import os
import sys
import time
import keyboard
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


direction = None
while True:
    action = ' '
    #time.sleep(1)

    if keyboard.is_pressed('w'):
        action = 'w'
    elif keyboard.is_pressed('s'):
        action = 's'
    elif keyboard.is_pressed('d'):
        action = 'd'
    elif keyboard.is_pressed('a'):
        action = 'a'
    elif keyboard.is_pressed('r'):
        action = 'r'
    if action in "wasdr":
        write_read(action)
        time.sleep(0.05)
        print(action)