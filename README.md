# AAIP Roadtrain Project
## Requirements
This codebase has the following dependecies :
- VLC
- python-vlc
- opencv-python
- python-rpi.gpio
- python3-rpi.gpio
- [Intel RealSense SDK 2.0](https://github.com/IntelRealSense/librealsense)

The following are recommended :
- libtbb-dev
- protobuf-compiler

Full instructions on how to create a Raspberry Pi 4 Model B installation from scratch
are available from the AAIP Roadtrain shared Google Drive.
A flashable disk image should be available for download shortly.

The model used for inter-device communication is multicasting.
The terminology adopted by this project, at this time, is of *sources* and *targets*.
Essentially, there is a single multicast source that sends requests to
a number of multicast targets that each drive one or more displays.

As a rule of thumb, each target device should have the same number of displays attached.
It is also advised that the devices be connected via ethernet to a dedicated router
or switch, though this is not essential it cuts down on network traffic that may impede
communication between devices. Control could be implemented purely via GPIO,
but this has not been implemented at this time.

Once you have downloaded this repository, installed the required dependencies,
and associated test pattern videos from the shared Google Drive,
run *VlcGpioTarget.py* on any target device that has a connected display
that you wish to use.
Control of playback is handled by running *VlcSource.py*.

Configuration for the different aspects of the system are located
near to their associated code.
To configure which displays are used, and what is played back on them, edit *common.py*.
It is best to give the absolute path of local video files.
The system will also support streamed playback, tested using *RTP*.
Streaming requires one stream for each video to be played back,
as a result your bandwidth may become too saturated for smooth playback.

The GPIO event handlers send out requests from the target to the source
which then relay that request as a boadcast to all targets.
Currently the system accepts two GPIO inputs on board pins 15 and 16.
One toggles display of the depth camera,
this will active a depth camera attached to any target device;
the other switches playback to the next item in the playlist.

Playback is done in-time rather than in-sync.
Great efforts have been expended to try and make sure displays remain in-time,
but it is possible that they can drift out-of-time as a result of changes to playback.
The main cause of such drifting is then VLC playback startup overhead.
Occasionally VLC playback freezes, it usually has a record of where about it is in playback,
so if it unfreezes it should still be in-time. YMMV.
There is a hack that can allow VLC to single step frame-by-frame and syncronise devices that
way, however it was discovered too late to be implemented at this time.

General support of the system can be obtained by emailing
[Sam Hart](mailto:wsdh500@york.ac.uk).
