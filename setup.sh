# create directory for the gps_parser code to live
sudo mkdir /usr/bin/gps_parser3

# copy the python script to this folder
sudo cp /boot/gps_setup/gps.py /usr/bin/gps_parser3/

#install pyserial from wheel
sudo pip3 install /boot/gps_setup/pyserial-3.4-py2.py3-none-any.whl

# install gpsd and overwrite default settings file
sudo apt install /boot/gps_setup/gpsd_3.17-7_armhf.deb
sudo cp /boot/gps_setup/gpsd /etc/default/gpsd

# overwrite the /etc/ntp.conf file
sudo cp /boot/gps_setup/ntp.conf /etc/

# restart the pi
#sudo shutdown -r now
