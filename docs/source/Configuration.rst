
*************
Configuration
*************

The majority of configuration for the project is done through ``common.py`` which configures which displays are used and what is to be displayed on them.
The exceptions are GPIO, the RealSense depth camera, and multicasting which are configured in ``gpio.py``, ``depth.py``, and ``multicast.py`` respectively.

Displays
--------

Within ``common.py`` there are a number of variables that control the displays.
If you are using a mulitple Pi setup then each Pi may want different configurations.
It may be as well to create multiple branches in Git for each Pi.

Physical Displays
^^^^^^^^^^^^^^^^^

The ``physical_displays`` variable configures which displays are active, for example

``physical_displays = [0,1]``

The values ``0`` and ``1`` refer to the HDMI IDs of the displays.
As both ``0`` and ``1`` appear in the list, they will both be active.

``physical_displays = [0]``

As only display ``0`` is in the list, only that display will be active.

``physical_displays = [1]``

As only display ``1`` is in the list, only that display will be active.

``physical_displays = [1,0]``

In this configuration both displays will be active though the contents of the displays will be switched.

nb. if using the depth camera, it is advised to only use a single display on that Pi.
It is recommended that, if using local files and not streams, to use an equal number of displays for each Pi in the setup.


Logical Displays and Playlists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``logical_displays`` variable configures what will be displayed on the relative displays.
This is directly related to the contents of the playlists.
The playlists are found in the variable, ``nplaylists``, and it is this list that the logical displays refers to.
For example,

``physical_displays = [0,1]``

``logical_displays = [0,1,2]``

In this configuration, both displays are active, display ``0`` in ``physical_displays`` will use playlist ``0``, and display ``1`` will use playlist ``1``.

``physical_displays = [1,0]``

``logical_displays = [0,1,2]``

In this configuration, both displays are active, display ``0`` in ``physical_displays`` will use playlist ``1``, and display ``1`` will use playlist ``0``.

nb. The number of items in the ``logical_displays`` list must be greater or equal to the number of items in the ``physical_displays`` list.

The variable, ``nplaylists`` is a list of lists. Each item in the list is a playlist made up of strings which are the absolute paths of the video files,
or the URLs of any streams being used. It is best not to mix local files and streams if switching playlist items should maintain position.

Fullscreen
^^^^^^^^^^

There is a ``fullscreen`` variable, which is a boolean indicating whether to use the whole of each display for playback.
This is generally set to ``True`` for normal use, however it may be changed to ``False`` to aid debugging. 


Geometries
^^^^^^^^^^

The display geometries can be configured in order to play a cropped region of the video during playback.
This is primarily aimed at single stream use where the same URL is used for all display playlists.
If the aspect ratio of the cropped geometry matches the aspect ratio of the display, the playback will be scaled to fill the display.

To enable geometries, set the ``use_geometry`` variable to ``True``.
If multiple streams, or multiple video files are being used, it may be as well to leave this variable as ``False``.

The geomteries are read from a list of lists called ``geometries``.
Each geometry is a list containing four variables : width, height, x-offset, and y-offset.
The width and height specify the width and height of the total cropped area,
and the x- and y-offsets offset into the cropped area.

For example, if we imagine a 2x2 unit video, if we wanted the left half of the video then the width would be 1, the height would be 2, and both offsets would be 0;
however if we wanted the right half of the video, width and height would be 2, and the x-offset would be 1 and the y-offset would be 0.
If we wanted a only of the top right corner of the video, width would be 2, height would be 1, x-offset would be 1, and y-offset would be 0;
however if we wanted the bottom right corner of the video, width and height would be 2, and x- and y-offsets would both be 1.

Here follows an example of how to split a 1920x1080 video into three pieces which display the total width and the middle third of the height of the video :

We need to create some variables in order to have Python do the arithmetic calculations for us.

The video is 1920x1080, so we'll specify them as variables :

``video_width = 1920``

``video_height = 1080``

We want to chop the width in three, one third for each display :

``third_width = video_width // 3``

We want to chop the height in three as we want to display the middle third, thus preserving the aspect ratio so it will scale to the full display :

``third_height = video_height // 3``

We want to calculate two thirds of the width as that will be the right-most edge of the second display and the left-most edge of the third display :

``two_third_width = third_width * 2``

As mentioned, we want to calculate two-thirds of the height as each display will have a third of the height as it's top edge two-thirds as it's bottom edge :

``two_third_height = third_height * 2``

We then define these geometries as lists, one for each display :

``geometry_0 = (third_width , two_third_height , 0 , third_height)``

``geometry_1 = (two_third_width , two_third_height , third_width , third_height)``

``geometry_2 = (video_width , two_third_height , two_third_width , third_height)``

Now we set the ``geometries`` variable to our newly created geometries :

``geometries = [geometry_0,geometry_1,geometry_2]``


GPIO
----

The pin numbers used for GPIO are stored in a list variable, ``pins``.
Pins are numbered using the BOARD numbering system, as opposed to the Broadcom GPIO numbering system, BCM.
GPIO is initialised with the ``init_gpio()`` function that takes a list of callback functions, one for each pin listed in ``pins``.
At shutdown the ``stop_gpio()`` function should be called to handle any cleanup that needs to take place.


Multicasting
------------

Configuration of the multicast group is found in ``multicast.py``.
For the most part this should be left as is, and only should be changed to prevent collisions with other multicast services such as real-time streaming of video.
The key values are :

``multicast_port = 0xf00d``

``multicast_addr = '224.223.222.221'``

``multicast_group = (multicast_addr,multicast_port)``


RealSense Depth Camera
----------------------

As with multicasting, configuration of the depth camera should be left in it's default state.
The key values are :

``warn_temp`` which is the temperature at which to warn about the projector, or the Asic, temperature,
and ``shutdown_temp`` which is the temperature at which to shutdown the RealSense camera.

You may also wish to change the name of the depth camera window, ``rs_window``,
and the default colour map, ``default_map`` though the latter is overriden as an argument to the functions that create the depth camera window,
``depth_stream``, and ``combined_stream``.
