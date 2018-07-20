#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from PyQt4 import QtGui, uic
from PyQt4 import QtCore as core
import numpy as np
import copy

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
__version__ = "1.0.1"
__maintainer__ = "Mateusz Bawaj"
__email__ = "bawaj@pg.infn.it"
__status__ = "Development"


class SvMainWindow(QtGui.QMainWindow):
    data = np.array

# Add parsers to the collection
    allparsers = {parser3589A, parser4395A, parserCF3600A, parserpyrpl}
    filterslist = core.QStringList()
    psdunitlist = []

    selectedparser = parser4395A  # Default parser in add file dialog. Substituted later in the openspectrumfile

    def resizeEvent(self, e):
        self.spectraTableWidget.resize(self.width() - 20, 380)  # Resize list of spectra
        frombottom = 80
        self.plotButton.move(10, self.height() - frombottom)
        self.addButton.move(10, self.height() - frombottom - 50)
        self.removeButton.move(140, self.height() - frombottom - 50)
        #QtGui.QMainWindow.resizeEvent(self, e)  # Given by https://stackoverflow.com/questions/41091212/pyqt4-window-resize-event

    def __init__(self):
# Prepare list of filters for QFileDialog
        self.filterslist.append("Select device")
        for par in self.allparsers:
            self.filterslist.append(par.filtername)
        self.filterslist.append("Spectrum files (*.csv *.dat *.xml)")
        self.filterslist.append("All files (*.*)")

        super(SvMainWindow, self).__init__()

        uic.loadUi("./SpectraVisualizer.ui", self)

# Prepare QTableView header widths
        self.spectraTableWidget.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)

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
        print("Open file dialog...")
        filedialog = QtGui.QFileDialog(self)
        filedialog.setWindowTitle('Load spectrum file')
        filedialog.setNameFilters(self.filterslist)
        filedialog.selectNameFilter(self.selectedparser.filtername)
        filedialog.setDirectory("~")

        if filedialog.exec_() == filedialog.Accepted:
            filedialog.selectedNameFilter()

            fname = filedialog.selectedFiles()[0]  # This is QString
            print("Loading file: " + fname)

            for parsermodule in self.allparsers:
                if parsermodule.filtername == filedialog.selectedNameFilter():  # Only if there is a coincident parser
                    self.selectedparser = parsermodule  # Remember parser for this session
                    newspectrum = parsermodule.parser(str(fname))

                    #  Header parse
                    newspectrum.header()
                    newspectrum.printparams()

                    #  Data parse
                    rownumber = self.spectraTableWidget.rowCount()
                    self.spectraTableWidget.insertRow(rownumber)

                    # 1st column - Filename and data
                    dataitem = QtGui.QTableWidgetItem(os.path.basename(str(fname)))
                    dataitem.setData(core.Qt.UserRole, newspectrum)
                    self.spectraTableWidget.setItem(rownumber, 0, dataitem)

                    # 2nd column - RBW
                    if newspectrum.rbw != 0:
                        rbwitem = QtGui.QTableWidgetItem(str(newspectrum.rbw))
                        rbwitem.setData(core.Qt.UserRole, newspectrum.rbw)
                    else:
                        rbwitem = QtGui.QTableWidgetItem("0.0")
                    self.spectraTableWidget.setItem(rownumber, 1, rbwitem)

                    # 3rd column - Measurement unit
                    nullIcon = QtGui.QIcon()
                    combo = QtGui.QComboBox()
                    for unit in SC.spectraunits:
                        combo.addItem(nullIcon, unit.symbol + " (" + unit.physical_quantity + ")", unit)
                    #combo.addItems(SC.unitssymbols)
                    if True: # If unit was recognized by parser
                        combo.setCurrentIndex(2)
                    self.spectraTableWidget.setCellWidget(rownumber, 2, combo)

                    # 4th column - Chart label
                    label = QtGui.QTableWidgetItem(os.path.basename(str(fname)))
                    self.spectraTableWidget.setItem(rownumber, 3, label)

                    # item.setCheckState(2)
                    #item.setSelected(False)
                    #self.spectraListWidget.addItem(item)
        else:
            print("QFileDialog canceled")
            return

    def removespectra(self):
        print("Remove selected spectra")
        index_list = []
        for SelectedItem in self.spectraTableWidget.selectedItems():
            index = SelectedItem.row()
            index_list.append(index)

        index_list = list(set(index_list)) # remove duplicates from the list

        for index in index_list:
            self.spectraTableWidget.removeRow(index)

    def plotallspectra(self):
        print("Plot spectra...")
        genericpars = gp.genericparser()
        numberofspectra = self.spectraTableWidget.rowCount()
        for dataset in range(0, numberofspectra):  # Iterate over all loaded spectra files
            its = copy.deepcopy(self.spectraTableWidget.item(dataset, 0).data(core.Qt.UserRole).toPyObject())  # Create full copy of data set
            #print(self.spectraTableWidget.item(dataset, 0).data(core.Qt.UserRole).toPyObject())
            print(its)

            try:
                rbw = gp.genericparser.from_SIprefix(genericpars, self.spectraTableWidget.item(dataset, 1).text())  # Read value of RBW from self.spectraTableWidget
            except ValueError as e:
                print(e)
                return

            print("RBW=" + str(rbw))  # Print RBW read from self.spectraTableWidget

            print(its.data)  # Before normalization and conversion

            # Use proper normalizer for existing source units
            curr_unit_index = self.spectraTableWidget.cellWidget(dataset, 2).currentIndex()  # Read selected unit
            print("Source unit: " + str(self.spectraTableWidget.cellWidget(dataset, 2).currentText().toStdString()))

            N = self.spectraTableWidget.cellWidget(dataset, 2).itemData(curr_unit_index, core.Qt.UserRole).toPyObject()
            print(N)

            its.data[:, range(1, its.numberoftraces)] = N.normalizer(self, its.data[:, range(1, its.numberoftraces)], N.K(self, rbw))
            # Use if necessary a proper converter based on source units and destination units

            print(its.data)  # After normalization and conversion

            labeltext = self.spectraTableWidget.item(dataset, 3).text()

            for trace in range(1, its.numberoftraces):
                plt.plot(its.data[:, 0], its.data[:, trace], label=labeltext + ' ' + str(trace))

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


    def printabout(self):
        print("Author: " + __author__)
        print("Copyright: " + __copyright__)
        print("Licence: " + __license__)
        print("Version: " + __version__)
        print("E-mail: " + __email__)
        print("Status: " + __status__)
        print("PyQt version: " + core.PYQT_VERSION_STR)
        print("Qt version: " + core.QT_VERSION_STR)
        print("Matplotlib version: " + matplotlib.__version__)

    def unitchanged(self):
        print("Unit index: " + str(self.unitComboBox.currentIndex()))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    # open the main window
    window = SvMainWindow()

    sys.exit(app.exec_())
