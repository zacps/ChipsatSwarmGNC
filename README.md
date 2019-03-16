# Chipsat Swarm GNC Project

Forked from https://github.com/roboticexplorationlab/sprite.

## Accessing the Serial Console
nearly any terminal program can communicate with the sprite (baud=112500, data=8 bit, parity=None, flow control=XON/XOFF). For example...

### MacOS
1. In terminal type: `ls /dev/tty.*`. The sprite will likely be listed as `/dev/tty.usbmodem_____`
2. Now enter: `screen /dev/tty.YOURBOARDNAMEHERE 115200`
3. You may or may not see a prompt, press <kbd>Ctrl</kbd>+<kbd>C</kbd> to halt the sprite
4. You can now enter the REPL by pressing any key, or hit <kbd>Ctrl</kbd>+<kbd>D</kbd> to reload the main.py
5. Exit screen at any time by pressing <kbd>Ctrl</kbd>+<kbd>A</kbd>+<kbd>\</kbd>

### Windows 
1. Windows doesn't have a built-in terminal program like MacOS. Personally, I like [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html), or [termite](https://www.compuphase.com/software_termite.htm). You can also use the arduino serial monitor if you'd like!
2. For something like PuTTY, set the Connection Type to Serial
3. Press the <kbd>Windows Key</kbd> and type device manager (select it)
4. In device manager, scroll down to "Ports (COM & LPT)" and expand it
5. Plug in, then unplug the sprite and notice the impacted "COM" port.
6. Return to PuTTY and enter "COM___" in the "Serial Line" field, and then click "Open"

## Running

Put all the files located in [/software/](/software/) on to the sprite and start the serial console (as described above). After pressing <kbd>Ctrl</kbd>+<kbd>C</kbd> to halt the sprite, press any key to enter the REPL, then type

```
import NAMEOFFILE
```

and press enter to execute the example. For example, it we wanted to run blink.py, it would be...

```
import blink
```

1. blink.py - will blink the green LED. 
2. i2c_IMU.py - samples all available sensors on the IMU and prints the results
3. cursor.py - uses the X,Y data from the IMU accelerometer and moves the computer cursor accordingly
4. cpc_test.py - example transmit message for the CC1101 radio
