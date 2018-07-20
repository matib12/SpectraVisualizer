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
    # number of traces
    numberoftraces = None
    rbw = 1.0

    originalunit = 'vrms'

    converters = SC.allconverters[originalunit]

    # Header takes 15 lines
    def __init__(self, filename):
        self.fname = filename
        self.data = genfromtxt(filename, delimiter=',', skip_header=16)
        self.numberoftraces = len(self.data[0] - 1)
        self.rbw = 30000.0


    def header(self):
        pass
