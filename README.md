# AAIP Roadtrain Project
## Installation
Take a Raspberry Pi 4 Model B with a freshly installed operating system and install git 

`# apt install git`

before checking out this repository

`$ git clone https://github.com/wsdh500/roadtrain`

`$ cd roadtrain`

In order to play back video, pip3 will need to be installed before installing the Python OpenCV bindings

`# apt install python3-pip`

`$ pip install opencv-python`

Installing the OpenCV bindings will also install Numpy.

In order to use push-buttons to switch videos, you will need to install the appropriate libraries

`# apt install python-rpi.gpio python3-rpi.gpio`

Finally, download the *videos* folder from the shared Google Drive folder into the working directory.

You should now be able to run the demo.

`$ python3 fullscreen_playback.py`

Pressing *n*, or clicking the push-button connected to board pin 15, will switch videos, and pressing *q* will quit the demo.