#!/bin/bash
sudo apt install libjasper-dev -y
sudo apt install libqtgui4 -y
sudo apt install libqt4-test -y
sudo apt install libhdf5-dev libhdf5-serial-dev -y

sudo apt install -y python3-libcamera python3-kms++
sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip
pip3 install numpy --upgrade
pip3 install picamera2

sudo pip3 install opencv-contrib-python
sudo pip3 install tflite-runtime
