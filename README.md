# Overview

This is designed to run on a fresh Raspberry Pi.  There is a python script `gps.py` which when running will get data from a USB GPS device and write the time, latitude, and longitude to a time-stamped file.

## Setup

Initial setup of a new Raspberry Pi will involve downloading and writing a Raspian image to the micro SD card according to instructions at `http://raspberrypi.org/downloads`

Once this is done, add an empty file called `ssh` to the boot folder on the SD card.  The enables `ssh` on boot, so you can connect to the Raspberry Pi via an ethernet cable.

Next, make a new directory under the `/boot/` folder, and copy the files in this repository into it.

Put the SD card into the Raspberry Pi and boot it up.  Plug in the GPS Dongle.

### Connecting to the Raspberry Pi by SSH

Find out the IP address of the Raspberry Pi by typing `ping raspberrypi.local` once you've connected the ethernet cable to the Pi.

Use the resultant IP address to SSH into the Pi, using `ssh pi@<IP-ADDRESS>` and using the default password `raspberry`

### Installation

When connected, run the shell script in `/boot/yournewdir/`  using `sudo ./setup.sh`

This should install the packages `pyserial` and `gpsd`, and copy the configuration files for `gpsd` and the `ntpd` daemon to the correct places.

It should also create a new directory `/usr/bin/gps_parser/` and put the python script `gps.py` into it.

If this doesn't work, best to make sure that the version of Raspbian is still using the same directories.

Now, restart the Pi with the command `sudo shutdown -r now` and wait for it to restart, before ssh-ing in again.

## Checking it's working

To check the `ntpd` time setting is working, you can use `ntpq -p` and look at the output.  There should be a line referring to the GPS, as well as the usual time servers which are not going to be accessible as there will be no internet connection (unless you've set that up yourself).

If not, check that the GPS is producing data at the serial port.  The setup files are expecting this data at `/dev/ttyACM0`.  If there are problems you'll need to check this is correct for the newly set up system.

Type `sudo stty -F /dev/ttyACM0 ispeed 4800 && cat </dev/ttyACM0` and you should see lines of data coming in.

If the port ACM0 is wrong, it will need to be found, and corrected in the python script and the `ntp.conf` file where it has the line `DEVICES="..."`

Once this is working, check the time of the Raspberry Pi with the command `date`.  It should show today's today and time.  If so, it is working and you can move on to using the python script.

## Running the GPS Parser

You can run the parser with `./usr/bin/gps_parser/gps.py`

*Note:* The other script `gps_parser.py` is an old version that sets the system clock itself, once per session.  This is not the ideal method of setting the clock, much better to use `gps.py` and the NTP daemon to set the time direct from the serial port.

## Support

Any issues, get in touch!
