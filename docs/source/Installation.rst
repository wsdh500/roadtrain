
************
Installation
************


These are installation notes for setting up a *Raspberry Pi 4 Model B* with 4GiB of RAM and a 32GB SD card
to run the **AAIP Roadtrain Project** code. Use with caution.

Lines starting with a ``$`` are shell commands of the user,
and lines starting with a ``#`` are shell commands of the super user
and can be prepended with sudo for sudoers.
Actions to perform are placed between *<>* as a reminder.

Pre-configured Images
---------------------

Operating System images that have been pre-installed, configured, and are ready for use
are available within *AAIP* from the shared Google Drive.
These can be flashed to an SD card using the instructions below.

Once the SD card has been flashed with the image, inserted in the Pi and booted,
you will need to change the hostname from *aaip-pi-x* to something more useful.

Edit ``/etc/hostname`` and ``/etc/hosts`` changing the name as appropriate.

You will also need to regenerate the OpenSSHd keys.

``# systemctl stop ssh``

``# rm /etc/ssh/ssh_host_*``

``# dpkg-reconfigure openssh-server``

``# systemctl start ssh``

To run the *roadtrain* software as a service, you will need to :

``# systemctl stop lightdm``

``# systemctl start roadtrain``

To enable the *roadtrain* service to start on system boot :

``# systemctl disable lightdm``

``# systemctl enable roadtrain``

``# shutdown -r now``

All files for the service are stored under ``/usr/share/aaip``.


Operating System Installation
-----------------------------


The development of the code was performed using *Ubuntu Mate*.
It may well be that *Raspbian* could be used instead, in which case skip ahead to code installation.

Download Ubuntu Mate 20.04 for the Raspberry Pi :
`https://ubuntu-mate.org/download/arm64/ <https://ubuntu-mate.org/download/arm64/>`_

Some useful information can be found here :
`https://ubuntu-mate.org/raspberry-pi/ <https://ubuntu-mate.org/raspberry-pi/>`_

If the Pi fails to boot, then check the the following trouble-shooting page :
`https://www.raspberrypi.org/forums/viewtopic.php?p=437084#p437084 <https://www.raspberrypi.org/forums/viewtopic.php?p=437084#p437084>`_


To flash the OS image to the SD card using Linux:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Insert the SD card and then check where it is attached using

``$ lsblk -p``
   
Then, once you’ve found the attached SD card, flash the image to the SD card using

``# dd if=<IMAGE> of=<DEVICE> conv=fsync ; sync ; sync``

Where ``<IMAGE>`` is the image, and ``<DEVICE>`` is the device NOT the partition.


To flash the OS image to the SD card using macOS:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Insert the SD card and then check where it is attached using

``$ diskutil list``

Then, once you’ve found the attached SD card, flash the image to the SD card using

``# dd if=<IMAGE> of=<DEVICE> conv=fsync ; sync ; sync``

Where ``<IMAGE>`` is the image, and ``<DEVICE>`` is the device NOT the partition.


To flash the OS image to the SD card using Windows:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To flash the image using Windows you will need an etcher such as
`balenaEtcher <https://www.balena.io/etcher/>`_, or
`Etcher <https://www.etcher.net/>`_.


Install, and configure to taste.


Code Installation
-----------------


Packages
^^^^^^^^

Update the package manager, and upgrade the installed packages and distribution

``# apt update``

``# apt -y full-upgrade``

``# apt -y autoremove``

``# apt -y dist-upgrade``

… it’s also a good idea to be able to log in remotely ...

``# apt install openssh-server``

… clone *git* repositories …

``# apt install git``

… and install *Python* modules …

``# apt install python3-pip``


Video Playback
^^^^^^^^^^^^^^

In order to play back video, you’ll need to install the *VLC* bindings

``# apt install vlc``

``$ pip install python-vlc``


RealSense SDK installation
^^^^^^^^^^^^^^^^^^^^^^^^^^

There appears to be no official SDK package for *Arm* architectures like the *Pi*,
the recommended path is to compile it from source.

The following appear to be the required libraries.

``# apt install pkg-config at``

``# apt install libssl-dev libusb-1.0-0-dev``

``# apt install libgtk-3-dev xorg-dev``

``# apt install libglfw3-dev libglu1-mesa``

``# apt install libgl1-mesa-dev libglu1-mesa-dev``

``# apt install mesa-utils mesa-utils-extra``

``# apt install glslang-dev glslang-tools``

``# apt install cmake``

In order to  display the depth camera, you’ll need to install the *OpenCV* bindings

``$ pip install opencv-python``

Installing the *OpenCV* bindings should also install *Numpy*.

Installing *Threaded Building Blocks* is recommended for performance, YMMV

``# apt install libtbb-dev``

Installing *Protobuf* is recommended for performance, YMMV

``# apt install protobuf-compiler``

If using *Bash*, update the environment variables in .bashrc (other shells are available …)

``$ echo export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp >> ~/.bashrc``

``$ echo export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=3 >> ~/.bashrc``

``$ source ~/.bashrc``

Update the dynamic library bindings

``$ echo export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH >> ~/.bashrc``

``$ source ~/.bashrc``

``# ldconfig``

Clone the SDK repository

``$ git clone https://github.com/IntelRealSense/librealsense.git``

Update the udev rules for the camera

``$ cd librealsense``

*< unplug the depth camera ! >*

``$ ./scripts/setup_udev_rules.sh``

*< plug the camera back in >*

Finally, build the SDK

``$ mkdir build``

``$ cd build``

``$ cmake ../ -DBUILD_EXAMPLES=true -DBUILD_PYTHON_BINDINGS:bool=true
-DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=$(which python3) -DFORCE_RSUSB_BACKEND=true``

``$ make``

… wait several hours, nb. you may need to cool the *Pi* during compilation …

``# make install``


GPIO setup
^^^^^^^^^^

Install the standard *GPIO* libraries

``# apt install python-rpi.gpio python3-rpi.gpio``

Add your user to the *dialout* group

``# usermod -a -G dialout <username>``

You will need to reboot, or possibly just logout, for the change to take effect.


*The Pi should now be ready for installation and execution of this codebase.*


Project code
^^^^^^^^^^^^

Finally, the original code for the project is available on
`GitHub <https://github.com/wsdh500/roadtrain>`_.
