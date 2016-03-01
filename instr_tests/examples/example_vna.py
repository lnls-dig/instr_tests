#!/usr/bin/python3

import sys
import os
import inspect
import visa

import matplotlib.pyplot as pyplot
import skrf as rf

cmd_folder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../")))


if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

#############################
# Importing local libraries #
#############################

from instruments.vna.agilent_e5061b import AgilentE5061B
from functions.vna.mag_lvl_test import mag_lvl_test


try:
    vna = AgilentE5061B("10.0.18.54")
except:
    sys.stdout.write("\nUnable to reach the vector network analyzer (Agilent E5061B) through the " +
                     "network. Exiting...\n\n")
    exit()

sys.stdout.write("\nRunning test...\n\n")


#vna.freq_range(100000,1e9)
#vna.set_center_frequency(500e6)
#vna.set_span(0)

vna.set_data_format("SLOG")
vna.write("SENS1:CORR:STAT 1")
vna.freq_range(5e6,550e6)

slog = (vna.get_slog_data())
freq = vna.get_frequency_data()
pyplot.plot(freq,slog[1])
pyplot.savefig('wave1.png')

#zone_freq = [100e3, 200e6, 450e6, 550e6, 800e6, 1e9]
#zone_type = [-1, 0, 1, 0, -1]
#zone_mag = [-60, 0, -60, 0,-40]

#print(mag_lvl_test(freq,s21, zone_freq, zone_type, zone_mag))
#print(vna.get_reflection_impedance())

#vna.save_csv("SLOG_s11")
vna.save_s1p("S","dB", "test_file")

ntwk = rf.Network('test_file.s1p')

ntwk.plot_s_smith()
pyplot.savefig('smith.png')

pyplot.close()
ntwk.plot_s_complex()
pyplot.savefig('complex.png')

pyplot.close()
ntwk.plot_s_db()
pyplot.savefig('db.png')

print("\nok")
