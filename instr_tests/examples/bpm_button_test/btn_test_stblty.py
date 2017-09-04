##################################################################################
# Name: 
#
#	BPM BUTTON STABILITY TEST
#
# Test overview:
#
# 	The purpose of the test is to obtain the variation in TDR response of a
# BPM button along many hours as result of room temperature variations.
#
# Script description:
#
#	Save the TDR 'response 4' data obtained by the Wide-Bandwidth
# Oscilloscope at regular intervals. The script saves the response data to the
# oscilloscope and a copy to the TEST_PATH location specified in the script.
# The first sample is saved at script initialization, while subsequent samples
# are saved at 1 hour intervals. The script DO NOT configure NEITHER calibrate 
# the oscilloscope for TDR measurement, the user must prepare and start the
# measurement before starting the script.
#
# Input Arguments: <button_code>
#
##################################################################################

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

# test folder
TEST_PATH = '/media/button_tdr/thermal_stability'

# sample counter
sample_cnt = 1

##### Save first response for button #####

# get current date and time
curr_date = datetime.datetime.now() # date
curr_time = curr_date.time() # time
next_date = curr_date + datetime.timedelta(hours=1) # next sample date and time

# filename
fmt_time = str(curr_time.hour)+'-'+str(curr_time.minute)+'-'+str(curr_time.second)
filename = sys.argv[1]+'_'+str(curr_date.date())+'_'+fmt_time

print 'Saving TDR response #1 at '+str(curr_time)

# save waveform
with open(TEST_PATH+'/'+filename, 'w') as f:

	wbo_socket.write(':DISK:STORe resp4,"'+filename+'",TEXT,XYVerbose')

	data = wbo_socket.query(':DISK:TFILe? "D:\\User Files\\Waveforms\\'+filename+'.txt"')

	f.write(data)

# read last error message
print(wbo_socket.query(":SYSTem:ERRor? STRING"))

# Keep saving the TDR response every hour
try:
	while True:

		# get current date and time
		curr_date = datetime.datetime.now()
		curr_time = curr_date.time()

		if curr_date >= next_date:

			# update next date
			next_date = curr_date + datetime.timedelta(hours=1) # next sample date and time
		
			# filename
			fmt_time = str(curr_time.hour)+'-'+str(curr_time.minute)+'-'+str(curr_time.second)
			filename = sys.argv[1]+'_'+str(curr_date.date())+'_'+fmt_time

			sample_cnt += 1

			print 'Saving TDR response #'+str(sample_cnt)+' at '+str(curr_time)

			# save waveform
			with open(TEST_PATH+'/'+filename, 'w') as f:

				wbo_socket.write(':DISK:STORe resp4,"'+filename+'",TEXT,XYVerbose')

				data = wbo_socket.query(':DISK:TFILe? "D:\\User Files\\Waveforms\\'+filename+'.txt"')

				f.write(data)

			# read last error message
			print(wbo_socket.query(":SYSTem:ERRor? STRING"))

# exit on keyboard interrupt
except KeyboardInterrupt:
	pass
