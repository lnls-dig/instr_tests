#-----------------------------------------------------------------------------
# Title      : Beam Position Monitor AFC v3_1 Class
# Project    :
#-----------------------------------------------------------------------------
# File       : afc_v3_1.py
# Author     : Vitor Finotti Ferreira  <vfinotti@finotti-Inspiron-7520>
# Company    : Brazilian Synchrotron Light Laboratory, LNLS/CNPEM
# Created    : 2016-03-16
# Last update: 2016-03-16
# Platform   :
# Standard   : Python 3.4
#-----------------------------------------------------------------------------
# Description:
#
# Defines specific class for LNLS BPM AFC v3.1 using EPICS
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
# 2016-mar-16 1.0      vfinotti        Created
#-----------------------------------------------------------------------------

import epics
import time
import numpy as np

# Time to wait after sending an instruction
SLEEP_TIME = 2.0


class AFC_v3_1_epics:
    """Class used to send commands and acquire data from the LNLS BPM AFC v3.1 using PyEpics.
    """

    def __init__(self, idn):
        """Class constructor. Here the socket connection to the instrument is initialized. The
        argument required, a string, is the IP adress of the instrument.

        "idn" is the identification of the device, and should be a unique string that identifies
        the device.

        e.g. in the "DIG-RSSMX100A-0:STATUS:Freq_RBV" process variable, "DIG-RSSMX100A-0:STATUS"
        is the "idn".

        """


        self.bpm_idn = idn

    def caput(self, variable_raw, value):
        """use caput to set a given variable to a given value"""

        if variable_raw[0] == ":":
            variable = variable_raw
        else:
            variable = ":" + variable_raw

        epics.caput(self.bpm_idn + variable, value)
        time.sleep(SLEEP_TIME)
        return

    def caget(self, variable_raw):
        """use caget to get a given variable"""

        if variable_raw[0] == ":":
            variable = variable_raw
        else:
            variable = ":" + variable_raw

        return epics.caget(self.bpm_idn + variable)


    def config_acq(self, samplesPre, samplesPost, shots, channel, trigger):
        """ Configures the BPM for data acquisition
        """

        epics.caput(self.bpm_idn + ':ACQ:samplesPre', samplesPre) # number of samples
        epics.caput(self.bpm_idn + ':ACQ:samplesPost', samplesPost)
        epics.caput(self.bpm_idn + ':ACQ:shots', shots) # number of shots taken
        epics.caput(self.bpm_idn + ':ACQ:channel', channel) # adc/fofb/tbt
        epics.caput(self.bpm_idn + ':ACQ:trigger', trigger)
        return

    def get_arraydata(self, channel, num_samples):
        if channel.upper() != 'A' and channel.upper() != 'B' and channel.upper() != 'C' and channel.upper() != 'D':
            print('Channel should be A, B, C or D')
            exit()
        return epics.caget(self.bpm_idn + ':ADC_'+str(channel.upper())+':ArrayData')[:num_samples] # get only "num_samples" samples
