#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import numpy as np

import parsers.parserGeneric as gp
from numpy import genfromtxt
import SpectraConverter as SC
import parse

__author__ = "Mateusz Bawaj"
__copyright__ = "Copyright 2018"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mateusz Bawaj"
__email__ = "bawaj@pg.infn.it"
__status__ = "Development"

#parserid =

parsername = "pyrpl"

# Filter name for QFileDialog
filtername = "pyrpl (*.csv)"


class parser(gp.genericparser):

    originalunit = 'dbm' # Can be discovered automatically by parser or set manually

    converters = SC.allconverters[originalunit]

    # Header takes 1 line
    headerlength = 1

    def __init__(self, filename):
        self.traces[:] = []
        self.fname = filename
        self.traces = genfromtxt(filename, delimiter=',', skip_header=self.headerlength)[:, [0, 1, 3, 5]] # What is column 7?
        self.numberoftraces = len(self.data[0]) / 2.0
        self.rbw = 1.0


    def header(self):
        with open(self.fname, 'r') as f:
            for i in range(self.headerlength):
                text = f.readline()
                print(text)
                if 'RBW' in text:
                    pass
                    # print(text)
