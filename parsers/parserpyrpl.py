#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import numpy as np

import parsers.parserGeneric as gp
from numpy import genfromtxt
import SpectraConverter as SC
import math

__author__ = "Mateusz Bawaj"
__copyright__ = "Copyright 2018"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mateusz Bawaj"
__email__ = "bawaj@pg.infn.it"
__status__ = "Development"

#parserid =

parsername = "pyrpl"
parsershortname = "pyrpl"

# Filter name for QFileDialog
filtername = "pyrpl (*.csv)"


class parser(gp.genericparser):

    originalunit = 'dbm' # Can be discovered automatically by parser or set manually

    converters = SC.allconverters[originalunit]

    # Header takes 1 line
    headerlength = 1

    def __init__(self, filename):
        self.fname = filename
        self.rbw = 1.0

    def parse(self):
        traces = []

        self._header()  # It does nothing

        data = genfromtxt(self.fname, delimiter=',', skip_header=self.headerlength)[:, [0, 1, 3, 5, 7]] # What is column 7?
        self.numberoftraces = len(data[0]) - 1
        for i in range(self.numberoftraces):
            #print(data[0, i + 1])
            if not math.isnan(data[0, i + 1]):  # I remove traces containing NaN
                thistrace = gp.trace()
                thistrace.fname = self.fname  # Filename
                thistrace.number = i  # Trace number
                thistrace.rbw = self.rbw  # RBW
                thistrace.originalunit = self.originalunit  # Original unit
                thistrace.tracedata = data[:, [0, i + 1]]
                traces.append(thistrace)  # Each trace is composed of two columns: freq, trace

        del data

        return traces

    def _header(self):
        pass
