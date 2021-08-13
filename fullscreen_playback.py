
# Demonstrate fullscreen multi-display video playback.
#
# for each display, playback a video contained in videos,
# wrapping round if there are fewer videos than displays.
# All videos replay at the same framerate, which *should* be known a priori.

from video import video_playback , get_switcher
import RPi.GPIO as gpio

dir = 'videos/test_patterns/double/'
videos = (dir+'double_display_0.mp4',
          dir+'double_display_1.mp4',
          dir+'inverted_double_display_0.mp4',
          dir+'inverted_double_display_1.mp4',)
fps = 30
fullscreen = True

switcher = get_switcher()

pink_pin=15
yelo_pin=16
pins=[pink_pin,yelo_pin]

def callback(pin):
    if pin == pink_pin:
        switcher()
    elif pin == yelo_pin:
        pass

gpio.setwarnings(True)
gpio.setmode(gpio.BOARD)
for pin in pins:
        gpio.setup(pin,gpio.IN,pull_up_down=gpio.PUD_DOWN)
        gpio.add_event_detect(pin,gpio.FALLING,callback=callback)
try:
    video_playback(videos,fps,fullscreen)

finally:
    gpio.cleanup()
