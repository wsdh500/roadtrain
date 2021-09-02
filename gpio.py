
"""
Configure, setup, and teardown, of GPIO.
----------------------------------------
"""

import RPi.GPIO as gpio


pink_pin=15
yelo_pin=16
#: list containing all connected board input pins.
pins=[pink_pin,yelo_pin]


def init_gpio(callback_functions):
    '''
    :param callback_functions: a list containing all callback functions, one for each pin.

    - Sets GPIO warnings to True
    - Sets GPIO mode to BOARD
    - For each pin in pins, sets pin as an input that pulls low, and calls the given callback function on the falling edge.

    '''
    gpio.setwarnings(True)
    gpio.setmode(gpio.BOARD)
    functions = iter(callback_functions)
    for pin in pins:
        gpio.setup(pin,gpio.IN,pull_up_down=gpio.PUD_DOWN)
        callback_function = next(functions)
        gpio.add_event_detect(pin,gpio.FALLING,callback=callback_function)

def stop_gpio():
    '''
    Cleanup and shutdown all GPIO.
    '''
    gpio.cleanup()
