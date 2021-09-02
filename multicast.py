"""
Defaults, constants, and functionality, for multicasting.
---------------------------------------------------------------
"""

import socket
import struct

#: The port used by the multicast group.
multicast_port = 0xf00d
#: The address used by the multicast group.
multicast_addr = '224.223.222.221'
#: The tuple of the multicast address and port.
multicast_group = (multicast_addr,multicast_port)


#: The length of byte array to be used in all communications.
padding = 16

#: The encoding to be used when communicating.
encoding = 'utf-8'

def prepare(i):
    '''
    :param i: a value

    Stringify, pad and encode the value, i, for communication.

    :return: a prepared byte array.
    ''' 
    return str(i).ljust(padding).encode(encoding)

#: Command used in all communications to request application shutdown. 
quit_command = prepare('quit')
#: Command used in all communications as acknowledgement.
ack_command = prepare('ack')

#: Command used in all communications to request playback to commence.
play_command = prepare('play')
#: Command used in all communications to request playback to cease.
stop_command = prepare('stop')

#: Command used in all communications to request the next playlist media.
next_command = prepare('next')

#: Command used in all communications to request the toggling the depth stream.
depth_command = prepare('depth')

def setup_target():
    """
    Setup instance as a multicast target.

    :return: a socket to send and receive communications by.
    """
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind(('',multicast_port))
    multicast = socket.inet_aton(multicast_addr)
    mreq = struct.pack('4sL',multicast,socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,mreq)
    return sock

def setup_source():
    '''
    Setup instance as a multicast source.

    :return: a socket to send and receive communications by.

    .. warning:: There wants to be only one source on the local network.
    '''
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.settimeout(0.2)
    ttl = struct.pack('b',1)
    sock.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,ttl)
    return sock

def send_message(sock,message,address):
    '''
    :param sock: the socket to send the communcation by
    :param message: the message to send
    :param address: the address to send the message to

    Send a given message, to a given address, via a given socket.

    .. note:: Ensures all bytes are sent.
    '''
    try:
        sent = 0
        while sent < padding:
            sent += sock.sendto(message,address)
            message = message[sent:]
    except socket.timeout:
        pass

