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
__version__ = "1.0.4"
__maintainer__ = "Mateusz Bawaj"
__email__ = "bawaj@pg.infn.it"
__status__ = "Development"

#parserid =

parsername = "Agilent/HP 4395A"
parsershortname = "4395A"

# Filter name for QFileDialog
filtername = parsershortname + " (*.txt)"

# Available spectra units from the instrument: spectrum: dBm, dBV, dBuV, W, V;
#                                                 noise: dBm/Hz, dBV/sqrt(Hz), dBuV/sqrt(Hz), W/Hz, V/sqrt(Hz).
# I expect that "noise" means normalized to the resolution bandwidth.


class parser(gp.genericparser):

    originalunit = 'dbm'  # Can be discovered automatically by parser or set manually

    converters = SC.allconverters[originalunit]

    # Header takes 15 lines
    headerlength = 15

    def __init__(self, filename):
        self.fname = filename
        self.rbw = 1.0

    def _header(self):
        with open(self.fname, 'r') as f:
            for i in range(self.headerlength):
                line_text = f.readline()

                #  RBW
                rbw_line_format = '"RBW:{:^}VBW:{:^}"'
                par = parse.parse(rbw_line_format, line_text)
                #print("Parser debug: " + str(par))
                if par is not None:
                    self.rbw = par[0][:-2]

                #  Unit
                unit_line_format = '"FORMAT TYPE: SPECTRUM   UNIT:{:^}"'
                par = parse.parse(unit_line_format, line_text)
                #print("Parser debug: " + str(par))
                if par is not None:
                    self.originalunit = par[0]
                    print(self.originalunit)

    def parse(self):
        traces = []

        self._header()

        data = genfromtxt(self.fname, delimiter='\t',
                          skip_header=self.headerlength)  # 1st col: freq, 2nd col: tr1, 3rd col: tr2
        self.numberoftraces = len(data[0]) - 1
        for i in range(self.numberoftraces):
            thistrace = gp.trace()
            thistrace.fname = self.fname  # Filename
            thistrace.number = i  # Trace number
            thistrace.rbw = self.rbw  # RBW
            thistrace.originalunit = self.originalunit  # Original unit
            thistrace.tracedata = data[:, [0, i + 1]]  # Trace data
            traces.append(thistrace)  # Each trace is composed of two columns: freq, trace

        del data

        return traces
