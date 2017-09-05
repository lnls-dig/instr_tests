#########################################################################
#
# Name:
#
#	AGILENT 86100D Wide-Bandwidth Oscilloscope Class
#
# Description:
#
#	Class for communicating with Agilent 86100D Oscilloscope.
#
#########################################################################


import visa
import time
import numpy as np
import datetime
import os

class Agilent86100D:
	"""Class for communicating with Agilent 86100D wide-bandwidth oscilloscope.
	"""

	def __init__(self, ip):
		"""Socket initialization."""

		# test if resource managers exists. Create if it doesn't.
		if 'rm' in globals():
			pass
		else:
			global rm
			rm = visa.ResourceManager('@py')

		self.wbo_socket = rm.open_resource('TCPIP::'+ip+'::inst0::INSTR')

	def query(self, text):
		"""Return the output of the query on text"""
		return self.wbo_socket.query(text)

	def write(self, text):
		"""Sends a command to the instrument."""
		self.wbo_socket.write(text)
		return

	def set_operation_complete(self):
		""" Sets the Standard Event Status Register's operation complete bit """
		self.write("*OPC")

	def wait_operation_complete(self):
		""" Holds the GPIB bus until the operations are complete at which time it returns a 1 """
		self.query("*OPC?")

	def view(self, element):
		""" Turns on a channel, function, waveform memory, jitter data memory, TDR response, histogram, or color grade memory. """

		# check element string
		elem_length = len(element)

		if elem_length == 0:
			print("Error in function blank: input string is empty")
			return

		ok = 0 # valid element string flag

		elem_aux = element.lower()
		
		if elem_aux[-1] == '1' or elem_aux[-1] == '2' or elem_aux[-1] == '3' or elem_aux[-1] == '4':

			elem_aux = elem_aux[:-1]

			if elem_aux == 'chan' or elem_aux == 'channel' or elem_aux == 'func' or elem_aux == 'function' or elem_aux == 'wmem' or elem_aux == 'wmemory' or elem_aux == 'resp' or elem_aux == 'response':

				ok = 1

		elif elem_aux == 'jdm' or elem_aux == 'jdmemory' or elem_aux == 'hist' or elem_aux == 'histogram' or elem_aux == 'cgm' or elem_aux == 'cgmemory':
			ok = 1

		# if invalid string
		if ok == 0:
			print("Error in function blank: invalid input argument")
			return

		# turn on element
		self.write(":VIEW "+element)		

	def blank(self, element):
		""" Turns off an active channel, function, waveform memory, jitter data memory, TDR response, histogram, or color 			grade memory. """

		# check element string
		elem_length = len(element)

		if elem_length == 0:
			print("Error in function blank: input string is empty")
			return

		ok = 0 # valid element string flag

		elem_aux = element.lower()
		
		if elem_aux[-1] == '1' or elem_aux[-1] == '2' or elem_aux[-1] == '3' or elem_aux[-1] == '4':

			elem_aux = elem_aux[:-1]

			if elem_aux == 'chan' or elem_aux == 'channel' or elem_aux == 'func' or elem_aux == 'function' or elem_aux == 'wmem' or elem_aux == 'wmemory' or elem_aux == 'resp' or elem_aux == 'response':

				ok = 1

		elif elem_aux == 'jdm' or elem_aux == 'jdmemory' or elem_aux == 'hist' or elem_aux == 'histogram' or elem_aux == 'cgm' or elem_aux == 'cgmemory':
			ok = 1

		# if invalid string
		if ok == 0:
			print("Error in function blank: invalid input argument")
			return

		# turn off element
		self.write(":BLANk "+element)

	def digitize(self, source=''):
		""" Invokes a special mode of data acquisition that is more efficient than using the RUN command when using averaging 			in the Oscilloscope mode. If you use the DIGitize command with no parameters, the digitize operation is performed on 			the channels or functions that were acquired with a previous digitize, run, or single operation. """

		sources = source.lower().replace(" ","").split(",")

		# check if argument is valid
		for s in sources:
			if not (s == '' or s[-1] == '1' or s[-1] == '2' or s[-1] == '3' or s[-1] == '4'):
				print("Error in function digitize: invalid input argument")
			if not (s[:-1] == 'chan' or s[:-1] == 'channel' or s[:-1] == 'func' or s[:-1] == 'function' or s[:-1] == 'resp' or s[:-1] == 'response'):
				print("Error in function digitize: invalid input argument")			

		# request digitize
		if source == '':
			self.write(":DIGitize")
		else:
			self.write(":DIGitize "+source)

	def run(self, channel=''):
		""" Starts the instrument running where the instrument acquires waveform data according to its current settings. 			Acquisition runs repetitively until the analyzer receives a correspondent STOP command. In TDR mode (software revision 			A.06.00 and above), the optional channel argument is not allowed. """

		# if no channel
		if channel == '':
			self.write(":RUN")
			return

		# check if channel is valid
		channel = channel.lower()

		if (channel[-1] == '1' or channel[-1] == '2' or channel[-1] == '3' or channel[-1] == '4') and (channel[:-1] == 'chan' or channel[:-1] == 'channel'):			
			# run
			self.write(":RUN "+channel)
		else:
			print("Error in function run: invalid input argument")
			return

	def stop(self, channel=''):
		""" Stops data acquisition for the active display. If no channel is specified, all active channels are affected. In 			TDR mode (software revision A.06.00 and above), the optional channel argument is not allowed. """

		# if no channel
		if channel == '':
			self.write(":STOP")
			return

		# check if channel is valid
		channel = channel.lower()

		if (channel[-1] == '1' or channel[-1] == '2' or channel[-1] == '3' or channel[-1] == '4') and (channel[:-1] == 'chan' or channel[:-1] == 'channel'):			
			# run
			self.write(":STOP "+channel)
		else:
			print("Error in function stop: invalid input argument")
			return

	def store_waveform(self, source='', dest=''):
		""" Copies a channel, function, stored waveform, or TDR response to a waveform memory or to color grade memory. The first parameter specifies the source. The second parameter is the destination, and can be any waveform memory. """

		if source == '':
			print("Error in function store_waveform: source string is empty")
			return
		if dest == '':
			print("Error in function store_waveform: destination string is empty")
			return

		source = source.lower()
		dest = dest.lower()

		# check source
		if source[-1] != '1' and source[-1] != '2' and source[-1] != '3' and source[-1] != '4':
			print("Error in function store_waveform: invalid source argument")
			return
		if source[:-1] != 'chan' and source[:-1] != 'channel' and source[:-1] != 'func' and source[:-1] != 'function' and source[:-1] != 'wmem' and source[:-1] != 'wmemory' and source[:-1] != 'resp' and source[:-1] != 'response':
			print("Error in functin store_waveform: invalid source argument")
			return

		# check destination
		if dest != "cgm" and dest != "cgmemory" and dest[-1] != '1' and dest[-1] != '2' and dest[-1] != '3' and dest[-1] != '4':
			print("Error in function store_waveform: invalid source argument")
			return
		if dest[:-1] != "wmem" and dest[:-1] != "wmemory":
			print("Error in function store_waveform: invalid destination argument")
			return

		# store waveform
		self.write(":STORe:WAVeform "+source+','+dest)

	def get_next_error(self):
		""" Returns the next error number and string in the error queue """

		return self.query(":SYSTEM:ERROR? STRING")

	def set_mode(self, mode):
		""" Sets the system mode. If a TDR/TDT module is present, changing to TDR/TDT mode using this command turns on 			averaging for both TDR/TDT and Oscilloscope modes. """

		mode = mode.lower()

		# check mode argument
		if mode != 'eye' and mode != 'osc' and mode != 'oscilloscope' and mode != 'tdr' and mode != 'jitt' and mode != 'jitter':
			print("Error in function set_mode: invalid input argument")
			return

		# set mode
		self.write(":SYSTem:MODE "+mode)

	def get_mode(self):
		""" Returns the system mode. """

		return self.query(":SYSTem:MODE?")

	def set_average_state(self, state):
		""" Enables or disables averaging. When ON, the analyzer acquires multiple data values for each time bucket, and 			averages them. """

		# check input argument
		if state != '1' or state != '0' or state.lower() != 'on' or state.lower() != 'off':
			print("Error in set_average: invalid input argument")
			return

		# set average
		self.write(":ACQuire:AVERage "+state)

	def get_average_state(self):
		""" Returns 1 if averaging is enabled, otherwise returns 0. """

		return self.query(":ACQuire:AVERage?")

	def set_best(self, option):
		""" When averaging is enabled with ACQuire:AVERage, the FLATness option improves the step flatness by using a signal 			processing algorithm within the instrument. You should use this option when performing TDR measurements or when step 			flatness is important. The THRuput option improves the instrument's throughput and should be used whenever best 		flatness is not required. """

		option = option.lower()

		# check input argument
		if option != 'thr' and option != 'thruput' and option != 'flat' and option != 'flatness':
			print("Error in function set_best: invalid input argument")
			return

		# set best
		self.write(":ACQuire:BEST "+option)

	def get_best(self):
		""" Returns the BEST parameter state. """

		return self.query(":ACQuire:BEST?")

	def set_count(self, count):
		""" Sets the number of averages for the waveforms. In the AVERage mode, the ACQuire:COUNt command specifies the 		number of data values to be averaged for each time bucket before the acquisition is considered complete for that time 			bucket. The value is an integer from 1 to 4096. """

		# check input argument
		try:
			count = int(count)
			if count < 1 or count > 4096:
				print("Error in function set_count: input argument out of range")
				return
		except:
			print("Error in function set_count: invalid input argument")

		# set count
		self.write(":ACQuire:COUNt "+str(count))

	def get_count(self):
		""" Returns the number of averages for the waveform. """

		return self.query(":ACQuire:COUNt?")

	def set_acquisition_points(self, points):
		""" Sets the requested memory depth for an acquisition. The points value range is 16 to 16,384 points. You can set 			the points value to AUTO, which allows the analyzer to select the number of points based upon the sample rate and 			time base scale. """

		# checke input argument
		if points.lower() != 'auto':
			points = int(points)
			if points < 16 or points > 16384:
				print("Error in function set_acquisition_points: invalid input argument")
				return

		# set points
		self.write(":ACQuire:POINts "+str(points))

	def get_acquisition_points(self):
		""" Returns the configured memory depth for acquisitions. """

		return self.query(":ACQuire:POINts?")

	def set_runtil(self, option, count, channel=''):
		""" Selects the acquisition run until mode.  """

		option = option.lower()
		count = int(count)
		channel = channel.lower()

		# check input arguments
		if option != 'off' and option != 'wav' and option != 'waveforms' and option != 'samp' and option != 'samples' and option != 'patt' and option != 'patterns':
			print("Error in function set_runtil: invalid option argument")
			return

		if channel[-1] != '1' and channel[-1] != '2' and channel[-1] != '3' and channel[-1] != '4' and channel != 'off':
			print("Error in function set_runtil: invalid channel argument")
			return
			
		if channel[:-1] != 'chan' and channel[:-1] != 'channel' and channel != 'off':
			print("Error in function set_runtil: invalid channel argument")
			return

		# set runtil
		self.write(":ACQuire:RUNTil "+option+","+count+","+channel)
			
	def get_runtil(self, channel=''):
		""" Returns the currently selected run until state. If the channel parameter is specified, the run until state of the 			specified channel is returned. """

		if channel[-1] != '1' and channel[-1] != '2' and channel[-1] != '3' and channel[-1] != '4' and channel != 'off':
			print("Error in function set_runtil: invalid channel argument")
			return
			
		if channel[:-1] != 'chan' and channel[:-1] != 'channel' and channel != 'off':
			print("Error in function set_runtil: invalid channel argument")
			return

		return self.query(":ACQuire:RUNTil? "+channel)

	def set_source(self, src1, src2=''):
		""" Selects the source for measurements. You can specify one or two sources with this command. """

		src1 = src1.lower()
		src2 = src2.lower()
		src = [src1, src2]

		# check input arguments
		for i in range(0,2):
			if not (i == 1 and src[i] == ''):
				if src[i][-1] != '1' and src[i][-1] != '2' and src[i][-1] != '3' and src[i][-1] != '4':
					print("Error in function set_source: invalid input argument")
					return

				if src[i][:-1] != 'chan' and src[i][:-1] != 'channel' and src[i][:-1] != 'func' and src[i][:-1] != 'function' and src[i][:-1] != 'resp' and src[i][:-1] != 'response' and src[i][:-1] != 'wmem' and src[i][:-1] != 'wmemory':

					print("Error in function set_source: invalid input argument")
					return

		# set source
		if src2 != '':
			self.write(":MEASure:SOURce "+src1+","+src2)
		else:
			self.write(":MEASure:SOURce "+src1)

	def get_source(self):
		""" Returns the source for measurements. """

		return self.query(":MEASure:SOURce?")

	def get_edge_time(self, thres, slope='+', occurrence=1, source=''):
		""" Returns the time interval between the trigger event and the specified edge (threshold level, slope, and 			transition) in oscilloscope mode. """

		if slope == '':
			slope = '+'

		thres = thres.lower()
		occurrence = int(occurrence)

		# check input arguments
		if thres != 'upp' and thres != 'upper' and thres != 'midd' and thres != 'middle' and thres != 'low' and thres != 'lower':
			print("Error in function get_edge_time: invalid input argument")
			return

		if slope != '+' and slope != '-':
			print("Error in function get_edge_time: invalid input argument")
			return

		if occurrence < 1:
			print("Error in function get_edge_time: invalid input argument")
			return

		if source != '' and source[-1] != '1' and source[-1] != '2' and source[-1] != '3' and source[-1] != '4':
			print("Error in function get_edge_time: invalid input argument")
			return

		if source != '' and source[:-1] != 'chan' and source[:-1] != 'channel' and source[:-1] != 'func' and source[:-1] != 'function' and source[:-1] != 'resp' and source[:-1] != 'response' and source[:-1] != 'wmem' and source[:-1] != 'wmemory':

			print("Error in function get_edge_time: invalid input argument")
			return

		# get edge time
		if source != '':
			self.query(":MEASure:TEDGe? "+thres+","+slope+occurrence+","+source)
		else:
			self.query(":MEASure:TEDGe? "+thres+","+slope+occurrence)

	def get_time_max(self, source):
		""" Measures the first time at which the first maximum voltage of the source waveform occurred. The source is 			specified with the MEASure:SOURce command or with the optional parameter following the TMAX command. In TDR mode, the 			time reported is measured with respect to the reference plane. """

		source = source.lower()

		# check input arguments
		if source[-1] != '1' and source[-1] != '2' and source[-1] != '3' and source[-1] != '4':
			print("Error in function get_time_max: invalid input argument")
			return

		if source[:-1] != 'chan' and source[:-1] != 'channel' and source[:-1] != 'func' and source[:-1] != 'function' and source[:-1] != 'resp' and source[:-1] != 'response' and source[:-1] != 'wmem' and source[:-1] != 'wmemory':

			print("Error in function get_time_max: invalid input argument")
			return

		# get maximum value time
		self.query(":MEASure:TMAX "+source)

	def get_time_min(self, source):
		""" Measures the first time at which the first minimum voltage of the source waveform occurred. The source is 			specified with the MEASure:SOURce command or with the optional parameter following the TMIN command. In TDR mode, the 			time reported is measured with respect to the reference plane. """

		source = source.lower()

		# check input arguments
		if source[-1] != '1' and source[-1] != '2' and source[-1] != '3' and source[-1] != '4':
			print("Error in function get_time_min: invalid input argument")
			return

		if source[:-1] != 'chan' and source[:-1] != 'channel' and source[:-1] != 'func' and source[:-1] != 'function' and source[:-1] != 'resp' and source[:-1] != 'response' and source[:-1] != 'wmem' and source[:-1] != 'wmemory':

			print("Error in function get_time_min: invalid input argument")
			return

		# get minimum value time
		self.query(":MEASure:TMIN "+source)

	def get_time_volt(self, volt, slope='+', occurrence=1, source=''):
		""" Returns the time interval between the trigger event and the specified voltage level and transition (oscilloscope 			mode) or the time interval between the reference plane and the specified voltage level and transition (TDR mode). """

		if slope == '':
			slope = '+'
		
		occurrence = int(occurrence)
		source = source.lower()

		# check input arguments
		if occurrence < 1:
			print("Error in function get_time_volt: invalid input argument")
			return

		if slope != '+' and slope != '-':
			print("Error in function get_time_volt: invalid input argument")
			return			

		if source != '' and source[-1] != '1' and source[-1] != '2' and source[-1] != '3' and source[-1] != '4':
			print("Error in function get_time_volt: invalid input argument")
			return

		if source != '' and source[:-1] != 'chan' and source[:-1] != 'channel' and source[:-1] != 'func' and source[:-1] != 'function' and source[:-1] != 'resp' and source[:-1] != 'response' and source[:-1] != 'wmem' and source[:-1] != 'wmemory':
			print("Error in function get_time_volt: invalid input argument")
			return

		# get specified voltage time
		if source != '':
			self.query(":MEASure:TVOLt? "+volt+","+slope+occurrence+","+source)
		else:
			self.query(":MEASure:TVOLt? "+volt+","+slope+occurrence)
	
#####################################################
#
#		TDR Sub-system
#
#####################################################

	def set_tdr_connect(self, channel, port):
		""" Enters the measurement setup connections between the instrument channels and the test device ports. Use the NONE 			argument to delete a previously established connection. """

		channel = channel.lower()
		port = port.lower()

		# check input arguments
		if channel == '' or port == '':
			print("Error in function set_tdr_connect: invalid input argument")
			return

		if channel[-1] != '1' and channel[-1] != '2' and channel[-1] != '3' and channel[-1] != '4':
			print("Error in function set_tdr_connect: invalid input argument")
			return

		if channel[:-1] != 'chan' and channel[:-1] != 'channel':
			print("Error in function set_tdr_connect: invalid input argument")
			return

		if port != 'none' and port[-1] != '1' and port[-1] != '2' and port[-1] != '3' and port[-1] != '4':
			print("Error in function set_tdr_connect: invalid input argument")
			return

		if port != 'none' and port[:-1] != 'dutp' and port[:-1] != 'dutport':
			print("Error in function set_tdr_connect: invalid input argument")
			return

		# connect TDR
		self.write(":TDR:CONNect "+channel+","+port)

	def get_tdr_connect(self, channel):
		""" Returns the measurement setup connections between the instrument channels and the test device ports. """

		channel = channel.lower()

		# check input arguments
		if channel[-1] != '1' and channel[-1] != '2' and channel[-1] != '3' and channel[-1] != '4':
			print("Error in function get_tdr_connect: invalid input argument")
			return

		if channel[:-1] != 'chan' and channel[:-1] != 'channel':
			print("Error in function get_tdr_connect: invalid input argument")
			return

		return self.query(":TDR:CONNect? "+channel)

	def set_dut_direction(self, direction):
		""" Selects the direction of the stimulus through the test device: forward or reverse. """

		direction = direction.lower()

		# check input argument
		if direction != 'forw' and direction != 'forward' and direction != 'rev' and direction != 'reverse':
			print("Error in function set_dut_direction: invalid input argument")
			return

		# set DUT direction
		self.write(":TDR:DUT:DIRection "+direction)

	def get_dut_direction(self):
		""" Returns the direction of the stimulus through the test device. """
	
		return self.query(":TDR:DUT:DIR?")

	def set_dut_type(self, dut_type):
		""" Selects the type of device that you are measuring. """

		dut_type = dut_type.lower()

		# check input argument
		if dut_type != 'd1p' and dut_type != 'd1port' and dut_type != 'd2p' and dut_type != 'd2port' and dut_type != 'd2pt' and dut_type != 'd2pthru' and dut_type != 'd4p' and dut_type != 'd4port':
			print("Error in function set_dut_type: invalid input argument")
			return			

		# set DUT type
		self.write(":TDR:DUT:TYPE "+dut_type)

	def get_dut_type(self):
		""" Returns the configured type of device for measurement. """

		return self.query(":TDR:DUT:TYPE?")

	def set_response_display(self, response, option):
		""" Turns on or off the display of the indicated response waveform. <response> identifies the response waveform. """

		# check input argument
		response = str(response)
		option = srt(option)

		if response != '1' and response != '2' and response != '3' and response != '4':
			print("Error in function set_response_display: invalid input argument")
			return

		if option != '1' and option != '0' and option != 'on' and option != 'off':
			print("Error in function set_response_display: invalid input argument")
			return

		# set display of response <n>
		self.write(":TDR:RESPonse"+response+":DISPlay "+option)

	def get_response_display(self, response):
		""" Returns the display state of the specified response waveform. """

		# check input arguments
		response = str(response)

		if response != '1' and response != '2' and response != '3' and response != '4':
			print("Error in function get_response_display: invalid input argument")
			return

		# get display state of response <n>
		self.query(":TDR:RESPonse"+response+":DISPlay?")

	def set_response_risetime(self, risetime):
		""" Specifies the response risetime setting in seconds. """

		risetime = float(risetime)

		self.write(":TDR:RESPonse1:RISetime "+risetime) # the specified response does not matter, since this setting applies to all responses

	def get_response_risetime(self):
		""" Returns the response risetime setting in seconds. """

		return self.query(":TDR:RESPonse1:RISetime?") # the specified response does not matter, since this setting applies to all responses

	def get_response_refplane(self, response):
		""" Queries the reference plane position for TDR or TDT responses. """

		# check input argument
		if response != '1' and response != '2' and response != '3' and response != '4':
			print("Error in function get_response_refplane: invalid input argument")
			return

		return self.query(":TDR:RESPonse"+response+":RPLane?")

	def set_response_type(self, response, resp_type):
		""" Specifies the response type. """

		resp_type = resp_type.lower()

		# check input argument
		if resp_type != 'csin' and resp_type != 'csingle' and resp_type != 'cdif' and resp_type != 'cdiff' and resp_type != 'ccom' and resp_type != 'ccommon' and resp_type != 'udif' and resp_type != 'udiff' and resp_type != 'ucom' and resp_type != 'ucommon':
			print("Error in function set_response_type: invalid input argument")
			return

		if response != '1' and response != '2' and response != '3' and response != '4':
			print("Error in function set_response_type: invalid input argument")
			return

		# set response type
		self.write(":TDR:RESPonse"+response+":TYPE "+resp_type)

	def get_response_type(self, response):
		""" Return the type of response for the specified response index. """

		return self.query(":TDR:RESPonse"+response+":TYPE?")

	def set_response_stimulus_mode(self, mode):
		""" Sets the measurement stimulus to single-ended, differential, or common mode. """

		mode = mode.lower()

		# check input argument
		if mode != 'sing' and mode != 'single' and mode != 'diff' and mode != 'differential' and mode != 'comm' and mode != 'common':
			print("Error in function set_response_stimulus_mode: invalid input argument")
			return

		# set mode
		self.write(":TDR:STIMulus:MODE "+mode)

	def get_response_stimulus_mode(self):
		""" Returns the measurement stimulus. """

		return self.query(":TDR:STIMulus:MODE?")

	def set_response_stimulus_state(self, stim, state):
		""" Turns on and off the selected stimulus. """

		stim = stim.lower()
		state = state.lower()

		# check input argument
		if stim == '' or state == '':
			print("Error in function set_response_stimulus_state: invalid input string")

		if stim[-1] == '1' or stim[-1] == '2' or stim[-1] == '3' or stim[-1] == '4':
			if stim[:-1] != 'chan' and stim[:-1] != 'channel':
				print("Error in function set_response_stimulus_state: invalid input argument")
				return
		elif stim != 'lmod' and stim != 'lmodule' and stim != 'rmod' and stim != 'rmodule':
				print("Error in function set_response_stimulus_state: invalid input argument")
				return

		if state != 'off' and state != 'on' and state != '1' and state != 'off':
				print("Error in function set_response_stimulus_state: invalid input argument")
				return

		# set stimulus state
		self.write(":TDR:STIMulus:STATe "+stim+","+state)

	def get_response_stimulus_state(self):
		""" Returns the TDR stimulus state. """

		return self.query(":TDR:STIMulus:STATe?")

#####################################################
#
#		Waveform Sub-system
#
#####################################################

#	def get_waveform_count
	def set_waveform_format(self, data_format):
		""" Sets the data transmission mode for waveform data output. The default is ASCii. """

		# check input argument
		if data_format != 'ASCii' and data_format != 'BYTE' and data_format != 'LONG' and data_format != 'WORD':
			print("Error in function set_waveform_format: invalid input argument")
			return

		# set format
		self.write(":WAVeform:FORMat "+data_format)

	def get_waveform_format(self):
		""" Returns the data transmission mode for waveform data output. """

		return self.query(":WAVeform:FORMat?")

	def get_waveform_points(self):
		""" Returns the points value in the current waveform preamble. The points value is the number of time buckets 			contained in the waveform selected with the WAVeform:SOURce command. """

		return self.query(":WAVeform:POINts?")

	def set_waveform_source(self, source):
		""" Selects a channel, function, TDR response, waveform memory, histogram, or color grade/gray scale as the waveform 			source. """

		source = source.lower()

		# check input argument
		if source[-1] == '1' or source[-1] == '2' or source[-1] == '3' or source[-1] != '4':
			if source != 'wmem' and source != 'wmemory' and source != 'func' and source != 'function' and source != 'chan' and source != 'channel' and source != 'resp' and source != 'response':
				print("Error in function set_waveform_soure: invalid input argument")
				return
		else:
			if source != 'hist' and source != 'histogram' and source != 'cgr' and source != 'cgrade':
				print("Error in function set_waveform_soure: invalid input argument")
				return

		# set source
		self.write(":WAVeform:SOURce "+source)

	def get_waveform_source(self):
		""" Returns the waveform source. """

		return self.query(":WAVeform:SOURce?")

#####################################################
#
#		Waveform Memory Sub-system
#
#####################################################

	
