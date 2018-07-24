#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import parse
import copy
import gc

__author__ = "Mateusz Bawaj"
__copyright__ = "Copyright 2018"
__license__ = "GPL"
__version__ = "1.0.4"
__maintainer__ = "Mateusz Bawaj"
__email__ = "bawaj@pg.infn.it"
__status__ = "Development"

SIprefix = {'Y': 24.0, 'Z': 21.0, 'E': 18.0, 'P': 15.0, 'T': 12.0, 'G': 9.0, 'M': 6.0, 'k': 3.0, 'm': -3.0, 'μ': -6.0,
           'u': -6.0, 'n': -9.0, 'p': -12.0, 'f': -15.0, 'a': -18.0, 'z': -21.0, 'y': -24.0}


class genericparser(object):
    fname = None
    rbw = 1.0

    def parse(self):  # Must be overloaded in the inheriting class
        return []

    def header(self):  # Must be overloaded in the inheriting class
        pass

    def printparams(self):
        print("Source file: " + self.fname)
        #print("Number of traces: " + str(self.numberoftraces))
        print("RBW: " + str(self.rbw))

    def from_SIprefix(input_str):
        format_string = '{:>g}{prefix:>D}'

        parse_res = parse.parse(format_string, input_str)  # If there is no pattern in the input string result is None

        if parse_res is None:  # No prefix used
            return float(input_str)
        else:
            #  print(parse_res)
            try:
                result = parse_res[0] * pow(10.0, SIprefix[parse_res['prefix'][0]])
            except KeyError as e:
                raise ValueError('Unknown prefix used')

        return result
