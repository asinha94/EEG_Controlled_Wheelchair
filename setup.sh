#!/bin/bash

# I dont remember if 'bluetooth' is needed, but install that anyway. the dev lib is necessary to compile pybluez
sudo apt-get install -y libbluetooth-dev bluetooth python2.7-dev

# Install All the python packages (Update as necessary)
sudo pip install -r requirements.txt

# Download from source and install
git clone https://github.com/akloster/python-mindwave
pushd python-mindwave
python setup.py install
popd
rm -rf python-mindwave

# If you have trouble connecting your device to the MindWave mobile copy hte pincodes file into
# /usr/var/lib/bluetooth/${YOUR_BLUETOOTH_MAC_ADDRESS}/
# Then restart your bluetooth service
# This is strictly Debian-variants only


