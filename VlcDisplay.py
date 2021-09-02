


import vlc
from Xlib import X, display
import time
from os.path import exists

class VlcDisplay:
    '''
    :param name: The name of the window.
    :param width: The width of the window to create.
    :param height: The height of the window to create.
    :param x_offset: The displacement of the window on the x-axis.
    :param y_offset: The displacement of the window on the y-axis.
    :param fullscreen: Whether to make this window fullscreen.

    VlcDisplay class is responsible for :

    * creating a VLC player instance,
    * creating a window for that instance,
    * moving the window to the correct offset for the correct display,
    * making the window fullscreen, if required.
    '''

    def __init__(self,name,width,height,x_offset,y_offset,fullscreen):
        '''
        Create a new instance of Class,
        create the player, it's associated window,
        and display.
        '''
        self.name = name

        # VLC
        self.instance = vlc.Instance()

        self.media_player = self.instance.media_player_new()
        self.player = self.instance.media_list_player_new()
        self.player.set_media_player(self.media_player)
        self.player.set_playback_mode(vlc.PlaybackMode.loop)

        # X11
        self.display = display.Display()
        self.screen = self.display.screen()
        self.root = self.screen.root
        self.window = self.root.create_window(0 , 0 , width , height ,
                                              0 , self.screen.root_depth ,
                                              background_pixel = self.screen.black_pixel ,
                                              event_mask = X.ExposureMask|X.KeyPressMask,)
        self.window.create_gc(foreground = self.screen.white_pixel,background = self.screen.black_pixel,)
        self.window.set_wm_name(name)
        self.window.map()
        self.media_player.set_xwindow(self.window.id)
        self.media_player.set_fullscreen(fullscreen)
        self.window.configure(x = x_offset , y = y_offset ,
                              width=width , height = height ,
                              border_width=0 , stack_mode=X.Above)
        self.root.warp_pointer(width,height)
        self.display.sync()

    def set_mrl(self,mrl):
        '''
        :param mrl: The MRL of the media for the player to play.
        '''
        self.player.set_mrl(mrl)

    def set_playlist(self,playlist):
        '''
        :param playlist: List containing the MRLs of the media for the player to play.
        '''
        self.media_list = self.instance.media_list_new()
        self.local_files = True
        for url in playlist:
            self.local_files &= exists(url)
            media = self.instance.media_new(url)
            media.parse()
            self.media_list.add_media(media)
        self.player.set_media_list(self.media_list)
        self.last_switched = 0

    def play_next(self):
        '''
        Play the next item in the playlist.
        '''
        current_time = time.time()
        if current_time - self.last_switched < 3:
            return
        else:
            self.last_switched = current_time
        size = self.media_list.count()
        if size > 1:

            # it's not possible to get the position of a stream.
            if self.local_files:
                playback_position = self.media_player.get_position()

            status = self.player.next()

            # it's not possible to get the position of a stream.
            if self.local_files:
                self.media_player.set_position(playback_position)

            # superfluous
            self.player.play()

    def play(self):
        '''
        Play the media.

        :return: boolean indicating whether the media wasn't playing.
        '''
        playing = False
        if not self.player.is_playing():
            self.player.play()
            playing = True
        else:
            print(self.name,'already playing.')
        return playing

    def stop(self):
        '''
        Stop the media.

        :return: boolean indicating whether the media was playing.
        '''
        stopping = False
        if self.player.is_playing():
            self.player.stop()
            stopping = True
        return stopping

    def is_playing(self):
        '''
        :return: boolean indicating whether the media is playing.
        '''
        position = self.media_player.get_position()
        # should check for loop
        return 0 <= position and position < 0.999

    def release(self):
        '''
        Essential cleanup, object cannot be used afterwards.
        '''
        if self.player != None and self.window != None:
            if self.player.is_playing():
                print('Stopping',self.name)
                self.player.stop()
            print('Releasing',self.name)
            self.player.release()
            self.player = None
            self.window = None
