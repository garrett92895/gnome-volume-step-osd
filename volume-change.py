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
from subprocess import getoutput, call

# Getting the dbus interface to communicate with gnome's OSD
session_bus = dbus.SessionBus()
proxy = session_bus.get_object('org.gnome.Shell', '/org/gnome/Shell')
interface = dbus.Interface(proxy, 'org.gnome.Shell')

# Interpreting how to affect the volume and by what percentage and
# then creating a bash command that will reduce the stdout to the
# new percentage volume. Vol = volume
vol_action = sys.argv[1]
vol_percent_change = int(sys.argv[2])

# Get the volumes for all the channels
comm_get_volume='amixer -D pulse get Master | grep -oP "\[\d*%\]" | sed s:[][%]::g'
vol_percentages=list(map(int, getoutput(comm_get_volume).split()))

# Average them into a single value (note the +0.5 for rounding errors)
vol_percentage=int(sum(vol_percentages)/len(vol_percentages)+0.5)

# Add/subtract the value of volume (handle negative values)
increase = (vol_action == 'increase')
if (increase):
    vol_percentage=max(0, (vol_percentage + vol_percent_change))
else:
    vol_percentage=max(0, (vol_percentage - vol_percent_change))

# Set the volume for both channels
command = 'amixer -D pulse sset Master ' + str(vol_percentage) + '% > /dev/null'

if (increase):
    command += ' && amixer -D pulse set Master unmute > /dev/null'

# Apply volume
call(command, shell=True)

# If it's 0 then add mute flag (trigger sub-action, keyboard light for example)
if vol_percentage == 0:
	call('amixer -D pulse set Master mute', shell=True);

# Determining which logo to use based off of the percentage
logo = 'audio-volume-'
if vol_percentage == 0:
	logo += 'muted'
elif vol_percentage < 30:
    logo += 'low'
elif vol_percentage < 70:
    logo += 'medium'
else:
    logo += 'high'
logo += '-symbolic'

# Make the dbus method call
interface.ShowOSD({"icon":logo, "level":vol_percentage/100})
