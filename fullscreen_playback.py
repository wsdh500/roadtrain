
# Demonstrate fullscreen multi-display video playback.
#
# for each display, playback a video contained in videos,
# wrapping round if there are fewer videos than displays.
# All videos replay at the same framerate, which *should* be known a priori.

from video import video_playback

videos = ('munching-squares_1920x1080.mp4',)
fps = 30
fullscreen = True
video_playback(videos,fps,fullscreen)
