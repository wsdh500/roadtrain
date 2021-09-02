"""
Code to automatically setup the displays from the provided configuration.
"""

## DISPLAYS

#: The physical displays to use, from leftmost-to-rightmost.
physical_displays = [0,1]
#: The playlist to use for the relative entry in physical_displays.
logical_displays = [0,1,2]
#: Enable fullscreen ?
fullscreen = True


## PLAYLISTS

videos_dir = 'roadtrain/test_patterns/'
videos_dir = '/home/sam/Videos/' + videos_dir

playlist_0 = [videos_dir + 'triple_display_0.mp4',
              videos_dir + 'inverted_triple_display_0.mp4']
playlist_1 = [videos_dir + 'triple_display_1.mp4',
              videos_dir + 'inverted_triple_display_1.mp4']
playlist_2 = [videos_dir + 'triple_display_2.mp4',
              videos_dir + 'inverted_triple_display_2.mp4']
nplaylists = [playlist_0,playlist_1,playlist_2]


## CODE

from display import n_displays , x_offset , y_offset , physical_width , physical_height

from VlcDisplay import VlcDisplay


def setup_displays():
    '''
    Automatically setup, and configure, each VlcDisplay.

    :return: list of VlcDisplay objects.
    '''
    players = []

    n = n_displays()
    j = min(n,len(physical_displays))
    for i in range(j):
        k = physical_displays[i]
        playlist = nplaylists[logical_displays[k]]
        k %= n
        name = 'Display-'+str(k)
        width = physical_width(k)
        height = physical_height(k)
        xoffset = x_offset(k)
        yoffset = y_offset(k)
        player = VlcDisplay(name,width,height,xoffset,yoffset,fullscreen)
        players.append(player)
        player.set_playlist(playlist)

    return players
