# create directory for the gps_parser code to live
mkdir /usr/bin/gps_parser

# copy the python script to this folder
cp /boot/gps_setup/gps.py /usr/bin/gps_parser/

#install pyserial from wheel
pip3 install /boot/gps_setup/pyserial-3.4-py2.py3-none-any.whl

# install gpsd and overwrite default settings file
apt install /boot/gps_setup/gpsd_3.17-7_armhf.deb
cp /boot/gps_setup/gpsd /etc/default/gpsd

# overwrite the /etc/ntp.conf file
cp /boot/gps_setup/ntp.conf /etc/

# restart the pi
#shutdown -r now
