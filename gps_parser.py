import serial
import os

'''

GPS Parser version 1.0
Rob Webster
December 2019

- For receiving and parsing data from UBlox-7 USB GPS dongle on Raspberry Pi

- See README.txt for setup instructions

- Time, Latitude, and Longitude data are written to a text file named "DDMMYY_gpsdata.txt" (comma separated values)
- Lat/Lon are in signed decimal degrees (eg Southern and Western hemispheres are -ve).

- The program also sets the system clock from the GPS data once per session

'''

# This is the port at which raw data arrives from the GPS dongle
port = "/dev/ttyACM0"

# The following line is an example of the raw NMEA message data
# This comes from the serial connection as byte string data so has to be decoded using the .decode() method.
#
# The first line contains time and lat/lon information.  The second line contains date information.
#
# $GPGGA,182322.00,5556.90084,N,00310.97671,W,1,04,6.02,96.3,M,49.8,M,,*75
# $GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68


def change_datetime(datetime_string):
    #  Sets the date from the datetime string provided, by running the command 'timedatctl' using the os module.
    try:
        os.system(f'sudo timedatectl set-time "{datetime_string}"')
        print(f'System date and time set to {datetime_string}')
    except:
        print('Date change unsuccessful...')


def parse_gps_data(raw, date_str, date_corr):
    #
    #  This function parses out the useful information from NMEA messages beginning with the code '$GPGGA'
    #  These messages contain both lat/lon and time information on the GPS signal
    #

    #  sd stands for "split data" - the message is split into comma-separated components and stored in this list:
    sd = raw.decode().split(",")

    # A string representation of the time of the message is built from the required parts of the 'sd' list:
    time = sd[1][0:2] + ":" + sd[1][2:4] + ":" + sd[1][4:6]

    # lat gives a float representation of the latitude in decimal degrees
    lat = float(sd[2]) / 100

    # NS gives the hemisphere of the current fix :  either 'N' or 'S'
    ns = sd[3]

    # lon gives a float representation of the longitude in decimal degrees
    lon = float(sd[4]) / 100

    # EW gives the direction from the meridian of the longitude : either 'E' or 'W'
    ew = sd[5]

    # The following simply converts the latitude to a negative number if in the Southern Hemisphere
    if ns == 'S':
        lat *= -1

    # And then converts the longitude to a negative number is the fix is west of the meridian
    if ew == 'W':
        lon *= -1

    # The following prints out the current lat/lon and the time of the fix.  The :.6f parts make the output display
    # with a consistent number of decimal places
    print(f"{time}  latitude : {lat:.6f}, longitude : {lon:.6f}")

    #
    # Opens up a file named with the datestamp and appends a line with the latest time and lat/lon data:
    #
    try:
        with open(f'{date_string}_gpsdata.txt', 'a') as f:
            f.write(f"{time},{lat:.6f},{lon:.6f}\n")
    except:
        print("Unable to write data to file....")

    # Build an appropriate datetime string in order to set the system clock later on:
    dd = date_str[0:2]
    mm = date_str[2:4]
    yyyy = '20' + date_str[4:6]
    datetime_string = f"{yyyy}-{mm}-{dd} {time}"

    # Call the change_datetime function to set the current system date and time
    # but ensure that it is only changed once per session
    if date_corr is False:
        date_corr = True
        change_datetime(datetime_string)

    # Returns a flag to say that the date and time has been set
    return date_corr


# Uses the pyserial module to listen for GPS raw data on port specified at the top of the file
s = serial.Serial(port, baudrate=9600, timeout=1)
print(f"Listening on port {port}...")

# Initialises a variable to hold the date
date_string = None

# Initialises a variable to record whether the date has been corrected or not during this session
date_corrected = False

while True:

    # Each time round the infinite while loop, read raw data from the serial port:
    raw_data = s.readline()
    message_id = raw_data[0:6].decode()  # The first 6 characters of the message are the identifier

    # Test the raw data to see if the current line contains date information, and update the date_string variable
    if message_id is '$GPRMC' and date_corrected is False:
        date_string = raw_data.decode().split(',')[9]

    # If the date_string variable has a date in it, run parse_gps_data to gather the necessary data
    # and write it to today's data file.  This ensures that the function is not run until at least one
    # $GPRMC message has been collected, to get a valid date.
    if message_id is '$GPGGA' and date_string is not None:
        date_corrected = parse_gps_data(raw_data, date_string, date_corrected)
