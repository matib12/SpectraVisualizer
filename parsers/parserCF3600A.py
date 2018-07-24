#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# import numpy as np

import parsers.parserGeneric as gp
from numpy import genfromtxt
import SpectraConverter as SC

__author__ = "Mateusz Bawaj"
__copyright__ = "Copyright 2018"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mateusz Bawaj"
__email__ = "bawaj@pg.infn.it"
__status__ = "Development"

#parserid =

parsername = "Ono Sokki CF-3600A"
parsershortname = "CF-3600A"

# Filter name for QFileDialog
filtername = parsershortname + " (*.txt)"


class parser(gp.genericparser):

    originalunit = 'vrms'

    converters = SC.allconverters[originalunit]

    # Header takes 15 lines
    def __init__(self, filename):
        self.fname = filename
        self.rbw = 1.0

    def parse(self):
        mytrace = []
        data = genfromtxt(self.fname, delimiter=',', skip_header=16)  # 1st col: freq, 2nd col: tr1, 3rd col: tr2
        self.numberoftraces = len(data[0]) - 1
        for i in range(self.numberoftraces):
            mytrace.append(data[:, [0, i + 1]])  # Each trace is composed of two columns: freq, trace

        return mytrace

    def header(self):
        pass
