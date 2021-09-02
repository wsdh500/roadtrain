
"""
Obtain the display geometry from shell, and library, calls.
-----------------------------------------------------------

In theory, there can be all sorts of weird and wonderful X11 setups,
no sense worrying about them unless they crop up in practice.

see: `xrandr(1) <https://www.x.org/releases/X11R7.5/doc/man/man1/xrandr.1.html>`_
"""

# for running shell commands and parsing the results
import re
from subprocess import run, PIPE

# for the library call
from Xlib.display import Display

# for handling potential errors
from Xlib.error import DisplayNameError

# Collects the groups : logical_width , logical_height
logical_pattern = r'current (\d+) x (\d+)'

# Collects the groups : id , width , height , offset_x , offset_y
display_pattern = r'HDMI-(\d) connected\s?\w* (\d+)x(\d+)\+(\d+)\+(\d+)'

output = run(['xrandr'],stdout=PIPE).stdout.decode()

## logical display information
logical_result = re.search(logical_pattern,output)
logic_width = '0'
logic_height = '0'
if logical_result != None:
    logic_width , logic_height = logical_result.groups()

## physical display information
display_result = re.findall(display_pattern,output)

# check for mismatches
total_width = 0
total_height = 0
for i in display_result:
    # width + x-offset
    tmp = int(i[1]) + int(i[3])
    if tmp > total_width:
        total_width = tmp
    # height + y-offset
    tmp = int(i[2]) + int(i[4])
    if tmp > total_height:
        total_height = tmp
# "in theory, there can be all sorts of weird and wonderful setups .."
if total_width != int(logic_width):
    print("WARNING : Total display width does not match logical width.")
if total_height != int(logic_height):
    print("WARNING : Total display height does not match logical height.")

## XLib logical display information
displays = []
try:
    displays = [(x.width_in_pixels,x.height_in_pixels)
                for x in Display().display.info.roots]
except DisplayNameError:
    pass

# check for mismatches
if len(displays) == 1:
    display = displays[0]
    if display[0] != int(logic_width):
        print("WARNING : XLib width does not match logical display width.")
    if display[1] != int(logic_height):
        print("WARNING : XLib height does not match logical display height.")
#else : ??

def n_displays():
    '''
    :return: number of available displays.
    '''
    return len(display_result)

def physical_width(i):
    '''
    :param i: index of display, zero-based.
    :return: width, in pixels, of display, i.
    '''
    return int(display_result[i][1])

def physical_height(i):
    '''
    :param i: index of display, zero-based.
    :return: height, in pixels, of display, i.
    '''
    return int(display_result[i][2])

def x_offset(i):
    '''
    :param i: index of display, zero-based.
    :return: x-offset, in pixels, of display i.
    '''
    return int(display_result[i][3])

def y_offset(i):
    '''
    :param i: index of display, zero-based.
    :return: y-offset, in pixels, of display i.
    '''
    return int(display_result[i][4])

def logical_width():
    '''
    :return: logical width, in pixels, of the combined displays.
    '''
    return int(logic_width)

def logical_height():
    '''
    :return: logical height, in pixels, of the combined displays.
    '''
    return int(logic_height)

# print out disgnostics regardless ...
for i in range(n_displays()):
    print('HDMI',i,':',physical_width(i),'x',physical_height(i),'+',x_offset(i),'+',y_offset(i))
print('Logical display :',logical_width(),'x',logical_height())
