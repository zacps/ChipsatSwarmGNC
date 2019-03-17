# ChipSAT Mesh Networking Project

ChipSATs are tiny, gram-sized satellites designed to be deployed into space. They are able to be equipped with sensors such as a camera, spectrophotometer, or magnetometer, and can transmit and receive radio signals. They can also “sail” by tilting towards or away from the Sun. A current is run through a coil, turning the chip into a compass needle that aligns with Earth’s magnetic field, allowing the chipsat to control its orientation.

Because chipsats are small and cheap, they can be disposable sensors that could be sent on suicide missions to explore hostile environments, such as Saturn’s rings. Following the r-strategy employed by animals such as fish, they are designed to be released in large quantities from CubeSAT dispensers. While the survival rate of any one chip may be small, together there is a high likelihood they are able to transmit meaningful data. 

This project tackles the problem of consolidating data from a large swarm of chipsats, when not every chipsat can communicate directly to every other chipsat.

## Links

*  Full writeup: https://docs.google.com/document/d/1hzKnmu8YG_KFgRJf368QwCqYyr6BJ2YGy78ygURtYAs/edit
*  Presentation: https://docs.google.com/presentation/d/1eVsdA_jHy1klxJGCvtmRGSL1OXVipmdyBoozKms7gx4/edit
*  Hackathon details, objectives: https://chipsat-aukland.devpost.com/

Forked from: https://github.com/roboticexplorationlab/sprite.

## Running the demo

### Accessing the serial console
Nearly any terminal program can communicate with the sprite (baud=112500, data=8 bit, parity=None, flow control=XON/XOFF). For example...

#### MacOS
1. In terminal type: `ls /dev/tty.*`. The sprite will likely be listed as `/dev/tty.usbmodem_____`
2. Now enter: `screen /dev/tty.YOURBOARDNAMEHERE 115200`
3. You may or may not see a prompt, press <kbd>Ctrl</kbd>+<kbd>C</kbd> to halt the sprite
4. You can now enter the REPL by pressing any key, or hit <kbd>Ctrl</kbd>+<kbd>D</kbd> to reload the main.py
5. Exit screen at any time by pressing <kbd>Ctrl</kbd>+<kbd>A</kbd>+<kbd>\</kbd>

#### Windows 
1. Windows doesn't have a built-in terminal program like MacOS. Personally, I like [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html), or [termite](https://www.compuphase.com/software_termite.htm). You can also use the arduino serial monitor if you'd like!
2. For something like PuTTY, set the Connection Type to Serial
3. Press the <kbd>Windows Key</kbd> and type device manager (select it)
4. In device manager, scroll down to "Ports (COM & LPT)" and expand it
5. Plug in, then unplug the sprite and notice the impacted "COM" port.
6. Return to PuTTY and enter "COM___" in the "Serial Line" field, and then click "Open"

### Running

Put all the files located in [/software/](/software/) on to the sprite and start the serial console (as described above). After pressing <kbd>Ctrl</kbd>+<kbd>C</kbd> to halt the sprite, press any key to enter the REPL, then type

```
import NAMEOFFILE
```

and press enter to execute the example. For example, it we wanted to run blink.py, it would be...

```
import blink
```

1. master_node.py - Simulates a master node, which receives data and syncs the slave nodes. Run exactly one of these.
2. slave_node.py - Simulates a slave node, which transmits data to other slave nodes. Running many of these represents a swarm of chipsats.
