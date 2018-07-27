#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Number of points varies. It is up to 801 points per channel (or 401 while using two channels?)

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

parsername = "HP 3589A"
parsershortname = "3589A"

# Filter name for QFileDialog
filtername = parsershortname + " (*.txt)"


class parser(gp.genericparser):

    rbw_format_string = 'PN-{:0>9}'

    originalunit = 'dbm'  # Can be discovered automatically by parser or set manually

    converters = SC.allconverters[originalunit]

    # Header takes 15 lines
    headerlength = 15

    def __init__(self, filename):
        self.traces[:] = []
        self.fname = filename
        data = genfromtxt(filename, delimiter='\t', skip_header=self.headerlength)
        self.numberoftraces = len(self.data[0]) - 1
        for i in range(self.numberoftraces):
            self.traces.append(data[:, [0, i + 1]])
        self.rbw = 1.0

    def _header(self):
        with open(self.fname, 'r') as f:
            for i in range(self.headerlength):
                line_text = f.readline()

                #  RBW
                rbw_line_format = '"RBW:{:^}VBW:{:^}"'
                par = parse.parse(rbw_line_format, line_text)
                print(par)
                if par is not None:
                    self.rbw = par[0][:-2]
