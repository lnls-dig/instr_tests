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

The classes need PyVisa >= 1.8 and PyVisa-py >= 0.2 to work properly.The Scikit-RF
package (>=0.15.1) is also used, and all dependences can be resolved using the
following command:


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