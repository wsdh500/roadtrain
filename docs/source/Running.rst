
*****************
Running a session
*****************

Once you have installed and configured the project to suit your tastes
you will want to run a session.

The project connects over the local network using multicasting to communicate.
The terminology used is of ``sources`` and ``targets``.
Sources are used to coordinate playback, targets perform the actual playback
on each display via their connected devices.

.. note::
   This project was designed to be used as an enclosed display kisok.
   Network overheads, which are not negligible, cause problems for sync'ing
   displays. As a result it is best to connect devices via ethernet
   rather than over WiFi.

.. warning::
   There is no implicit security in the project.
   As such, you will want to isolate the devices you will be using,
   that is to say, you will want only allow those devices
   and any other trusted devices onto the network.

   DO NOT USE THIS PROJECT ON A PUBLIC NETWORK.

For each device that will be driving the displays you need to run ``VlcTarget``.
This will setup the devices ready for playback, GPIO,
and potentially a connected depth camera.

Playback will not start immediately.
In order to coordinate playback you will need to run ``VlcSource``.
This can be done on one of the display devices,
but can also be run on a separate machine on the network.
``VlcSource`` provides a simple shell-like interface.
Available commands are listed at run-up.
A typical session goes something like this :

Type ``ack`` to get a list of targets on the network.

Type ``play`` in order to start playback on the targets.

If the videos are not in sync, type ``stop`` and then ``play`` again.
Usually this works first time, but may take a couple of attempts until
playback is sync'ed well enough.

You can optionally type ``depth`` in order to run-up the depth camera
on whichever device it is connected to.

You can optionally type ``next`` to switch to the next item in the playlist.

Finally, if you type ``quit`` all the targets will shut-down.

Unfortunately, there is no command to exit the source without quitting.
This would be a usefull command for future expansion.

When running a pre-installed image, targets can be set up to run-up as
a service. See the documentation on Pre-configured Images under
`Installation <./Installation.html>`_.
