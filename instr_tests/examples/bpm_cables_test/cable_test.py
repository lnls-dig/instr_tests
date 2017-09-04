########################### Run in python 3 ###########################################
#
#	Device test script using Agilent E5061B Network Analizer 
#	and DCA-X 86100D Wide-Bandwidth Oscilloscope
#
#######################################################################################

import sys
import socket
import time
import os

import instr_tests as instr
import agilent_86100d

import util

################################## Initialization #####################################
#
#	Verify input arguments.
#	Open connection with Network Analyser.
#	Open connection with Wide-Bandwidth Oscilloscope.
#	Set up instruments for the test procedure.
#
#######################################################################################

###### Verify input arguments #########################################################

argc = len(sys.argv)	# input argument count

if argc > 3:	# excess input arguments check
	print('Error: Too many input arguments')
	sys.exit(0)
if argc < 3:	# missing input arguments check
	print('Error: Input argument missing')
	sys.exit(0)

vna_ip_numbers = sys.argv[1].split('.')
wbo_ip_numbers = sys.argv[2].split('.')

if len(vna_ip_numbers) != 4:	# invalid vna ip check
	print('Error: Invalid input IP address for Network Analizer')
	sys.exit(0)

if len(wbo_ip_numbers) != 4:	# invalid wbo ip check
	print('Error: Invalid input IP address for Wide-Bandwidth Oscilloscope')
	sys.exit(0)

for i in range(4):	# invalid vna ip check
	if int(vna_ip_numbers[i]) > 255 or int(vna_ip_numbers[i]) < 0:
		print('Error: Invalid input IP address for Network Analyser')
		sys.exit(0)

for i in range(4):	# invalid wbo ip check
	if int(wbo_ip_numbers[i]) > 255 or int(wbo_ip_numbers[i]) < 0:
		print('Error: Invalid input IP address for Wide-Bandwidth Oscilloscope')
		sys.exit(0)

###### Connect to modules and configure them ##########################################

print('Trying to connect to Agilent E5061B ...')

try:
    vna = instr.instruments.vna.AgilentE5061B(sys.argv[1])	# open communication with Network Analyser
except:
    sys.stdout.write("\nUnable to reach the vector network analyzer (Agilent E5061B) through the " +
                     "network. Exiting...\n\n")
    exit()

# Network Analyser settings
vna.set_data_format("MLOG")					# Log Magnitude data format
vna.write("SENS1:CORR:STAT 1")					# correction state ON
vna.write(":DISP:WIND1:TRAC1:Y:PDIV 10")			# 10 dB per division
vna.write(":DISP:WIND1:TRAC1:Y:RLEV -30")			# displayed trace reference position

print('Done')

print('\n')
print('Trying to connect to Agilent DCA-X 86100D ...')		# open communication with Wide-Bandwidth Oscilloscope

try:
	# connect to Wide-Bandwidth Oscilloscope
	wbo = agilent_86100d.Agilent86100D(sys.argv[2])
except:
	print "Could not connect to Wide-Bandwidth Oscilloscope"

# High-Bandwidth Oscilloscope settings
# NO CONFIG

print('Done')

################################## Test Routine #######################################
#
#
#	Run test procedure.
#
#
#######################################################################################

###### Manual procedure ##############################################################

print('\n')
print('********** Manual test configuration **********')

valid = 0
while valid != 1:
	test_folder = raw_input('Enter output folder name: ')
	print('Confirm output folder name as: '+test_folder)
	print('y) Yes')
	print('n) No')
	while valid != 1:
		conf = raw_input().replace("\n","").lower()
		if conf == 'y' or conf == 'yes' or conf == 'n' or conf == 'no':
			valid = 1
	valid = 0
	if conf == 'y' or conf == 'yes':
		valid = 1

print('\n')
print('#################### TEST PROCEDURE START ####################')
print('\n\n\n')

util.manual_test(test_folder, vna, wbo)		# start test procedure

print('\n\n\n')
print('#################### TEST PROCEDURE END ####################')

