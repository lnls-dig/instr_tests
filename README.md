# instr_tests

## Overall
Repository with classes and functions aiming to remotely control laboratory
instruments such as network analyzers, signal generators and oscilloscopes.
This is done using VXI-11 protocol through PyVisa and PyVisa-py.

## Implemented devices

For now, the devices under implementation are:

- Agilent (Keysight) E5061B Network Analyzer
- Rohde & Schwarz SMA100A Signal Generator

## Requirements

The classes need PyVisa >= 1.8 and PyVisa-py >= 0.2 to work properly. They
can be installed using the following commands:


```
$ pip3 install pyvisa
$ pip3 install pyvisa-py
```

## Documentation

To be done in readthedocs.org