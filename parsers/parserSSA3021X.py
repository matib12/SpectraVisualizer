#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# import numpy as np

# Number of points varies. It is up to 801 points per channel (or 401 while using two channels?)

import parserGeneric as gp
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

parsername = "Siglent SSA3021X"
parsershortname = "SSA3021X"

# Filter name for QFileDialog
filtername = parsershortname + " (*.txt)"


class parser(gp.genericparser):
    fname = None
    data = None
    # number of traces
    numberoftraces = None
    rbw = 1.0

    rbw_format_string = 'PN-{:0>9}'

    originalunit = 'dbm' # Can be discovered automatically by parser or set manually

    converters = SC.allconverters[originalunit]

    # Header takes 15 lines
    headerlength = 15

    def __init__(self, filename):
        self.fname = filename
        self.data = genfromtxt(filename, delimiter='\t', skip_header=self.headerlength)
        self.numberoftraces = len(self.data[0] - 1)
        self.rbw = 1.0

    def header(self):
        f = open(self.fname, 'r')

        for i in range(self.headerlength):
            line_text = f.readline()

            #  RBW
            rbw_line_format = '"RBW:{:^}VBW:{:^}"'
            par = parse.parse(rbw_line_format, line_text)
            print(par)
            if par is not None:
                self.rbw = par[0][:-2]

        f.close()
