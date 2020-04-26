#!/usr/bin/python3

import serial
import os

'''
GPS Parser version 2
Rob Webster
April 2020

- For receiving and parsing data from UBlox-7 USB GPS dongle on Raspberry Pi

- See README.md for setup instructions

- Time, Latitude, and Longitude data are written to a text file named "DDMMYY_gpsdata.txt" (comma separated values)
- Lat/Lon are in signed decimal degrees (eg Southern and Western hemispheres are -ve).

'''

# This is the port at which raw data arrives from the GPS dongle
port = "/dev/ttyACM0"

# The following line is an example of the raw NMEA message data, which is in byte string format so has to be decoded using the .decode() method:
# The first line contains time and lat/lon information.  The second line contains date information.
#
# $GPGGA,182322.00,5556.90084,N,00310.97671,W,1,04,6.02,96.3,M,49.8,M,,*75
# $GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68

def get_date_string(raw_data):
     # This function simply return the date from the NMEA message
     sd = raw_data.decode().split(',')
     return sd[9]

def change_datetime(datetime_string):
     #  Sets the date from the datetime string provided, by running the command 'timedatctl' using the os module.
     #  Only use if the proper NTPD / GPSD method is not working!
     try:
          os.system(f'sudo timedatectl set-time "{datetime_string}"')
          # print(f'date changed to {datetime_string}')
     except:
          print('date change unsuccessful...')

def get_gps_data(raw_data, date_string):
     #  This function parses out the useful information from NMEA messages beginning with the code '$GPGGA'
     #  These messages contain both lat/lon and time information on the GPS signal
     #  The following 'if' statement checks if the message starts with the correct identifier code, and if so parses it

     # The following lines build a longer date string in order to set the system clock later on:
     dd = date_string[0:2]
     mm = date_string[2:4]
     yyyy = '20' + date_string[4:6]
     long_date_string = f"{yyyy}-{mm}-{dd}"

     # Checks if the current message is a "$GPGGA" message", and that there is a valid date_string and processes the message if so:
     if raw_data[0:6].decode() == "$GPGGA" and date_string != None:
          #  sd stands for "split data" - the message is split into comma separated components and stored in this list
          sd = raw_data.decode().split(",")
          # A string representation of the time of the message is built from the required parts of the 'sd' list:
          time = sd[1][0:2] + ":" + sd[1][2:4] + ":" + sd[1][4:6]
          # lat gives a float representation of the latitude in decimal degrees
          lat = float(sd[2])/100
          # NS gives the hemisphere of the current fix :  either 'N' or 'S'
          NS = sd[3]
          # lon gives a float representation of the longitude in decimal degrees
          lon = float(sd[4])/100
          # EW gives the direction from the meridian of the longitude : either 'E' or 'W'
          EW = sd[5]
          # The following simply converts the latitude to a negative number if in the Southern Hemisphere
          if NS == 'S':
               lat *= -1
          # And then converts the longitude to a negative number is the fix is west of the meridian
          if EW == 'W':
               lon *= -1
          # The following prints out the current lat/lon and the time of the fix.  The :.6f parts make the output display with a consistent number of decimal places
          print(f"{time}  latitude : {lat:.6f}, longitude : {lon:.6f}")
          # Opens up a file named with the datestamp and appends a line with the latest time and lat/lon data: 
          with open(f'{date_string}_gpsdata.txt', 'a') as f:
               f.write(f"{time},{lat:.6f},{lon:.6f}\n")
          # The following creates a string containing both the date and the time in the correct format for setting the system clock: 
          datetime_string = f"{long_date_string} {time}"
          #print(f"datetime_string is : {datetime_string}")

          # change_datetime(datetime_string)



print(f"Listening on port {port}...")
# Uses the pyserial module to listen for GPS raw data on port specified at the top of the file
s = serial.Serial(port, baudrate=9600, timeout = 1)
# Initialises a variable to hold the date
date_string = None

while True:
     # Each time round the infinite loop, read raw data from the serial port:
     raw_data = s.readline()
     # Test the raw data to see if the current line contains date information, and update the date_string variable if so
     if raw_data[0:6].decode() == '$GPRMC':
          date_string = get_date_string(raw_data)
     # If the date_string variable has a valid date in it, run get_gps_data to gather the necessary data and write it to file:
     # This ensures that the get_gps_data function is not run until at least one $GPRMC message has been collected, to get a valid date.
     if date_string != None:
          get_gps_data(raw_data, date_string)
   
   
