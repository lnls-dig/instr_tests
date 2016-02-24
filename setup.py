from setuptools import setup
import os
import io

import instr_tests

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')
install_requires = read('requirements.txt')
setup(
    name = "instr_tests",
    version = instr_tests.__version__,
    author = "Vitor Finotti Ferreira",
    author_email = "vitor.ferreira@lnls.br",
    description = ("Classes and functions to remotely access instruments and "
                   "run tests."),
    license = "GPLv3",
    keywords = "instruments vxi-11 pyvisa",
    url = "https://github.com/lnls-dig/instr_tests",
    packages=['instr_tests',],
    long_description = long_description,
    install_requires = install_requires,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ]
)
