# gnome-volume-step-osd
------------------------
A workaround script that allows you to change the system volume by a desired step size while still triggering GNOME's volume notification OSD (On Screen Display)

Requirements
------------
The script is built using Python3 and has a the following requirements
*    `python3`
*    `python3-dbus` (or equivalent)

The package with the correct version is listed as python-dbus in the Arch repositories and python3-dbus in the Debian and Fedora repositories

This was also written and tested to be working on GNOME 3.16 with gnome-shell installed. I'm unsure if it will work on other versions of GNOME (although I don't see why it shouldn't) so your mileage may vary.

How to Use
------------------
Just download the script and make sure it is executable with 
   ```chmod +x volume-change.py```
The script takes in two arguments:
* [string arg1] increase or decrease
* [int arg2] percentage change

an example for running this script might look like 

    python3 volume-change.py increase 2

This would increase the volume by 2 percent

You can then create a custom keyboard shortcut setting the command to either of these commands

    python3 [SCRIPT_DIRECTORY]/volume-change.py [arg1] [arg2]
    ./[SCRIPT_DIRECTORY]/volume-change.py [arg1] [arg2]

Because this script will run every time you press the volume up or down keys, you may want to run a compiled version. You can compile the script with basic optimizations with
    
    python3 -O -m py_compile volume-change.py

and then your command would be

    python3 [SCRIPT_DIRECTORY]/__pycache__/volume-change.cpython-[PYTHON_VERSION].pyo [arg1] [arg2]

Motivation and Explanation
--------------------------
The motivation behind this is that each time you change the volume in GNOME 3, the volume changes by a set percentage (6% in GNOME 3.16). That percentage is literally hardcoded into the C code of the gnome-settings-daemon and is therefore not configurable. For me, 6% was too much of a step, and I would continue to bounce back and forward between too loud and too quiet of a volume. 

The way to work around this is to create a custom keyboard shortcut for your volume keys to run a command that will manually adjust the volume the desired amount. This is what I do in my script, using the command `amixer -D pulse sset Master %[percentage][+-]`. If this does not adjust your volume, you'll have to replace the command with one that works for you.

The problem with this approach is that it no longer triggers the nice volume notification OSD like the default volume control buttons do. You don't get a notification or indication of what the current volume is. A solution to this is to create your own notifications with the current percentage. However, I wanted my solution to work seemlessly with the system, and I didn't want to have to replace GNOME's built-in volume OSD with my own just because I was manually setting the volume. 

It's much easier to just use your own custom notification by using notify-send. However, in order to get GNOME's volume OSD to show up as instead of my own, less-appealing version of a volume notification, I make a dbus ShowOSD() method call to org.gnome.Shell with the proper icon and level values.

As a side note, the bash commands (amixer...) are what I use to adjust my volume and then reduce the stdout from that command to just the volume percentage level. You may need to alter the script slightly to fit your system.
