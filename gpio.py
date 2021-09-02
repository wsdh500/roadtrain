
import RPi.GPIO as gpio


pink_pin=15
yelo_pin=16
pins=[pink_pin,yelo_pin]


def init_gpio(callback_functions):
    gpio.setwarnings(True)
    gpio.setmode(gpio.BOARD)
    functions = iter(callback_functions)
    for pin in pins:
        gpio.setup(pin,gpio.IN,pull_up_down=gpio.PUD_DOWN)
        callback_function = next(functions)
        gpio.add_event_detect(pin,gpio.FALLING,callback=callback_function)

def stop_gpio():
    gpio.cleanup()
