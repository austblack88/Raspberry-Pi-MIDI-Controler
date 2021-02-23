# Synthomaniacs
# CS121
import sys
import RPi.GPIO as GPIO
import time
import os
import subprocess, signal
from telnetlib import Telnet
import board
import busio
import sparkfun_qwiickeypad
import digitalio

# Button Pin #'s
GREEN = 16
BLUE = 19
BLACK = 21
INTERRUPT = 6

# Settings
max_gain = 5
gain = 2.5
min_gain = 0

# Create bus object using our board's I2C port
i2c = busio.I2C(board.SCL, board.SDA)

# Create relay object
keypad = sparkfun_qwiickeypad.Sparkfun_QwiicKeypad(i2c)

# Set up Interrupt pin on GPIO D6 with a pull-up resistor
keypad_interrupt_pin = digitalio.DigitalInOut(board.D6)
keypad_interrupt_pin.direction = digitalio.Direction.INPUT
keypad_interrupt_pin.pull = digitalio.Pull.UP

def beep():
    fluid.write(b"noteon 1 70 100\n")
    time.sleep(0.2)
    fluid.write(b"noteoff 1 70\n")

def kill_synth(pfs):
    print ("Quitting Synthesizer...")
    os.killpg(pfs.pid, signal.SIGTERM)
    time.sleep(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLUE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLACK, GPIO.IN, pull_up_down = GPIO.PUD_UP)

black_flag = 0
green_flag = 0
blue_flag = 0
while True:
    # -------------------------------- Start BLACK Button ----------------------------------------
    BLACK_STATE = GPIO.input(BLACK)
    if BLACK_STATE == False and black_flag == 0:
        print ("Starting Synthesizer...\n")
        fs = subprocess.Popen("fluidsynth -a alsa -g 2.5 -C off -R off -r 48000 -i -s /usr/share/sounds/sf2/FluidR3_GM.sf2 &", shell = True, preexec_fn = os.setsid)
        time.sleep(5)
        fluid = Telnet("localhost", "9800")
        subprocess.call("aconnect 20:0 128:0", shell = True)

        # Set Channel 0 to 000-000 Yamaha Grand Piano
        fluid.write(b"select 0 1 0 0\n")
        # Set Channel 1 to 008-080 Sine Wave
        fluid.write(b"select 1 1 8 80\n")

        print ("\nSynthesizer Ready\n")
        time.sleep(1)
        black_flag = 1

    BLACK_STATE = GPIO.input(BLACK)
    if BLACK_STATE == False and black_flag == 1:
        kill_synth(fs)
        black_flag = 0
    # -------------------------------- End BLACK Button ------------------------------------------
    # -------------------------------- Start BLUE Button -----------------------------------------
    BLUE_STATE = GPIO.input(BLUE)
    if BLUE_STATE == False and black_flag == 1 and blue_flag == 0:
        fluid.write(b"chorus on\n")
        print("Chorus On")
        time.sleep(.5)
        blue_flag = 1

    BLUE_STATE = GPIO.input(BLUE)
    if BLUE_STATE == False and black_flag == 1 and blue_flag == 1:
        fluid.write(b"chorus off\n")
        print("Chorus Off")
        time.sleep(.5)
        blue_flag = 0
    # -------------------------------- End BLUE Button -------------------------------------------
    # -------------------------------- Start GREEN Button ----------------------------------------
    GREEN_STATE = GPIO.input(GREEN)
    if GREEN_STATE == False and black_flag == 1 and green_flag == 0:
        fluid.write(b"reverb on\n")
        fluid.write(b"rev_setroomsize 0.9\n")
        print("Reverb On")
        time.sleep(.5)
        green_flag = 1

    GREEN_STATE = GPIO.input(GREEN)
    if GREEN_STATE == False and black_flag == 1 and green_flag == 1:
        fluid.write(b"reverb off\n")
        print("Reverb Off")
        time.sleep(.5)
        green_flag = 0
    # -------------------------------- End GREEN Button ------------------------------------------
    # -------------------------------- Start KEYPAD ----------------------------------------------
    if (not keypad_interrupt_pin.value) and (black_flag == 1):
        # Request the next key pressed.
        keypad.update_fifo()
        key = keypad.button
        if key != 0:
            c = chr(key)
            if c == '1':
                fluid.write(b"select 0 1 0 0\n")
                print("Yamaha Grand Piano")
            elif c == '2':
                fluid.write(b"select 0 1 0 2\n")
                print("Electric Piano")
            elif c == '3':
                fluid.write(b"select 0 1 0 3\n")
                print("Honky Tonk")
            elif c == '4':
                fluid.write(b"select 0 1 0 7\n")
                print("Clavinet")
            elif c == '5':
                fluid.write(b"select 0 1 0 12\n")
                print("Marimba")
            elif c == '6':
                fluid.write(b"select 0 1 0 18\n")
                print("Rock Organ")
            elif c == '7':
                fluid.write(b"select 0 1 0 26\n")
                print("Jazz Guitar")
            elif c == '8':
                fluid.write(b"select 0 1 0 36\n")
                print("Slap Bass")
            elif c == '9':
                fluid.write(b"select 0 1 0 62\n")
                print("Synth Brass 1")
            elif c == '0':
                fluid.write(b"select 0 1 0 50\n")
                print("Synth Strings 1")
            elif c == '#':
                if gain < max_gain:
                    gain += 0.5
                    fluid.write(b"gain " + str(gain).encode('ascii') + b"\n")
                    print("Gain = " + str(gain))
                elif gain == max_gain:
                    beep()
                    print ("Gain is at Maximum")
            elif c == '*':
                if gain > min_gain:
                    gain -= 0.5
                    fluid.write(b"gain " + str(gain).encode('ascii') + b"\n")
                    print("Gain = " + str(gain))
                elif gain == min_gain:
                    beep()
                    print ("Gain is at Minimum")

            time.sleep(0.25)
    # -------------------------------- End KEYPAD ------------------------------------------------
