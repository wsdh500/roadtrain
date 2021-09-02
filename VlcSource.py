
"""
The source takes commands as arguments and sends them to the targets.

In practice, it establishes the multicast channel
over which it sends, and relays, messages.

When executed from a shell, this file functions as a basic "shell"
 for the source.

Could be improved by accepting piped commands on STDIN so it can be scripted.
"""

import socket

from multicast import multicast_group , setup_source , send_message
from multicast import padding , prepare , encoding
from multicast import quit_command , play_command , stop_command
from multicast import ack_command , depth_command , next_command

import threading
import time
import sys


class VlcSource:
    '''
    Source for Vlc*Target multicast instances.
    '''

    def __init__(self):
        # SETUP MULTICAST SOURCE
        print('Setting up source ...')
        self.socket = setup_source()

        def runner(self):
            self.addresses = {}
            self.running = True
            try:
                while self.running:
                    try:
                        data , address = self.socket.recvfrom(padding)
                        if data != None:
                            if data == quit_command:
                                print('Received quit signal from',address)
                                self.running = False
                            elif data == depth_command:
                                send_message(self.socket,depth_command,multicast_group)
                            elif data == next_command:
                                send_message(self.socket,next_command,multicast_group)
                            elif data == ack_command:
                                self.addresses[address] = time.time()
                    except socket.timeout:
                        pass

            finally:
                print('Shutting down.')
                for i in range(100):
                    send_message(self.socket,quit_command,multicast_group)
                self.socket.close()
                print('Closed socket.')

        self.thread = threading.Thread(target=runner,args=(self,))
        self.thread.start()

    def send_message(self,message):
        '''
        :param message: The message to send to the multicast group.

        '''
        send_message(self.socket,message,multicast_group)


if __name__ == "__main__":

    def handle_depth(source):
        '''
        :param source: The VlcSource instance.

        Handles depth camera events.
        Sends the "depth" message.
        '''
        print('toggling depth camera visibility ...')
        source.send_message(depth_command)

    def handle_next(source):
        '''
        :param source: The VlcSource instance.

        Handles playlist events.
        Sends a number of "ack" messages followed by the "next" message.
        '''
        print('requesting the next playlist item ....')
        for i in range(10):
            source.send_message(ack_command)
        source.send_message(next_command)

    def handle_quit(source):
        '''
        :param source: The VlcSource instance.

        Handles quit events.
        Sends the "quit" message.
        '''
        print('requesting shutdown ...')
        source.send_message(quit_command)
        source.running = False

    def handle_play(source):
        '''
        :param source: The VlcSource instance.

        Handles play events.
        Sends a number of "ack" messages followed by the "play" message.
        '''
        print('requesting playback ...')
        for i in range(10):
            source.send_message(ack_command)
        source.send_message(play_command)

    def handle_stop(source):
        '''
        :param source: The VlcSource instance.

        Handles stop events.
        Sends the "stop" message.
        '''
        print('requesting all stop ...')
        source.send_message(stop_command)

    def handle_ack(source):
        '''
        :param source: The VlcSource instance.

        Handles acknowledgement events.
        Sends the "ack" message, waits one second, and displays the acknowledging IP addresses.
        '''
        source.addresses = {}
        source.send_message(ack_command)
        time.sleep(1)
        for address in source.addresses.keys():
            print(address[0])

    help_command = prepare('help')
    commands = (ack_command.decode( encoding),
                depth_command.decode(encoding),
                play_command.decode(encoding),
                next_command.decode(encoding),
                stop_command.decode(encoding),
                quit_command.decode(encoding),
                help_command.decode(encoding))

    print("Type 'help' for available commands.")
    try:
        source = VlcSource()
        while source.running:
            command = input('>> ')
            command = command.strip()
            command = prepare(command)
            if command == '':
                next
            elif command == depth_command:
                handle_depth(source)
            elif command == next_command:
                handle_next(source)
            elif command == quit_command:
                handle_quit(source)
            elif command == play_command:
                handle_play(source)
            elif command == stop_command:
                handle_stop(source)
            elif command == ack_command:
                handle_ack(source)
            elif command == help_command:
                print('Available commands :')
                for command in commands:
                    print('\t',command)
    finally:
        print('exiting ...')
        source.running = False
        sys.exit()
