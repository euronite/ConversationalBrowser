#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This contains the main Controller/View of the GUI.
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog, QDialogButtonBox, QVBoxLayout
import sys
from conversationalbrowser import data_manipulation as dm
from conversationalbrowser.model import Model
from conversationalbrowser import graph
from pathlib import Path


class FileDialog(QWidget):
    def __init__(self):
        super(FileDialog, self).__init__()
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Choose csv file")
        self.setGeometry(100, 100, 640, 480)

    def open_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "QFileDialog.getOpenFileName()",
            "",
            "CSV Files (*.csv)",
            options=options,
        )
        return file


class CallerDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(CallerDialog, self).__init__(*args, **kwargs)
        uic.loadUi(Path("conversationalbrowser/ui/dialog_caller_id.ui"), self)
        self.setWindowTitle("Choose caller IDs")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        self.model = Model()
        super(MainWindow, self).__init__(*args, **kwargs)
        # Load the UI
        ui_location = Path(
            "conversationalbrowser/ui/main_window.ui"
        )  # This converts \ on windows etc.
        uic.loadUi(ui_location, self)
        graph.initmpl(self)

    def openCallerDialog(self):
        caller_dialog = CallerDialog()
        caller_dialog.exec_()
        caller_dialog.show()

    @pyqtSlot()
    def browseSlot(self):
        file_dialog = FileDialog()
        file = file_dialog.open_file_dialog()
        if file:
            self.model.set_file_name(file)
            self.callerDropdown.addItems(
                dm.get_all_call_ids(self.model.get_file_content())
            )
            QMessageBox.information(self, "Load File", "File loaded successfully.")
        else:
            QMessageBox.critical(
                self, "Load File Error", "File not selected, please try again"
            )

    @pyqtSlot()
    def clearGraphSlot(self):
        self.openCallerDialog()
        # graph.rmmpl(self)

    @pyqtSlot()
    def displayGraphSlot(self):
        if self.occurrencesRadioBtn.isChecked():
            print("occurrences")
        else:
            print("duration")
        if self.averageCheckbox.isChecked():
            print("Average selected")
        gender = self.genderDropdown.currentText()
        role = self.roleDropdown.currentText()
        cue = self.cueDropdown.currentText()
        caller_id = self.callerDropdown.currentText()
        chart = self.chartDropdown.currentText()
        print(gender, role, cue, caller_id, chart)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()