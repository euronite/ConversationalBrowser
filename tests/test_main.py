from PyQt5 import QtCore
import pytest

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
    assert widget.cueBtn.text() == "Cue Types"
    assert widget.exportBtn.text() == "Export"
    assert widget.callerGenderDropdown.currentText() == "Caller Both Genders"
    assert widget.receiverGenderDropdown.currentText() == "Receiver Both Genders"
    assert widget.roleDropdown.currentText() == "Receiver and Caller"
    assert widget.callerBtn.text() == "Caller ID"
    assert widget.averageCheckbox.text() == "Average"
    assert widget.durationRadioBtn.text() == "Duration"
    assert widget.occurrencesRadioBtn.text() == "Occurrences"
    assert widget.exportBtn.text() == "Export"


@pytest.fixture
def caller_data():
    widget = main.CallerDialog()
    ids = ["F01", "F02", "F03", "F04", "F05"]
    widget.populateListView(ids)
    return widget


def test_populate_caller_id_dialog(caller_data):
    assert caller_data.callerListWidget.count() == 6


def test_deselect_callerIds_dialog(qtbot, caller_data):
    qtbot.mouseClick(caller_data.pushButton, QtCore.Qt.LeftButton)
    assert len(caller_data.callerListWidget.selectedItems()) == 0


def test_select_all_caller_id_dialog(qtbot, caller_data):
    qtbot.mouseClick(caller_data.pushButton, QtCore.Qt.LeftButton)
    qtbot.addWidget(caller_data)
    caller_list = caller_data.callerListWidget
    rec = caller_list.visualItemRect(caller_list.item(0))
    center = rec.center()
    assert caller_list.itemAt(center).text() == "All Caller IDs"
    qtbot.mouseClick(caller_list.viewport(), QtCore.Qt.LeftButton, pos=center)
    assert len(caller_list.selectedItems()) == 5


def test_select_individual_caller_dialog(qtbot, caller_data):
    qtbot.mouseClick(caller_data.pushButton, QtCore.Qt.LeftButton)
    qtbot.addWidget(caller_data)
    caller_list = caller_data.callerListWidget
    rec = caller_list.visualItemRect(caller_list.item(1))
    center = rec.center()
    qtbot.mouseClick(caller_list.viewport(), QtCore.Qt.LeftButton, pos=center)
    assert caller_list.itemAt(center).text() == "F01"
    rec = caller_list.visualItemRect(caller_list.item(2))
    center = rec.center()
    assert caller_list.itemAt(center).text() == "F02"
    qtbot.mouseClick(caller_list.viewport(), QtCore.Qt.LeftButton, pos=center)
    assert len(caller_list.selectedItems()) == 2
