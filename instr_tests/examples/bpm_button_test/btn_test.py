###################################################################################
#
# Name:
#
#	BPM BUTTON TEST
#
# Test overview:
#
#	Get the TDR response of each BPM button in order to get its capacitance.
#
# Script description:
#
#       Save the TDR 'response 4' data obtained by the Wide-Bandwidth
# Oscilloscope. The script saves the response data to the oscilloscope and a
# copy to the TEST_PATH location specified in the script. The script DO NOT
# configure NEITHER calibrate the oscilloscope for TDR measurement, the user 
# must prepare and start the measurement before starting the script.
#
# Input Arguments: <button_code>	
#
###################################################################################

import visa
import time
import datetime
import sys
import os

# check input arguments
argc = len(sys.argv)

if argc < 2:
	print("Error: not enough input arguments")
	sys.exit()
elif argc > 2:
	print("Error: too many input arguments")
	sys.exit()

# filename
filename = sys.argv[1]+'_'+str(datetime.date.today())

# connection
if 'rm' in globals():
	pass
else:
	global rm
	rm = visa.ResourceManager('@py')

# oscilloscope IP
ip = "10.0.18.63"

# open connection
wbo_socket = rm.open_resource('TCPIP::'+ip+'::inst0::INSTR')

# save folder
TEST_PATH = '/media/button_tdr'

#if not os.access(TEST_PATH, os.F_OK):	# create directory if it does not exit
#	os.makedirs(TEST_PATH)

# save TDR response
with open(TEST_PATH+'/'+filename, 'w') as f:

	wbo_socket.write(':DISK:STORe resp4,"'+filename+'",TEXT,XYVerbose')

	data = wbo_socket.query(':DISK:TFILe? "D:\\User Files\\Waveforms\\'+filename+'.txt"')

	f.write(data)

# read last error message
print(wbo_socket.query(":SYSTem:ERRor? STRING"))
