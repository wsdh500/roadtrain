# AAIP Roadtrain Project
## Installation
Take a Raspberry Pi 4 Model B with a freshly installed operating system and install git 

`# apt install git`

before checking out this repository

`$ git clone https://github.com/wsdh500/roadtrain`

`$ cd roadtrain`

In order to play back video, pip3 will need to be installed before installing the Python OpenCV bindings

`# apt install python3-pip`

`# pip install opencv-python`

Installing the OpenCV bindings will also install Numpy.

Finally, download the videos folder from the shared Google Drive folder into the working directory.

You should now be able to run the demo.

`$ python3 fullscreen_playback.py`
