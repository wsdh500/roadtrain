
"""
Multicast target.
-----------------

Runs as a script on any target device attached to one or more displays.
Playback is controlled by the multicast source, *VlcSource*.

* Runs the *VlcDisplay* code as configured,
* sets up as a multicast target, accepting requests from the multicast source,
* accepts input via GPIO which controls the depth camera window and playlist position.

"""

import sys

from gpio import init_gpio , stop_gpio

import depth

from multicast import setup_target , send_message , padding
from multicast import quit_command , play_command , stop_command
from multicast import ack_command , depth_command , next_command

from common import setup_displays


if __name__ == "__main__":

    ## DEPTH
    start_depth_cam , stop_depth_cam = depth.create_event_handlers(depth.rs_args)


    ## DISPLAYS
    players = setup_displays()


    ## MULTICAST
    sock = setup_target()

    address = None


    ## GPIO
    def toggle_depthcam(pin):
        '''
        :param pin: GPIO pin the signal was recived on.
        Callback function which toggles the depth camera visibility
        by sending a message back to the multicast source.
        '''
        global address
        global sock
        if address != None and sock != None:
            send_message(sock,depth_command,address)

    def request_next(pin):
        '''
        :param pin: GPIO pin the signal was recived on.
        Callback function which requests the next item in the playlist
        by sending a message back to the multicast source.
        '''
        global address
        global sock
        if address != None and sock != None:
            send_message(sock,next_command,address)

    init_gpio([toggle_depthcam,request_next])


    ## MAIN LOOP

    HALTING = 0
    RUNNING = 1
    PLAYING = 2
    STATUS = RUNNING
    try:
        while STATUS in [RUNNING,PLAYING]:
            data , address = sock.recvfrom(padding)
            if data == quit_command:
                print('Quitting.')
                STATUS = HALTING
                send_message(sock,ack_command,address)
            elif data == depth_command:
                print('Received "depth" request')
                start_depth_cam()
                stop_depth_cam()
                send_message(sock,ack_command,address)
            elif data == play_command:
                print('Received "Play" request')
                ok = True
                for player in players:
                    if not player.is_playing():
                        ok &= player.play()
                if not ok:
                    print('Not OK.','Shutting down.')
                    STATUS = HALTING
                else:
                    STATUS = PLAYING
                send_message(sock,ack_command,address)
            elif data == next_command:
                print('Received "Next" request')
                for player in players:
                    player.play_next()
                send_message(sock,ack_command,address)
            elif data == stop_command:
                print('Answering "All Stop".')
                for player in players:
                    player.stop()
                send_message(sock,ack_command,address)
            elif data == ack_command:
                send_message(sock,ack_command,address)

    finally:
        print('Shutting down.')
        if address != None:
            send_message(sock,quit_command,address)
        sock.close()
        for player in players:
            player.release()
        players = []
        stop_depth_cam()
        stop_gpio()

        print('Exit.')
        sys.exit()
