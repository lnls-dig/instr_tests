#-----------------------------------------------------------------------------
# Title      : VNA Magnitude Level Test Function
# Project    :
#-----------------------------------------------------------------------------
# File       : mag_lvl_test.py
# Author     : Vitor Finotti Ferreira  <vfinotti@finotti-Inspiron-7520>
# Company    : Brazilian Synchrotron Light Laboratory, LNLS/CNPEM
# Created    : 2016-02-23
# Last update: 2016-02-23
# Platform   :
# Standard   : Python 3.4
#-----------------------------------------------------------------------------
# Description:
#
# Receives 'x' (frequency) and 'y' (magnitude) data from a Network Analyzer.
# Then, the 3 arrays are given:
# - zone_freq = array with N elements containing the frequencies that surrounds
#               the intervals where the magnitude level will be tested.
#               (e.g. zone_freq = [0, 140, 1000, 1500, 2000, 3000])
#
# - zone_type = array with N-1 elements stating if the respective manitude in
#               zone_mag will be the maximum in the interval (1), the minimun
#               in the interval (-1) or if it doesn't matter (0).
#               (e.g. zone_type = [-1,0,1,0,-1])
#
#
# - zone_mag  = array with N-1 elements stating the manitude of the frequency
#               interval, usually in dB
#               (e.g. zone_mag = [-40,0,-10,0,-40])
#
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

import numpy as np
import math


def mag_lvl_test(x, y, zone_freq, zone_type, zone_mag):

    index_nearest = find_index_nearest(x, zone_freq)

    # test for each zone
    for i in range(len(index_nearest)-1):
        bot = index_nearest[i]
        top = index_nearest[i+1] + 1 # added 1 to eval last element of y array
        if zone_type[i] == -1:
            if max(y[bot:top]) > zone_mag[i]:
                return False
        elif zone_type[i] == 1:
            if min(y[bot:top]) < zone_mag[i]:
                return False
        elif zone_type[i] == 0:
            pass
        else:
            print("\nZone type must be -1, 0 or 1\n")
            exit()

    return True


def find_index_nearest(array,value):
    """find index of nearest element in array of each element in value"""
    nearest = []
    for i in value:
        idx = np.searchsorted(array, i, side="left")
        if math.fabs(i - array[idx-1]) < math.fabs(i - array[idx]):
            nearest.append(idx-1)
        else:
            nearest.append(idx)
    return nearest
