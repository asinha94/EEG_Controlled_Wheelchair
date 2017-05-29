#!/bin/bash

# Make sure that the bluez version is 4.* because 5 will not work with the MindWave
sudo apt-get install -y libbluetooth-dev bluetooth python2.7-dev bluez

# Install All the python packages (Update as necessary)
sudo pip install -r requirements.txt

