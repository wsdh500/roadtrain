"""
Configure available displays.
-----------------------------

Code to automatically setup the displays from the provided configuration.
"""

## DISPLAYS

#: The physical displays to use, indexed from 0 indicating display port.
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


## GEOMETRIES

#: Enable geometries ?
use_geometry = False


# Example of how to split a video in 3

video_width = 1920
video_height = 1080

third_width = video_width // 3
third_height = video_height // 3
two_third_width = third_width * 2
two_third_height = third_height * 2

geometry_0 = (third_width , two_third_height , 0 , third_height)
geometry_1 = (two_third_width , two_third_height , third_width , third_height)
geometry_2 = (video_width , two_third_height , two_third_width , third_height)


#: The pre-defined geometries.
geometries = [geometry_0,geometry_1,geometry_2]
