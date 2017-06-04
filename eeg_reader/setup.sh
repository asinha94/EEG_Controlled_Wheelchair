#!/bin/bash

# Make sure that the bluez version is 4.* because 5 will not work with the MindWave
sudo apt-get install -y libbluetooth-dev bluetooth python2.7-dev bluez

# Install All the python packages (Update as necessary)
sudo pip install -r requirements.txt

# In my case because I downgraded my bluetooth, the bluetooth gui got uninstalled. So for some reason I need to turn it on manually like so

# sudo rfkill unblock bluetooth
# sudo hciconfig hci0 up
# hciconfig hci0 XX:XX:XX:XX:XX:XX connect 

