
##   code for obtaining the display geometry from shell and library calls
##   in theory, there can be all sorts of weird and wonderful setups
##   no point worrying about them unless they crop up

# for running shell commands and parsing the results
import re
from subprocess import run, PIPE

# for the library call
from Xlib.display import Display

# groups : logical_width , logical_height
logical_pattern = r'current (\d+) x (\d+)'

# groups : id , width , height , offset_x , offset_y
display_pattern = r'HDMI-(\d) connected\s?\w* (\d+)x(\d+)\+(\d+)\+(\d+)'

output = run(['xrandr'],stdout=PIPE).stdout.decode()

## logical display information
logical_result = re.search(logical_pattern,output)
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
displays = [(x.width_in_pixels,x.height_in_pixels)
           for x in Display().display.info.roots]

# check for mismatches
if len(displays) == 1:
    display = displays[0]
    if display[0] != int(logic_width):
        print("WARNING : XLib width does not match logical display width.")
    if display[1] != int(logic_height):
        print("WARNING : XLib height does not match logical display height.")
#else : ??

def n_displays():
    return len(display_result)

def physical_width(i):
    '''Get width of display i'''
    return int(display_result[i][1])

def physical_height(i):
    '''Get height of display i'''
    return int(display_result[i][2])

def x_offset(i):
    '''Get x-offset of display i'''
    return int(display_result[i][3])

def y_offset(i):
    '''Get yoffset of display i'''
    return int(display_result[i][4])

def logical_width():
    '''Get logical width'''
    return int(logic_width)

def logical_height():
    '''Get logical height'''
    return int(logic_height)

# print out disgnostics regardless ...
for i in range(n_displays()):
    print('HDMI',i,':',physical_width(i),'x',physical_height(i),'+',x_offset(i),'+',y_offset(i))
print('Logical display :',logical_width(),'x',logical_height())
