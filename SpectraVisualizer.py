#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from PyQt4 import QtGui, uic
from qtpy import QtWidgets, uic
from qtpy import QtCore as core
import numpy as np
import gc

import sys, os

import matplotlib
import matplotlib.pyplot as plt

import parsers.parserGeneric as gp
import parsers.parser3589A as parser3589A
import parsers.parser4395A as parser4395A
import parsers.parserCF3600A as parserCF3600A
import parsers.parserpyrpl as parserpyrpl

import SpectraConverter as SC

__author__ = "Mateusz Bawaj"
__copyright__ = "Copyright 2018"
__license__ = "GPL"
__version__ = "1.0.4"
__maintainer__ = "Mateusz Bawaj"
__email__ = "bawaj@pg.infn.it"
__status__ = "Development"

# TODO add logging to file
# TODO add configuration file for last and favourite settings
# TODO write the SSA3000X parser


class SvMainWindow(QtWidgets.QMainWindow):
    filenameItemFlags = core.Qt.ItemIsSelectable | core.Qt.ItemIsUserCheckable | core.Qt.ItemIsEnabled
    traceItemFlags = core.Qt.ItemIsSelectable | core.Qt.ItemIsUserCheckable | core.Qt.ItemIsEnabled
    data = np.array

# Add parsers to the collection
    availableparsers = {parser3589A, parser4395A, parserCF3600A, parserpyrpl}
    parsers = list()
    filterslist = [None]
    psdunitlist = []

    selectedfilepath = None  # Working directory path
    selectedfiltername = None  #parser4395A  # Default parser in add file dialog. Substituted later in the openspectrumfile

    def resizeEvent(self, e):
        self.spectraTableWidget.resize(self.width() - 20, 380)  # Resize list of spectra
        frombottom = 80
        self.plotButton.move(10, self.height() - frombottom)
        self.addButton.move(10, self.height() - frombottom - 50)
        self.removeButton.move(140, self.height() - frombottom - 50)
        #QtGui.QMainWindow.resizeEvent(self, e)  # Given by https://stackoverflow.com/questions/41091212/pyqt4-window-resize-event

    def __init__(self):
        """
        Constructor of SvMainWindow
        1. Prepares an ordered list of filters for QFileDialog.
        2. Loads ui from file created by QtCreator
        3. Connects callbacks for events
        4. Displays GUI
        """
        self.filterslist[0] = ("Select device")
        parsermodulelist = []
        for par in self.availableparsers:
            parsermodulelist.append(par.filtername)

        parsermodulelist = sorted(parsermodulelist)  # Available filters appear always in the same order
        self.filterslist += parsermodulelist
        self.filterslist.append("Spectrum files (*.csv *.dat *.xml)")
        self.filterslist.append("All files (*.*)")

        super(SvMainWindow, self).__init__()

        uic.loadUi("./SpectraVisualizer.ui", self)

        # Prepare QTableView header widths
        self.spectraTableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Prepare list of units
        for unit in SC.spectraunits:
            #self.psdunitlist.append(unit.symbol + " (" + unit.physical_quantity + ")")
            self.unitComboBox.addItem(unit.symbol + " (" + unit.physical_quantity + ")", unit)

        # Attach methods:
        self.plotButton.clicked.connect(self.plotallspectra)

        self.addButton.clicked.connect(self.openspectrumfile)

        self.removeButton.clicked.connect(self.removespectra)

        self.actionOpenFile.triggered.connect(self.openspectrumfile)

        self.actionQuitSV.triggered.connect(self.quit_sv)

        self.actionAbout.triggered.connect(self.printabout)

        self.unitComboBox.currentIndexChanged.connect(self.unitchanged)

        self.show()

    @staticmethod
    def quit_sv():
        print("Quit Spectra Visualizer")
        exit(0)

    def openspectrumfile(self):
        """
        Adds entries to the list in the main window which correspond to traces saved in the parsed file
        """
        print("Open file dialog...")
        filedialog = QtWidgets.QFileDialog(self)
        filedialog.setWindowTitle('Load spectrum file')
        filedialog.setNameFilters(self.filterslist)
        if self.selectedfiltername is not None:
            filedialog.selectNameFilter(self.selectedfiltername)
        if self.selectedfilepath is None:
            filedialog.setDirectory("~")
        else:
            filedialog.setDirectory(self.selectedfilepath)

        if filedialog.exec_() == filedialog.Accepted:
            fname = filedialog.selectedFiles()[0]
            print("Loading file: " + fname)

            self.selectedfilepath = os.path.dirname(os.path.abspath(fname))

            for parsermodule in self.availableparsers:
                if parsermodule.filtername == filedialog.selectedNameFilter():  # Only if there is a coincident parser
                    self.selectedfiltername = parsermodule.filtername  # Remember the previous filtername

                    currentparse = parsermodule.parser(fname)  # Remember parser for this programme run

                    traces = currentparse.parse()  #

                    #  Data parse
                    rowsnumber = self.spectraTableWidget.rowCount()

                    for trace in traces:
                        self.spectraTableWidget.insertRow(rowsnumber)

                        # 1st column - Filename and data
                        dataitem = QtWidgets.QTableWidgetItem(os.path.basename(fname))
                        dataitem.setData(core.Qt.UserRole, trace)
                        dataitem.setFlags(self.filenameItemFlags)
                        self.spectraTableWidget.setItem(rowsnumber, 0, dataitem)

                        # 2nd column - Trace number in file
                        tracenumberinfileitem = QtWidgets.QTableWidgetItem(str(trace.number))
                        tracenumberinfileitem.setFlags(self.traceItemFlags)
                        self.spectraTableWidget.setItem(rowsnumber, 1, tracenumberinfileitem)

                        # 2nd column - RBW
                        if currentparse.rbw != 0:
                            rbwitem = QtWidgets.QTableWidgetItem(str(trace.rbw))
                            rbwitem.setData(core.Qt.UserRole, trace.rbw)
                        else:
                            rbwitem = QtWidgets.QTableWidgetItem("0.0")
                        self.spectraTableWidget.setItem(rowsnumber, 2, rbwitem)

                        # 3rd column - Measurement unit
                        combobox = QtWidgets.QComboBox()
                        for unit in SC.spectraunits:
                            combobox.addItem(unit.symbol + " (" + unit.physical_quantity + ")", unit)

                        if True:  # If unit was recognized by parser
                            combobox.setCurrentIndex(0)
                        self.spectraTableWidget.setCellWidget(rowsnumber, 3, combobox)

                        # 4th column - Chart label
                        labelitem = QtWidgets.QTableWidgetItem(os.path.basename(fname) + " TR:" + str(trace.number))
                        self.spectraTableWidget.setItem(rowsnumber, 4, labelitem)

                    del currentparse
        else:
            print("QFileDialog canceled")

    def removespectra(self):
        """
        Removes selected entries from the list in the main window
        """
        print("Remove selected spectra")
        index_list = []
        for SelectedItem in self.spectraTableWidget.selectedItems():
            index = SelectedItem.row()
            index_list.append(index)

        index_list = list(set(index_list))  # Remove duplicates from the list

        print(index_list)

        for index in index_list[::-1]:  # Remove in the reversed order
            self.spectraTableWidget.removeRow(index)

    def plotallspectra(self):
        """
        Opens a new window with a chart plotting all traces present in the list in the main window
        """
        print("Plot spectra...")
        numberofspectra = self.spectraTableWidget.rowCount()

        fig = plt.figure()
        fig.canvas.set_window_title('Chart')

        for dataset in range(0, numberofspectra):  # Iterate over all loaded spectra files
            its = self.spectraTableWidget.item(dataset, 0).data(core.Qt.UserRole)

            currenttrace = int(self.spectraTableWidget.item(dataset, 1).text())
            print("Plotting trace: " + str(currenttrace))

            try:
                rbw = gp.genericparser.from_SIprefix(input_str=self.spectraTableWidget.item(dataset, 2).text())  # Read value of RBW from self.spectraTableWidget
            except ValueError as e:
                print(e)
                return None

            print("RBW=" + str(rbw))  # Print RBW read from self.spectraTableWidget

            #print("Trace before normalization:")
            #print(its.tracedata[:, 1])  # Before normalization and conversion

            # Use proper normalizer for existing source units
            curr_unit_index = self.spectraTableWidget.cellWidget(dataset, 3).currentIndex()  # Read selected unit
            print("Source unit: " + str(self.spectraTableWidget.cellWidget(dataset, 3).itemData(curr_unit_index).unit))

            N = self.spectraTableWidget.cellWidget(dataset, 3).itemData(curr_unit_index)

            # Use if necessary a proper converter based on source units and destination units
            normalizedtemporary = N.normalizer(self, its.tracedata[:, 1], N.K(self, rbw))

            #print("Trace after normalization:")
            #print(normalizedtemporary)  # After normalization and conversion

            labeltext = self.spectraTableWidget.item(dataset, 4).text()  # Label

            plt.plot(its.tracedata[:, 0], normalizedtemporary, label=labeltext)

        if numberofspectra > 0:
            plt.ylabel(SC.spectraunits[self.unitComboBox.currentIndex()].symbol)

            if self.Xlog_checkBox.checkState():
                print("Print in logscale on X axis")
                plt.semilogx()

            plt.legend()
            plt.show()
            #plt.show(block=False) #depreciated

        else:
            print("Nothing to plot")

        if "normalizedtemporary" in locals():
            del normalizedtemporary

        gc.collect()  # Garbage collector keeps the memory usage fairly low


    def printabout(self):
        print("Author: " + __author__)
        print("Copyright: " + __copyright__)
        print("Licence: " + __license__)
        print("Version: " + __version__)
        print("E-mail: " + __email__)
        print("Status: " + __status__)
        print("PyQt version: " + core.PYQT_VERSION_STR)
        #print("Qt version: " + core.QT_VERSION)  # Was working with PyQt4 library
        print("Matplotlib version: " + matplotlib.__version__)

    def unitchanged(self):
        print("Unit index: " + str(self.unitComboBox.currentIndex()))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # open the main window
    window = SvMainWindow()

    sys.exit(app.exec_())
