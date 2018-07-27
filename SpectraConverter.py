#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np

__authors__ = "Mateusz Bawaj, Marco Vardaro"
__copyright__ = "Copyright 2018"
__license__ = "GPL"
__version__ = "1.0.4"
__maintainer__ = "Mateusz Bawaj"
__email__ = "bawaj@pg.infn.it"
__status__ = "Development"

# Units
# Amplitude
vpp = {'id':"vpp", 'symbol': "Vpp", 'unit': "V"}
vamp = {'id':"ampl", 'symbol': "Ampl", 'unit': "V"}
vrms = {'id':"vrms", 'symbol': "Vrms", 'unit': "V"}
dbvrms = {'id':"dbvrms", 'symbol':"dBVrms", 'unit':"dBVrms"}
# Power
watt = {'id':"watt", 'symbol': "P", 'unit': "W"}
dBm = {'id':"dbm", 'symbol': "dBm", 'unit': "dBm"}


# Power spectral density
# psd_dBm = {'id':"psddbm", 'symbol': "dBm/Hz", 'unit': "W/Hz", 'physical_quantity': "PSD"}
class psd_dBm:  # Verified with data acquired by 4395A!!! Works well
    id ="psddbm"
    symbol = "dBm/Hz"
    unit = "W/Hz"
    physical_quantity = "PSD"

    def normalizer(self, array, rbw):
        """

        :param array:
        :param rbw:
        :return:
        """
        return lognormalize(array, rbw)

    def K(self, rbw):
        return KdB(rbw)


class psd_W:  # Verified with data acquired by 4395A!!! Works well
    id = "psdwatt"
    symbol = "W/Hz"
    unit = "W/Hz"
    physical_quantity = "PSD"

    def normalizer(self, array, rbw):
        return linNormalize(array, rbw)

    def K(self, rbw):
        return KW(rbw)


#psd_volt = {'id':"psdvolt", 'symbol': "V²/Hz", 'unit': "V^2/Hz", 'physical_quantity': "PSD"}
class psd_volt:
    id = "psdvolt"
    symbol = "V²/Hz"
    unit = "V^2/Hz"
    physical_quantity = "PSD"

    def normalizer(self, array, rbw):
        return linNormalize(array, rbw)

    def K(self, rbw):
        return KW(rbw)


# Energy spectral density
#esd_volt = {'id':"esdvolt", 'symbol': "V/Hz", 'unit': "V/Hz", 'physical_quantity': "ESD"}
# class esd_volt:
#     id = "esdvolt"
#     symbol = "V/Hz"
#     unit = "V/Hz"
#     physical_quantity = "ESD"
#
#     def normalizer(self, array, rbw):
#         return linnormalize(array, rbw)
#
#     def K(self, rbw):
#         return KW(rbw)

# Amplitude spectral density
class asd_volt:  # Verified with data acquired by 4395A!!! Works well
    id = "asdvolt"
    symbol = "V/√Hz"
    unit = "V/sqrt(Hz)"
    physical_quantity = "ASD"

    def normalizer(self, array, rbw):
        return linNormalize(array, rbw)

    def K(self, rbw):
        return KV(rbw)


class asd_dBV:  # Verified with data acquired by 4395A!!! Works well
    id ="asddbv"
    symbol = "dBV/√Hz"
    unit = "V/sqrt(Hz)"
    physical_quantity = "ASD"

    def normalizer(self, array, rbw):
        return lognormalize(array, rbw)

    def K(self, rbw):
        return KdB(rbw)


spectraunits = [psd_dBm, asd_dBV, psd_W, psd_volt, asd_volt]
#allunits = {vpp, vamp, vrms, watt, dBm}
unitssymbols = []
for a in spectraunits:
    unitssymbols.append(a.symbol)


# === Conversions ===
def vpp2amp(array):
    """!@brief Function converts Volt peak-to-peak to amplitude.

    This function takes a part of converters dictionary fromvppconverterspalette.

    @type array
    @param array Input array

    @rtype: array
    @return: Returns a sentence with your variables in it
    """
    return array/2.0


def vpp2vrms(array):
    return array/(2.0*math.sqrt(2.0))


def vpp2power(array, resistance=50.0):
    vrms = vpp2vrms(array)
    return vrms * vrms / resistance


def vpp2dbm(array, resistance=50.0):
    watt = vpp2power(array, resistance)
    return 10.0 * np.log10(watt) + 30.0


def amp2vpp(array):
    return array * 2.0


def amp2vrms(array):
    return array * 2.0 / math.sqrt(2.0)


def amp2power(array, resistance=50.0):
    vrms = amp2vrms(array)
    return vrms * vrms / resistance


def amp2dbm(array, resistance=50.0):
    watt = amp2power(array, resistance)
    return 10.0 * np.log10(watt) + 30.0


def vrms2amp(array):
    return array * math.sqrt(2.0)


def vrms2vpp(array):
    return array * 2.0


def vrms2power(array, resistance=50.0):
    return (array * array) / resistance


def vrms2dbm(array, resistance=50.0):
    watt = vrms2power(array, resistance)
    return 10.0 * np.log10(watt) + 30.0


def dbm2power(array):
    return np.power(10, (array - 30.0) / 10.0)


def dbm2vrms(array, resistance=50.0):
    watt = dbm2power(array)
    return np.sqrt(watt * resistance)


def dbm2amp(array, resistance=50.0):
    vrms = dbm2vrms(array, resistance)
    return vrms * math.sqrt(2.0)


def dbm2vpp(array, resistance=50.0):
    amp = dbm2amp(array, resistance)
    return amp * 2.0


def power2dbm(array):
    return 10.0 * np.log10(array) + 30.0


def power2vrms(array, resistance=50.0):
    return np.sqrt(array * resistance)


def power2amp(array, resistance=50.0):
    vrms = power2vrms(array, resistance)
    return vrms * math.sqrt(2.0)


def power2vpp(array, resistance=50.0):
    amp = power2amp(array, resistance)
    return amp * 2.0


def single(array):
    return array


# K factor
def KdB(rbw):
    return 10.0 * math.log10(rbw)


def KW(rbw):
    return rbw


def KV(rbw):
    return math.sqrt(rbw)


# === Normalization ===
def lognormalize(array, K):  # dBm/Hz, dBV/sqrt(Hz), dBuV/sqrt(Hz)
    return array - K


def linNormalize(array, K):  # V/sqrt(Hz), W/Hz
    return array / K


from_vpp_converterspalette = {'vpp': single, 'amp': vpp2amp, 'vrms': vpp2vrms, 'power': vpp2power, 'dbm': vpp2dbm}
from_amp_converterspalette = {'vpp': amp2vpp, 'amp': single, 'vrms': amp2vrms, 'power': amp2power, 'dbm': amp2dbm}
from_rms_converterspalette = {'vpp': vrms2vpp, 'amp': vrms2amp, 'vrms': single, 'power': vrms2power, 'dbm': vrms2dbm}
from_power_converterspalette = {'vpp': power2vpp, 'amp': power2amp, 'vrms': power2vrms, 'power': single, 'dbm': power2dbm}
from_dbm_converterspalette = {'vpp': dbm2vpp, 'amp': dbm2amp, 'vrms': dbm2vrms, 'power': dbm2power, 'dbm': single}

allconverters = {'vpp': from_vpp_converterspalette, 'amp': from_amp_converterspalette, 'vrms': from_rms_converterspalette, 'dbm': from_dbm_converterspalette, 'power': from_power_converterspalette}
