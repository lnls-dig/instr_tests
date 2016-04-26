# instr_tests

## Overall
Repository with classes and functions aiming to remotely control laboratory
instruments such as network analyzers, signal generators and oscilloscopes.
This is done using VXI-11 protocol through PyVisa and PyVisa-py.

## Implemented devices

For now, the devices under implementation are:

- Agilent (Keysight) E5061B Network Analyzer
- Rohde & Schwarz SMA100A Signal Generator
- Rohde & Schwarz SMB100A Signal Generator

## Requirements

The classes need PyVisa and PyVisa-py to communicate with the
devices using Visa protocol and PyEpics to communicate using the EPICS control system.
The Scikit-RF package is also used, and all dependences can be resolved using the following
command:


```
$ pip3 install -r requirements.txt
```

## Installation

The package can be installed using the setup.py file with the following command:

```
$ python3 setup.py install
```

## Documentation

To be done in readthedocs.org