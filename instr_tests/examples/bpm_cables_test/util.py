########################### Run in python 3 ###########################################
#
#		Utility functions for bpm cables testing
#
#######################################################################################

import numpy as np
import sys
import socket
import time
import os

import instr_tests as instr

###########################  Constants ###############################################

START_FREQ_BROAD = '5E3'
END_FREQ_BROAD = '3E9'

START_FREQ_NARROW = '450000000'
END_FREQ_NARROW = '550000000'

########################### Function Definitions #####################################
"""
Name:
		visual_inspection

Description:
		Ask user for visual inspection information and save it to a file with the specified name piece to the specified folder.

Input arguments:
		filename	A name piece to be part of the inspection file name.

		file_path	The path to the location where the inspection file is going to be saved.

"""
def visual_inspection(file_path, filename):

	print('\n************** Visual Inspection **************\n')

	# ask user to provide crimping/robustness/thermo-shrinkable quality
	options = ['Excellent','Good','Bad']
	choice = user_choice(options, 'Evaluate quality of crimping / robustness / thermo-shrinkable:', confirm=True)

	phys_quality = options[choice]	# physical quality

	# ask user to provide identification quality
	options = ['Excellent','Good','Bad']
	choice = user_choice(options, 'Evaluate identification quality:', confirm=True)

	ident_quality = options[choice]	# identification quality

	# ask user to enter observation
	observ = ''
	valid = 0
	while valid != 1:
		observ = raw_input('Enter observation: ')
		print('Confirm observation ['+observ+'] ? (y/n) ')
		while valid != 1:
			conf = raw_input()
			conf = conf.lower()
			if conf == 'y' or conf == 'yes' or conf == 'n' or conf == 'no':
				valid = 1
		valid = 0
		if conf == 'y' or conf == 'yes':
			valid = 1

	# save inspection data
	data_pairs = [['Physical Quality', phys_quality], ['Identification Quality', ident_quality], ['Observation', observ]]

	save_statistics(file_path+'/'+'inspection_'+filename+'.txt', data_pairs, append=False)
"""
Name:
		save_statistics

Description:
		Saves a set of data pairs to a file, each pair containing a name and a data value.

Input arguments:
		filename	Filename including path to save location.

		data_pairs	A list of pairs (tuples or lists) containing each the name and value of a given piece of data.

		append		A boolean value indicating whether the data pairs should be appended to the file, or the file should be overwritten.
"""
def save_statistics(filename, data_pairs, append=False):
	
	op = 'w'	# initialize operation as write

	if append:
		op = 'a'

	with open(filename, op) as f:

		for data in data_pairs:

			f.write(data[0]+"\t"+str(data[1])+"\n")
"""
Name:
		save_csv

Description:
		Save data arrays to .csv file. Each input data array <n> is saved to column <n> of the .csv file.

Input arguments:
		filename	Filename including path to save location.

		data		A list of data arrays of same length. An error is generated if the data arrays have different length.
"""
def save_csv(filename, data):

	data_col_cnt = len(data)

	# data is empty
	if data_col_cnt == 0:
		print("In save_csv function: Empty data array list")
		return

	data_row_cnt = len(data[0])

	# check data arrays' length
	for i in range(1, data_col_cnt):
		if data_row_cnt != len(data[i]):
			print("Error in save_csv function: data arrays have different length")
			return

	# write data file
	with open(filename,'w') as f:
		for row in range(0, data_row_cnt):
			for col in range(data_col_cnt-1):
				f.write(str(data[col][row])+",")
			f.write(str(data[data_col_cnt-1][row])+"\n")
"""
Name:
		vna_test

Description:
		Perform S11, S21, and S22 measurements and save results to specified folder.

Input arguments:
		file_path	The path to which the test files are going to be saved.

		vna		An object containing a Vector Network Analyser instance.

		dev_name	The name of the device being tested. The test files names are built from the device name.

		test_ranges	A list of ranges. Each range is a tuple containing start and stop frequencies.

		test_suffixes	A list of suffixes to use when saving data for each frequency range. If there are less suffixes than ranges, the missing suffixes are set to the range values.
"""
def vna_test(file_path, vna, dev_name, test_ranges, test_suffixes):

	# add slash
	if file_path != "" and file_path[-1:] != "/":
		file_path += "/"

	suffix_cnt = len(test_suffixes)

	# ----------- Guide user through setup before measurement starts -----------
	print('\n!!!!!!!!! INSTRUCTIONS !!!!!!!!!\n')
	print('1- Connect device to Agilent E5061B Network Analizer')
	print('2- Press <ENTER> to start measurement')
	print('(Enter "skip" to skip measurement)')
	cmd = raw_input()
	cmd = cmd.replace("\n","").lower()

	if cmd == 'skip':
		print("\n[Measurement skipped]")
	else:
		meas_again = 1

		while meas_again == 1:

			s11_1mhz = 0	# init s11 at 1mhz
			s11_500mhz = 0	# init s11 at 500MHz
			s11_avg = 0	# init s11 average
			s21_1mhz = 0	# init s21 at 1mhz
			s21_500mhz = 0	# init s21 at 500MHz
			s21_3ghz = 0	# init s21 at 3GHz
			s22_1mhz = 0	# init s22 at 1mhz
			s22_500mhz = 0	# init s22 at 500MHz
			s22_avg = 0	# init s22 average

			suffix = ''	# init suffix

			meas_again = 0
			print('\n[Measuring ...]')

			for i in range(0, len(test_ranges)):

				if suffix_cnt > i:		# get suffix
					suffix = test_suffixes[i]
				else:
					suffix = str(test_ranges[i][0])+'_'+str(test_ranges[i][1]) 

				# ----------- Set frequency range -----------			
				vna.freq_range(test_ranges[i][0], test_ranges[i][1])
				print('[Range set to ('+str(test_ranges[i][0])+', '+str(test_ranges[i][1])+')]')

				# ----------- Get frequency stimulus values -----------
				freq = vna.get_frequency_data()

				# ----------- Measure S11 -----------
				s11_data = vna.get_s11_data()

				# ----------- Get S11 stastistics -----------
				if suffix == 'broad':
					s11_avg = np.mean(s11_data)	# calculate average

					vna.write(":CALC1:MARK1:X 1E6")	# marker at 1 MHz
					y_str = vna.query(":CALC1:MARK1:Y?")	# read y at marker position
					s11_1mhz = float((y_str.replace("\n","").split(","))[0])

				elif suffix == 'narrow':
					vna.write(":CALC1:MARK1:X 5E8")	# marker at 500 MHz
					y_str = vna.query(":CALC1:MARK1:Y?")	# read y at marker position
					s11_500mhz = float((y_str.replace("\n","").split(","))[0])

				# ----------- Save S11 data -----------
				filename = file_path+'s11_'+dev_name+'_'+suffix+'.csv'
				data = [freq, s11_data]
				save_csv(filename, data)

				# ----------- Measure S21 -----------
				s21_data = vna.get_s21_data()

				# ----------- Get S21 statistics -----------
				if suffix == 'broad':
					vna.write(":CALC1:MARK1:X 3E9")	# marker at 3 GHz
					y_str = vna.query(":CALC1:MARK1:Y?")	# read y at marker position
					s21_3ghz = float((y_str.replace("\n","").split(","))[0])

					vna.write(":CALC1:MARK1:X 1E6")	# marker at 1 MHz
					y_str = vna.query(":CALC1:MARK1:Y?")	# read y at marker position
					s21_1mhz = float((y_str.replace("\n","").split(","))[0])

				elif suffix == 'narrow':
					vna.write(":CALC1:MARK1:X 5E8")	# marker at 500 MHz
					y_str = vna.query(":CALC1:MARK1:Y?")	# read y at marker position
					s21_500mhz = float((y_str.replace("\n","").split(","))[0])

				# ----------- Save S21 data -----------
				filename = file_path+'s21_'+dev_name+'_'+suffix+'.csv'
				data = [freq, s21_data]
				save_csv(filename, data)

				# ----------- Measure S22 -----------
				s22_data = vna.get_s22_data()

				# ----------- Get S22 statistics -----------
				if suffix == 'broad':
					s22_avg = np.mean(s22_data)	# calculate average

					vna.write(":CALC1:MARK1:X 1E6")	# marker at 1 MHz
					y_str = vna.query(":CALC1:MARK1:Y?")	# read y at marker position
					s22_1mhz = float((y_str.replace("\n","").split(","))[0])

				elif suffix == 'narrow':
					vna.write(":CALC1:MARK1:X 5E8")	# marker at 500 MHz
					y_str = vna.query(":CALC1:MARK1:Y?")	# read y at marker position
					s22_500mhz = float((y_str.replace("\n","").split(","))[0])

				# ----------- Save S22 data -----------
				filename = file_path+'s22_'+dev_name+'_'+suffix+'.csv'
				data = [freq, s22_data]
				save_csv(filename, data)

			# ----------- Save statistics -----------
			filename = file_path+'statistics_'+dev_name+'.txt'
			stat_info = [['S11 1MHz', s11_1mhz], ['S11 500MHz', s11_500mhz], ['S11 AVG', s11_avg], ['S21 1MHz', s21_1mhz], ['S21 500MHz', s21_500mhz], ['S21 3GHz', s21_3ghz], ['S22 1MHz', s22_1mhz], ['S22 500MHz', s22_500mhz], ['S22 AVG', s22_avg]]
			save_statistics(filename, stat_info, append=False)

			# ----------- Confirm that test is valid -----------
			print('[Done]')
			print('\n---> Choose option:')
			print('r) Redo measurement')
			print('c) Continue and save')
	
			valid = 0
			while valid != 1:
				cmd = raw_input()	
				cmd = cmd.replace("\n","").lower()

				if cmd == 'c' or cmd == 'r':
					valid = 1
			if cmd == 'r':
				meas_again = 1
"""
Name:
		wbo_test

Description:
		Perform TDR measurement and save result to specified folder.

Input arguments:
		file_path	The path to which the test files are going to be saved.

		vna		An object containing a Wide-Bandwidth Oscilloscope instance.

		dev_name	The name of the device being tested. The test file name is built from the device name.
"""
def wbo_test(file_path, wbo, dev_name):

	# add slash
	if file_path != "" and file_path[-1:] != "/":
		file_path += "/"

	# ----------- Guide user through setup before measurement starts -----------
	print('\n!!!!!!!!! INSTRUCTIONS !!!!!!!!!\n')
	print('1- PUT ON THE GROUND BRACELET')
	print('2- Connect device to DCA-X 86100D Wide-Bandwidth Oscilloscope')
	print('3- Press <ENTER> to start measurement')
	print('Enter "skip" to skip measurement')
	cmd = raw_input()
	cmd = cmd.replace("\n","").lower()

	if cmd == 'skip':
		print("[Measurement skipped]")
	else:
		meas_again = 1

		while meas_again == 1:

			meas_again = 0
			print('\n[Measuring ...]')

			# ----------- Measure TDR -----------
			# Measurement is assumed to be running
			time.sleep(1.0)

			# ----------- Save TDR info -----------
			wbo.write(':DISK:STORe resp3,"'+dev_name+'",TEXT,XYVerbose')
			data = wbo.query(':DISK:TFILe? "D:\\User Files\\Waveforms\\'+dev_name+'.txt"')
			filename = file_path+'tdr_'+dev_name+'.txt'
			with open(filename, 'w') as f:
				f.write(data)

			# ----------- Get TDR delay -----------
			tdr_delay = 0
			data_idx = 0

			lines = data.split("\r\n")
			for line in lines:	# find data start
				data_idx += 1
				if line.lower() == 'xy data:':
					break

			lines = lines[data_idx:] # remove header

			for line in lines:	# find y step
				if line != '\n':
					xy_data = [float(i) for i in line.split(",")]
					if len(xy_data) == 2:
						if xy_data[1] >= 50:	# if y is greater than 50%
							tdr_delay = xy_data[0]
							break

			# ----------- Save delay to statistics -----------
			filename = file_path+'statistics_'+dev_name+'.txt'
			stat_info = [['TDR', tdr_delay]]
			save_statistics(filename, stat_info, append=True)

			# ----------- Confirm that test is valid -----------
			print('[Done]')
			print('\n---> Choose option:')
			print('r) Redo measurement')
			print('c) Continue and save')
	
			valid = 0
			while valid != 1:
				cmd = raw_input()	
				cmd = cmd.replace("\n","").lower()

				if cmd == 'c' or cmd == 'r':
					valid = 1
			if cmd == 'r':
				meas_again = 1
"""
Name:
		automatic_test

Description:
		Receives as input argument a file containing the device list for testing.
		Run through lines, get section and subsections.
		Create directories for the new sections in the test folder.
		If an existing folder is specified, just enter the folder.
		Perform the necessary measurements for the device specified in the line.
		Save results to folder.

Input arguments:
		dev_list	A file containing the list of devices to test.
				Each line of the file must refer to each device to test.
				Each column of the file specifies a folder that should be part of the device result files path.
				Columns delimiters are <tab> characters ('\t').
				The last column must contain the device code. This code is used by the test functions to build the test files name.

		test_folder	The desired test folder name.

		vna		An object containing a Vector Network Analyser instance.

		wbo		An object containing a Wide-Bandwidt Oscilloscope instance.
"""
def automatic_test(dev_list, test_folder, vna, wbo):

	with open(dev_list, 'r') as test_file:			# device list file open

		test_count = 0					# test counter

		for line in test_file:

			folder_structure = line.replace("\n","").split("\t")	# split line into sections and cable ID

			file_path = '/'.join(folder_structure[:-1])		# build file path from specified sections

			file_path = os.getcwd()+"/"+test_folder+"/"+file_path	# append current path and test folder to file path

			if not os.access(file_path, os.F_OK):			# create directory if it does not exit
				os.makedirs(file_path)

			range1 = (START_FREQ_BROAD, END_FREQ_BROAD)		# prepare ranges
			ranges = [range1]
			suffixes = []

			vna_test(file_path, vna, folder_structure[-1], ranges, suffixes)# Perform test with Network Analyser

			wbo_test(file_path, wbo, folder_structure[-1])		# Perform test with Wide-Banwidth Oscilloscope

			test_count += 1						# increment test count

	print('########## Test complete ##########')
	print('#\n#\n')
	print('# Devices tested:',test_count)

"""
Name:
		manual_test

Description:	
		Ask user for manufacturer and cable size.
		Create directories for the new sections.
		If an already existing folder is specified, just enter the folder.
		Perform the necessary measurements for the devices in the specified category.
		Ask the user the action to take when appropriate.

Input arguments:
		test_folder	The desired test folder name.
	
		vna		An object containing a Vector Network Analyser instance.

		wbo		An object containing a Wide-Bandwidt Oscilloscope instance.
"""
def manual_test(test_folder, vna, wbo):

	exit_test = 0		# exit flag
	test_count = 0		# test counter

	while exit_test == 0:

		same_manufac = 1
		same_size = 1

		options = ['Rosenberger','DataLink','Axon','Hytem']
		choice = user_choice(options, 'Enter manufcturer name:', confirm=False)	# ask for manufacturer option
		manufac= options[choice]	# get manufacturer name

		while same_manufac == 1 and exit_test != 1:

			options = ['Short','Medium','Long']
			choice = user_choice(options, 'Enter cable size:', confirm=False)	# ask for cable size
			cable_size = options[choice]	# get cable size

			same_size = 1

			while same_size == 1 and exit_test != 1 and same_manufac == 1:

				print('Enter cable code:')			# ask for cable code
				code = raw_input()				# get cable code
				code = code.replace("\n","")

				print('\n')
				print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
				print('CONFIRM CABLE INFORMATION:')	# confirm cable information			
				print('Manufacturer: '+manufac)
				print('Size: '+cable_size)
				print('Code: '+code)
				print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
				print('\n')
				print('Confirm? (y/n)')
				conf = 'n'
				valid = 0
				while valid != 1:
					conf = raw_input()
					conf = conf.replace("\n","").lower()
					if conf == 'y' or conf == 'n':
						valid = 1
				if conf == 'y':	# proceed

					colors = ['blue', 'yellow', 'white', 'green']		# Cable colors
					if cable_size == 'Medium':
						colors = ['red', 'blue', 'yellow', 'white', 'green']	# Cable colors for size medium
		
					for color in colors:						# Make tests for all cable colors

						file_path = manufac+'/'+cable_size+'/'+code+'/'+color	# build file path from specified sections

						file_path = os.getcwd()+"/"+test_folder+"/"+file_path	# append current path and test folder to file path

						if not os.access(file_path, os.F_OK):			# create directory if it does not exit
							os.makedirs(file_path)

						print('\n************** '+color.upper()+' cable **************\n')


						if color != 'red':
							range1 = (START_FREQ_BROAD, END_FREQ_BROAD)		# prepare ranges
							range2 = (START_FREQ_NARROW, END_FREQ_NARROW)
							ranges = [range1, range2]
							suffixes = ['broad', 'narrow']
						else:
							range1 = (START_FREQ_BROAD, END_FREQ_BROAD)
							ranges = [range1]
							suffixes = ['broad']				

						vna_test(file_path, vna, code+'_'+color, ranges, suffixes)# Perform test with Network Analyser
						wbo_test(file_path, wbo, code+'_'+color)		# Perform test with Wide-Banwidth Oscilloscope

						test_count += 1						# increment test count

					print('##### Finished testing all colors #####')	# finished measuring all colors

					file_path = os.getcwd()+"/"+test_folder+"/"+manufac+'/'+cable_size+'/'+code
					visual_inspection(file_path, code)	# make visual inspection

					print("###############################")	# remind user to take a picture
					print("#                             #")
					print("# TAKE A PICTURE OF THE CABLE #")
					print("#                             #")
					print("#        _[]_/____\__n_       #")
					print("#       |_____.--.__()_|      #")
					print("#       |LI  //# \\\\    |      #")
					print("#       |    \\\\__//    |      #")
					print("#       |     '--'     |      #")
					print("#   jgs '--------------'      #")
					print("#                             #")
					print("###############################")

					key = raw_input('Press <ENTER> to continue')
					print("\n\n")

				valid = 0
				while valid != 1:
					print('Enter one of the following options:')	# ask user for next action
					print('c) Choose another code')
					print('s) Choose another size')
					print('m) Choose another manufacturer')
					print('e) Exit test')
					
					option = raw_input()
					option = option.replace("\n","").lower()
					if option == 'c' or option == 's' or option == 'm' or option == 'e':
						valid = 1
					else:
						print('Invalid input: Must be "c", "s", "m" or "e"')
				if option == 's':
					same_size = 0
				elif option == 'm':
					same_manufac = 0
				elif option == 'e':
					exit_test = 1

	print('########## Test complete ##########')
	print('#\n#\n')
	print('# Devices tested:',test_count)

"""
Name:
		user_choice

Description:
		Asks user to select one of the available options, providing the option corresponding index.
		Returns the index of the selected option in the specified input list.

Input arguments:
		options		A list of strings containing all the available options.

		query		The query that should be displayed to the user.

		confirm		A boolean indicating whether the user should confirm the selected value.
"""
def user_choice(options, query, confirm=False):
	
	if len(options) == 0:
		print('Error: in user_choice, options list is empty')
		return

	choice = 0	# choice variable

	choose_again = 1	# init loop key

	while choose_again == 1:

		choose_again = 0

		# display query
		print('\n')
		print(query)

		idx_cnt = 1

		# display options
		for option in options:
			print(str(idx_cnt)+') '+option)
			idx_cnt += 1

		print('\n')

		valid = 0
		while valid != 1:

			# get user option
			sel = raw_input()
			sel = sel.replace("\n","")

			# verify if user selection is valid
			try:
				choice = int(sel)
				if choice < idx_cnt and choice > 0:
					valid = 1
					choice = choice - 1
				else:
					print('Invalid input: Must be an integer from 1 to '+str(idx_cnt-1))
			except:
				print('Invalid input: Must be an integer from 1 to '+str(idx_cnt-1))
				valid = 0
	
		# if confirm argument is 1, ask user for confirmation
		if confirm:
			print('Confirm option as '+options[choice]+'? (y/n)')
		
			valid = 0
			conf = 'n'
			while valid != 1:

				conf = raw_input()
				conf = conf.replace("\n","")
				conf = conf.lower()

				if conf == 'y' or conf == 'yes' or conf == 'n' or conf == 'no':
					valid = 1

			if conf == 'n' or conf == 'no':
				choose_again = 1

	if choice < 0:
		print("Error in function user_choice: index is less than 0")

	return choice
