#-----------------------------------------------------------------------------
# Title      : Agilent E5061B Network Analyzer Class
# Project    :
#-----------------------------------------------------------------------------
# File       : agilent_e5061b.py
# Author     : Vitor Finotti Ferreira  <vfinotti@finotti-Inspiron-7520>
# Company    : Brazilian Synchrotron Light Laboratory, LNLS/CNPEM
# Created    : 2016-02-23
# Last update: 2016-02-23
# Platform   :
# Standard   : Python 3.4
#-----------------------------------------------------------------------------
# Description:
#
# Defines specific class for the Agilent E5061B Network Analyzer using
# VXI-11 protocol with PyVisa and PyVisa-py
#-----------------------------------------------------------------------------
# Copyright (c) 2016 Brazilian Synchrotron Light Laboratory, LNLS/CNPEM
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program. If not, see
# <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------
# Revisions  :
# Date        Version  Author          Description
# 2016-feb-23 1.0      vfinotti        Created
#-----------------------------------------------------------------------------


# define specific class for Agilent E5061B Network Analyzer

import visa
import time
import numpy as np

# Time to wait after sending an instruction
SLEEP_TIME = 2.0

class AgilentE5061B:
    """Class used to send commands and acquire data from the Agilent E5061B vector network analyzer.
    """

    def __init__(self, ip):
        """Class constructor. Here the socket connection to the instrument is initialized. The
        argument required, a string, is the IP adress of the instrument."""

        # test if resource managers exists. Create if it doesn't.
        if 'rm' in globals():
            pass
        else:
            global rm
            rm = visa.ResourceManager('@py')

        vna_ip = ip

        self.vna_socket = rm.open_resource('TCPIP::' + vna_ip + '::inst0::INSTR')

        self.vna_socket.write(":SYST:PRES")
        self.vna_socket.write(":DISP:WIND1:TRAC1:Y:RLEV -40")
        self.vna_socket.write(":DISP:WIND1:TRAC1:Y:PDIV 15")
        self.vna_socket.write(":SENS1:SWE:TIME:AUTO ON")
        self.vna_socket.write(":SENS1:SWE:POIN 1601")
        self.vna_socket.write(":SENS1:SWE:TYPE LIN")
        self.vna_socket.write(":SOUR1:POW:GPP 0.0")


    def query(self, text):
        """Return the output of the query on text"""
        return self.vna_socket.query(text)

    def write(self, text):
        """Sends a command to the instrument."""
        self.vna_socket.write(text)
        time.sleep(SLEEP_TIME)
        return

    def get_frequency_data(self):
        """Get the list of frequencies of the instrument sweep, returning a sequence of floating
           point numbers."""
        frequency_data = self.vna_socket.query(":SENS1:FREQ:DATA?")
        frequency_data = frequency_data[:len(frequency_data) - 1].split(",")
        frequency_data = [float(i) for i in frequency_data]
        return(frequency_data)

    def get_s11_data(self):
        """Get the S11 trace data, returning a sequence of floating point numbers."""
        self.vna_socket.write(":CALC1:PAR1:DEF S11")
        time.sleep(SLEEP_TIME)
        s11_data = self.vna_socket.query(":CALC1:DATA:FDAT?")
        s11_data = s11_data[:len(s11_data) - 1].split(",")
        s11_data = s11_data[::2]
        s11_data = [round(float(i),2) for i in s11_data]
        return(s11_data)

    def get_s12_data(self):
        """Get the S12 trace data, returning a sequence of floating point numbers."""
        self.vna_socket.write(":CALC1:PAR1:DEF S12")
        time.sleep(SLEEP_TIME)
        s12_data = self.vna_socket.query(":CALC1:DATA:FDAT?")
        s12_data = s12_data[:len(s12_data) - 1].split(",")
        s12_data = s12_data[::2]
        s12_data = [round(float(i),2) for i in s12_data]
        return(s12_data)

    def get_s21_data(self):
        """Get the S21 trace data, returning a sequence of floating point numbers."""
        self.vna_socket.write(":CALC1:PAR1:DEF S21")
        time.sleep(SLEEP_TIME)
        s21_data = self.vna_socket.query(":CALC1:DATA:FDAT?")
        s21_data = s21_data[:len(s21_data) - 1].split(",")
        s21_data = s21_data[::2]
        s21_data = [round(float(i),2) for i in s21_data]
        return(s21_data)

    def get_s22_data(self):
        """Get the S22 trace data, returning a sequence of floating point numbers."""
        self.vna_socket.write(":CALC1:PAR1:DEF S22")
        time.sleep(SLEEP_TIME)
        s22_data = self.vna_socket.query(":CALC1:DATA:FDAT?")
        s22_data = s22_data[:len(s22_data) - 1].split(",")
        s22_data = s22_data[::2]
        s22_data = [round(float(i),2) for i in s22_data]
        return(s22_data)

    def set_marker_frequency(self,value):
        """set the center frequency of the VNA"""
        self.vna_socket.write(":CALC1:MARK1:X " + str(value))
        time.sleep(SLEEP_TIME)
        return

    def get_marker_value(self,marker):
        """get the value of the marker 1 """
        #self.vna_socket.write(":CALC1:MARK" + str(marker) + ":Y?")
        #ans= self.vna_socket.read_raw()
        ans = self.vna_socket.query(":CALC1:MARK" + str(marker) + ":Y?")
        index = ans.find(',')
        ans = ans[:index].strip()
        return(ans)

    def set_center_frequency(self, freq):
        """set the center frequency of the VNA"""
        self.vna_socket.write(":SENS1:FREQ:CENT " + str(freq))
        time.sleep(SLEEP_TIME)
        return

    def set_span(self,freq):
        """set the span of the VNA"""
        self.vna_socket.write(":SENS1:FREQ:SPAN " + str(freq))
        time.sleep(SLEEP_TIME)
        return

    def set_power(self, power):
        self.vna_socket.write(":SOUR1:POW:GPP " + str(power))
        time.sleep(SLEEP_TIME)
        return

    def freq_range(self, start, stop):
        """set the start and stop frequencies of the windows"""
        self.vna_socket.write(':SENS:FREQ:START ' + str(start))
        time.sleep(SLEEP_TIME)
        self.vna_socket.write(':SENS:FREQ:STOP ' + str(stop))
        time.sleep(SLEEP_TIME)
        return

    def get_reflection_impedance(self):
        self.vna_socket.write(":CALC1:PAR1:DEF S11")
        time.sleep(SLEEP_TIME)
        self.vna_socket.write(':CALC1:FORM SMIT')
        time.sleep(SLEEP_TIME)
        z_data = self.vna_socket.query(":CALC1:DATA:FDAT?")
        z_data = z_data[:len(z_data) - 1].split(",")
        z_data = [round(float(i),2) for i in z_data]
        z_data = [np.mean(z_data[0:len(z_data):2]), np.mean(z_data[1:len(z_data):2])]
        return(z_data)

    def save_csv(self, file_name):
        """ Save data in a CSV file inside in the directory D:\instr_tests_csv\ """
        self.vna_socket.write("MMEM:MDIR \"d:\instr_tests_csv\"")
        time.sleep(SLEEP_TIME)
        self.vna_socket.write("MMEM:STOR:FDAT \"d:\instr_tests_csv\\" + file_name + ".csv\"")
        time.sleep(SLEEP_TIME)

    def set_data_format(self, data_format):
        """ Set data display format. It can be:

        - "MLOGarithmic": Specifies the log magnitude format.
        - "PHASe": Specifies the phase format.
        - "GDELay": Specifies the group delay format.
        - "SLINear": Specifies the Smith chart format (Lin/Phase).
        - "SLOGarithmic": Specifies the Smith chart format (Log/Phase).
        - "SCOMplex": Specifies the Smith chart format (Re/Im).
        - "SMITh": Specifies the Smith chart format (R+jX).
        - "SADMittance": Specifies the Smith chart format (G+jB).
        - "PLINear": Specifies the polar format (Lin/Phase).
        - "PLOGarithmic": Specifies the polar format (Log/Phase).
        - "POLar": Specifies the polar format (Re/Im).
        - "MLINear": Specifies the linear magnitude format.
        - "SWR": Specifies the SWR format.
        - "REAL": Specifies the real format.
        - "IMAGinary": Specifies the imaginary format.
        - "UPHase": Specifies the expanded phase format.
        - "PPHase": Specifies the positive phase format."""

        self.vna_socket.write(":CALC1:FORM " + data_format)

        value = self.vna_socket.query(":CALC1:FORM?")
        value = value[:len(value)-1] # removing the \n character

        # Checking if the current value and expected value are the same
        if value != data_format[:len(value)]:
            print("Error while setting the data format!")
            print("Current value: " + value)
            print("Expected value: " + data_format[:len(value)])

    #def close_connection(self):
    #    """Close the socket connection to the instrument."""
    #    self.vna_socket.close()
