#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This contains the main Controller/View of the GUI.
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog
from sys import exit as s_exit
from sys import argv as s_argv
from conversationalbrowser import data_manipulation as dm
from conversationalbrowser.model import Model, CallerModel
from conversationalbrowser import graph
from pathlib import Path


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        self.model = Model()
        self.callModel = CallerModel()
        super(MainWindow, self).__init__(*args, **kwargs)
        # Load the UI
        ui_location = Path(
            "conversationalbrowser/ui/main_window.ui"
        )  # This converts \ on windows etc.
        uic.loadUi(ui_location, self)
        graph.initmpl(self)
        self.roleDropdown.activated[str].connect(self.callerReceiverToggle)
        self.chartDropdown.activated[str].connect(self.averageToggle)

    @pyqtSlot()
    def browseSlot(self):
        file_dialog = FileDialog()
        file = file_dialog.openFileDialog()
        if file:
            self.model.set_file_name(file)
            self.model.set_caller_ids(
                dm.get_all_call_ids(self.model.get_file_content())
            )

            QMessageBox.information(self, "Load File", "File loaded successfully.")
        else:
            QMessageBox.critical(
                self, "Load File Error", "File not selected, please try again"
            )

    @pyqtSlot()
    def exportGraph(self):
        file_dialog = FileDialog()
        location = file_dialog.saveFileDialog()
        try:
            graph.export(self, location)
        except IOError:
            QMessageBox.critical(self, "Saving File Error", "Unable to save file!")

    @pyqtSlot()
    def clearGraphSlot(self):
        graph.rmmpl(self)

    @pyqtSlot()
    def displayCallerDialog(self):
        self.openCallerDialog()

    @pyqtSlot()
    def cueType(self):
        self.openCueDialog()

    @pyqtSlot()
    def displayGraphSlot(self):
        if not self.callModel.selected:
            self.callModel.selected = [("All Caller IDs", 0)]
        if not self.callModel.cues_selected:
            self.callModel.cues_selected = [("All Cues", 0)]
        graph.displaympl(self, self.model, self.callModel)

    def averageToggle(self):
        if self.chartDropdown.currentText() == "Display Totals":
            self.averageCheckbox.setEnabled(True)
        else:
            self.averageCheckbox.setEnabled(False)

    def callerReceiverToggle(self):
        if self.roleDropdown.currentText() == "Receiver and Caller":
            self.callerGenderDropdown.setEnabled(True)
            self.receiverGenderDropdown.setEnabled(True)
        elif self.roleDropdown.currentText() == "Caller":
            self.receiverGenderDropdown.setEnabled(False)
            self.callerGenderDropdown.setEnabled(True)
        elif self.roleDropdown.currentText() == "Receiver":
            self.callerGenderDropdown.setEnabled(False)
            self.receiverGenderDropdown.setEnabled(True)

    def openCueDialog(self):
        cue_dialog = CueDialog(self)
        if not self.callModel.cues_selected:
            cue_dialog.selectAll()
        else:
            for pair in self.callModel.cues_selected:
                if pair[1] == 0:
                    cue_dialog.selectAll()
                    break
                cue_dialog.cueListWidget.item(pair[1]).setSelected(True)
        cue_dialog.exec_()
        cue_dialog.show()
        self.callModel.cues_selected = []
        for item in cue_dialog.cueListWidget.selectedItems():
            self.callModel.cues_selected.append(
                (item.text(), cue_dialog.cueListWidget.row(item))
            )

    def openCallerDialog(self):
        caller_dialog = CallerDialog(self)
        caller_dialog.populateListView(self.model.callerIds)
        if not self.callModel.selected:
            caller_dialog.selectAll()
        else:
            for pair in self.callModel.selected:
                # Selects the rows that have been selected previously. If the previously selected row is 0, selectall
                if pair[1] == 0:
                    caller_dialog.selectAll()
                    break
                caller_dialog.callerListWidget.item(pair[1]).setSelected(True)
        caller_dialog.exec_()
        caller_dialog.show()
        self.callModel.selected = []
        for item in caller_dialog.callerListWidget.selectedItems():
            # This appends the caller ID and the position in the list to the caller model.
            self.callModel.selected.append(
                (item.text(), caller_dialog.callerListWidget.row(item))
            )


class FileDialog(QWidget):
    def __init__(self):
        super(FileDialog, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Choose csv file")
        self.setGeometry(100, 100, 640, 480)

    def openFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "QFileDialog.getOpenFileName()",
            "",
            "CSV Files (*.csv)",
            options=options,
        )
        return file

    def saveFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            None,
            "QFileDialog.getSaveFileName()",
            directory="plot.png",
            options=options,
        )
        return filename


class CallerDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(CallerDialog, self).__init__(*args, **kwargs)
        uic.loadUi(Path("conversationalbrowser/ui/dialog_caller_id.ui"), self)
        self.setWindowTitle("Choose caller IDs")
        self.callerListWidget.selectionModel().currentChanged.connect(self.onRowChanged)

    def populateListView(self, id_list):
        self.callerListWidget.addItems(id_list)

    def onRowChanged(self, current):
        if current.row() != 0:
            self.callerListWidget.item(0).setSelected(False)
        elif current.row() == 0:
            self.selectAll()

    def deselectAll(self):
        for i in range(self.callerListWidget.count()):
            self.callerListWidget.item(i).setSelected(False)

    def selectAll(self):
        for i in range(self.callerListWidget.count()):
            self.callerListWidget.item(i).setSelected(True)

    @pyqtSlot()
    def clearCallerList(self):
        self.deselectAll()


class CueDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(CueDialog, self).__init__(*args, **kwargs)
        uic.loadUi(Path("conversationalbrowser/ui/dialog_cue.ui"), self)
        self.setWindowTitle("Choose cues to display")
        self.cueListWidget.selectionModel().currentChanged.connect(self.onRowChanged)

    def onRowChanged(self, current):
        if current.row() != 0:
            self.cueListWidget.item(0).setSelected(False)
        elif current.row() == 0:
            self.selectAll()

    def deselectAll(self):
        for i in range(self.cueListWidget.count()):
            self.cueListWidget.item(i).setSelected(False)

    def selectAll(self):
        for i in range(self.cueListWidget.count()):
            self.cueListWidget.item(i).setSelected(True)

    @pyqtSlot()
    def clearCueList(self):
        self.deselectAll()


def main():
    app = QtWidgets.QApplication(s_argv)
    main_window = MainWindow()
    main_window.show()
    s_exit(app.exec())


if __name__ == "__main__":
    main()
