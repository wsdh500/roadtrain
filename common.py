"""
Configure available displays.
-----------------------------

Code to automatically setup the displays from the provided configuration.
"""

## DISPLAYS

#: The physical displays to use, indexed from 0 indicating leftmost-to-rightmost.
physical_displays = [0,1]
#: The playlist to use for the relative entry in physical_displays.
logical_displays = [0,1,2]
#: Enable fullscreen ?
fullscreen = True


## PLAYLISTS

videos_dir = '/usr/share/aaip/videos/test_patterns/'

playlist_0 = [videos_dir + 'triple_display_0.mp4',
              videos_dir + 'inverted_triple_display_0.mp4']
playlist_1 = [videos_dir + 'triple_display_1.mp4',
              videos_dir + 'inverted_triple_display_1.mp4']
playlist_2 = [videos_dir + 'triple_display_2.mp4',
              videos_dir + 'inverted_triple_display_2.mp4']
nplaylists = [playlist_0,playlist_1,playlist_2]
