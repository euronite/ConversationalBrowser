from main import *


def test_mainwindow(qtbot):
    w = MainWindow()
    qtbot.addWidget(w)
