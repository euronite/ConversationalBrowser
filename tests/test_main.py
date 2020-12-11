from PyQt5.uic.uiparser import QtCore

import main


# test unit tests run and are able to pass
def test_assert():
    test_value = 1
    assert test_value == 1


def test_ui(qtbot):
    widget = main.MainWindow()
    qtbot.addWidget(widget)
    assert widget.displayBtn.text() == "Display"
    assert widget.clearBtn.text() == "Clear"
    assert widget.chartDropdown.currentText() == "Display Totals"
    assert widget.cueDropdown.currentText() == "All"
    assert widget.exportBtn.text() == "Export"
    assert widget.callerGenderDropdown.currentText() == "Caller Both Genders"
    assert widget.receiverGenderDropdown.currentText() == "Receiver Both Genders"
    assert widget.roleDropdown.currentText() == "Receiver and Caller"
    assert widget.callerBtn.text() == "Caller ID"
    assert widget.averageCheckbox.text() == "Average"
    assert widget.durationRadioBtn.text() == "Duration"
    assert widget.occurrencesRadioBtn.text() == "Occurrences"
