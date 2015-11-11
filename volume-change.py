#!/usr/bin/python3
# By: Garrett Holbrook
# Date: August 27th, 2015
#
# Usage: Changes the system volume through amixer and then 
#        makes a dbus method call to the gnome shell to get the
#        gnome volume OSD (On Screen Display)
#
# Requires: python3 and python-dbus (on Arch) or python3-dbus
#           (on Debian) or equivalent
import dbus
import sys
from subprocess import getoutput

# Getting the dbus interface to communicate with gnome's OSD
session_bus = dbus.SessionBus()
proxy = session_bus.get_object('org.gnome.Shell', '/org/gnome/Shell')
interface = dbus.Interface(proxy, 'org.gnome.Shell')

# Interpreting how to affect the volume and by what percentage and
# then creating a bash command that will reduce the stdout to the
# new percentage volume. Vol = volume
vol_action = sys.argv[1]
vol_percent_change = sys.argv[2]

command = 'amixer -D pulse sset Master ' + vol_percent_change + '%'

if vol_action == 'increase':
    command += '+ > /dev/null && amixer -D pulse set Master unmute'
else:
    command += '-'

command += ' | grep -oP "\[\d*%\]" | head -n 1 | sed s:[][%]::g'

current_vol_percentage = int(getoutput(command))
# If it's 0 then add mute flag (tigger sub-action, keyboard ligth for example)
if current_vol_percentage == 0:
	getoutput('amixer -D pulse set Master mute');

# Determining which logo to use based off of the percentage
logo = 'audio-volume-'
if current_vol_percentage == 0:
	logo += 'muted'
elif current_vol_percentage < 30:
    logo += 'low'
elif current_vol_percentage < 70:
    logo += 'medium'
else:
    logo += 'high'
logo += '-symbolic'

# Make the dbus method call
interface.ShowOSD({"icon":logo, "level":current_vol_percentage})

