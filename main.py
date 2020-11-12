from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMessageBox
import sys
from conversationalbrowser import data_manipulation as dm
from conversationalbrowser.model import Model
from pathlib import Path
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib

matplotlib.use("Qt5Agg")


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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        self.model = Model()
        super(MainWindow, self).__init__(*args, **kwargs)
        # Load the UI
        ui_location = Path(
            "conversationalbrowser/ui/main_window.ui"
        )  # This converts \ on windows etc.
        uic.loadUi(ui_location, self)
        fig = Figure()
        fig.add_subplot(111)
        self.addmpl(fig)

    def rmmpl(self):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        fig = Figure()
        fig.add_subplot(111)
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

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
        self.rmmpl()

    @pyqtSlot()
    def displayGraphSlot(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
