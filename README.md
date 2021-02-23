# Introduction
 This project focuses on the development of a Raspberry Pi based musical synthesizer with a variety of user inputs. The MIDI controller used in this case is an *AKAI LPK25 Laptop Performance Keyboard*.

The following diagram illustrates the setup of each component:
![Diagram](Diagram.png?raw=true)


# Function
The synthesizer works by utilizing a variety of python packages/distributions and MIDI software. The MIDI software utilized for real-time playing is *Fluidsynth*, and is based on the Soundfont 2 specification. *Fluidsynth* generates audio by reading and handling MIDI events from MIDI input devices, such as our keyboard, and by using a desired SoundFont in the form of an sf2 file. Because the keypad is an I2C device, the python script utilizes *CircuitPython* which is a microcontroller software, alongside a python distribution that utilizes the *CircuitPython* library for this specific piece of hardware.

The synthesizer works by plugging in a MIDI controller into the USB port of the Raspberry Pi. Upon turning on the Raspberry Pi and logging in, the python script runs in the background. 

This script listens for the **black** button to be pressed, and in doing so, starts up the *Fluidsynth* as a server, uses the *ALSA* sound module, and connects the MIDI controller client to the *Fluidsynth* client. From there, the blue and green buttons, as well as the keypad, may be used. Because *Fluidsynth* takes commands from its own proprietary shell, the *Telnet* python module is used to send commands to the *Fluidsynth* server. 

The **blue** button is used to send a command to *Fluidsynth* to turn on the chorus effect, and after another push, turns it off. 

The **green** button is used to send a command to *Fluidsynth* to turn on the reverb effect, and after another push, turns it off. 

The **keypad** is used to change the instrument being used, with each key sending a command to *Fluidsynth* to select a specific instrument. 

The **asterisk** and **pound** keys send a command to *Fluidsynth* to change the value of the gain. Upon each push of the asterisk/pound key, we decrement/increment the value of the gain by 0.5, then send that value to *Fluidsynth*. 

The user may play as much as they like, and when finished, may press the **black** button again, which kills the *Fluidsynth* program currently running. Because the python script runs in the background, and constantly awaits the press of the **black** button, the user may turn this off and on at their own leisure.
