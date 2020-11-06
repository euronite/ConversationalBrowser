from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
import sys
from conversationalbrowser import data_manipulation as dm
from pathlib import Path


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Load the UI
        ui_location = Path(
            "conversationalbrowser/ui/main_window.ui"
        )  # This converts \ on windows etc.
        uic.loadUi(ui_location, self)
        self.loadDataBtn.clicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        data_location = Path(
            "data/genderedCorpus.csv"
        )  # converts / or \ depending on OS
        try:
            df = dm.read_in_data(data_location)
            print("Successfully read in data!")
        except FileNotFoundError:
            print("File has not been found. Please check file path is correct.")


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
