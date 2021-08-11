
# Demonstrate fullscreen multi-display video playback.
#
# for each display, playback a video contained in videos,
# wrapping round if there are fewer videos than displays.
# All videos replay at the same framerate, which *should* be known a priori.

from video import video_playback

dir = 'videos/test_patterns/double/'
videos = (dir+'double_display_0.mp4',
          dir+'double_display_1.mp4',
          dir+'inverted_double_display_0.mp4',
          dir+'inverted_double_display_1.mp4',)
fps = 30
fullscreen = True
video_playback(videos,fps,fullscreen)
