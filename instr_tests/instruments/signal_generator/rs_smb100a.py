#-----------------------------------------------------------------------------
# Title      : Rohde & Schwarz SMB100A Signal Generator Class
# Project    :
#-----------------------------------------------------------------------------
# File       : rs_smb100a.py
# Author     : Vitor Finotti Ferreira  <vfinotti@finotti-Inspiron-7520>
# Company    : Brazilian Synchrotron Light Laboratory, LNLS/CNPEM
# Created    : 2016-02-29
# Last update: 2016-02-29
# Platform   :
# Standard   : Python 3.4
#-----------------------------------------------------------------------------
# Description:
#
# Defines specific class for Rohde & Schwarz SMb100A Signal Generator using
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
# 2016-feb-29 1.0      vfinotti        Created
#-----------------------------------------------------------------------------

import visa
import time
import numpy as np

# Time to wait after sending an instruction
SLEEP_TIME = 2.0

class RSSMB100A:
    """Class used to send commands and acquire data from the Rohde & Schwarz SMB100A Signal Generator.
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

        sig_gen_ip = ip

        self.sig_gen_socket = rm.open_resource('TCPIP::' + sig_gen_ip + '::inst0::INSTR')


    def query(self, text):
        """Return the output of the query on text"""
        return self.sig_gen_socket.query(text)

    def write(self, text):
        """Sends a command to the instrument."""
        self.sig_gen_socket.write(text)
        time.sleep(SLEEP_TIME)
        return

    def set_frequency(self, freq):
        """set the frequency value"""
        self.sig_gen_socket.write(":SENS:FREQ " + str(freq))
        time.sleep(SLEEP_TIME)
        return

    def set_lfo(self, freq):
        """set the low frequency output"""
        self.sig_gen_socket.write(':LFO:FREQ ' + str(freq))
        self.sig_gen_socket.write(':LFO:FREQ:MODE FIXED')
        self.sig_gen_socket.write(':LFO:STAT ON')
        return

    def set_am(self, stat):
        """set the amplitude modulation output"""
        if stat != 0 and stat != 1 and stat != 'ON' and stat != 'OFF':
            print('State should be 1, 0, \'ON\' or \'OFF\'')
            exit()
        self.sig_gen_socket.write(':AM:STAT ' + str(stat))
        self.sig_gen_socket.write(':AM:SOUR INT')
        self.sig_gen_socket.write(':MOD:STAT ON')
        return

    def set_fm(self, stat):
        """set the frequency modulation output"""
        if stat != 0 and stat != 1 and stat != 'ON' and stat != 'OFF':
            print('State should be 1, 0, \'ON\' or \'OFF\'')
            exit()
        self.sig_gen_socket.write(':FM:STAT ' + str(stat))
        self.sig_gen_socket.write(':FM:SOUR INT')
        self.sig_gen_socket.write(':MOD:STAT ON')
        return

    def set_rf(self, freq, level):
        """set the RF output"""
        self.sig_gen_socket.write(':FREQ ' + str(freq))
        self.sig_gen_socket.write(':POW '+ str(level))
        self.sig_gen_socket.write(':FREQ:MODE FIXED')
        self.sig_gen_socket.write(':OUTP:STAT ON')
        return


    #def close_connection(self):
    #    """Close the socket connection to the instrument."""
    #    self.sig_gen_socket.close()
