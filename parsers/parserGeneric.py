#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import parse

SIprefix = {'Y': 24.0, 'Z': 21.0, 'E': 18.0, 'P': 15.0, 'T': 12.0, 'G': 9.0, 'M': 6.0, 'k': 3.0, 'm': -3.0, 'μ': -6.0,
           'u': -6.0, 'n': -9.0, 'p': -12.0, 'f': -15.0, 'a': -18.0, 'z': -21.0, 'y': -24.0}

class genericparser:

    def printparams(self):
        print("File: " + self.fname)
        print("Number of traces: " + str(self.numberoftraces))
        print("RBW: " + str(self.rbw))


    def from_SIprefix(self, input_str):
        format_string = '{:>g}{prefix:>D}'

        parse_res = parse.parse(format_string, input_str)  # If there is no patter in the input string result is None

        if parse_res is None:  # No prefix used
            return float(input_str)
        else:
            #  print(parse_res)
            try:
                res = parse_res[0] * pow(10.0, SIprefix[parse_res['prefix'][0]])
            except KeyError as e:
                raise ValueError('Unknown prefix used')

        return res
