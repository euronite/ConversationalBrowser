from PyQt5 import QtCore
import pytest

import main


# test unit tests run and are able to pass
def test_assert():
    test_value = 1
    assert test_value == 1


def test_ui(qtbot, main_window):
    qtbot.addWidget(main_window)
    assert main_window.displayBtn.text() == "Display"
    assert main_window.clearBtn.text() == "Clear"
    assert main_window.chartDropdown.currentText() == "Display Totals"
    assert main_window.cueBtn.text() == "Cue Types"
    assert main_window.exportBtn.text() == "Export"
    assert main_window.callerGenderDropdown.currentText() == "Caller Both Genders"
    assert main_window.receiverGenderDropdown.currentText() == "Receiver Both Genders"
    assert main_window.roleDropdown.currentText() == "Receiver and Caller"
    assert main_window.callerBtn.text() == "Caller ID"
    assert main_window.averageCheckbox.text() == "Average"
    assert main_window.durationRadioBtn.text() == "Duration"
    assert main_window.occurrencesRadioBtn.text() == "Occurrences"
    assert main_window.exportBtn.text() == "Export"


@pytest.fixture
def caller_data():
    widget = main.CallerDialog()
    ids = ["F01", "F02", "F03", "F04", "F05"]
    widget.populateListView(ids)
    return widget

@pytest.fixture
def main_window():
    return main.MainWindow()


def test_disable_caller_dropdown(main_window):
    assert main_window.callerGenderDropdown.isEnabled()
    main_window.roleDropdown.setCurrentIndex(1)
    assert main_window.roleDropdown.currentText() == "Receiver"
    main_window.callerReceiverToggle()
    assert main_window.callerGenderDropdown.isEnabled() is False
    main_window.roleDropdown.setCurrentIndex(2)
    main_window.callerReceiverToggle()
    assert main_window.callerGenderDropdown.isEnabled()


def test_disable_receiver_dropdown(main_window):
    assert main_window.receiverGenderDropdown.isEnabled()
    main_window.roleDropdown.setCurrentIndex(1)
    main_window.callerReceiverToggle()
    assert main_window.receiverGenderDropdown.isEnabled()
    main_window.roleDropdown.setCurrentIndex(2)
    main_window.callerReceiverToggle()
    assert main_window.receiverGenderDropdown.isEnabled() is False

def test_display_totals(main_window):
    main_window.chartDropdown.setCurrentIndex(1)
    assert main_window.chartDropdown.currentText() == "Display Per Call"
    main_window.averageToggle()
    assert main_window.averageCheckbox.isEnabled() is False
    main_window.chartDropdown.setCurrentIndex(0)
    main_window.averageToggle()
    assert main_window.averageCheckbox.isEnabled() is True
def test_select_individual_caller_dialog(qtbot):
    cue_dialog = main.CueDialog()
    qtbot.mouseClick(cue_dialog.pushBtn, QtCore.Qt.LeftButton)
    qtbot.addWidget(cue_dialog)
    cue_list = cue_dialog.cueListWidget
    rec = cue_list.visualItemRect(cue_list.item(1))
    center = rec.center()
    qtbot.mouseClick(cue_list.viewport(), QtCore.Qt.LeftButton, pos=center)
    assert cue_list.itemAt(center).text() == "Silence"
    rec = cue_list.visualItemRect(cue_list.item(2))
    center = rec.center()
    assert cue_list.itemAt(center).text() == "Backchat"
    qtbot.mouseClick(cue_list.viewport(), QtCore.Qt.LeftButton, pos=center)
    assert len(cue_list.selectedItems()) == 2


def test_cue_dialog(qtbot):
    cue_dialog = main.CueDialog()
    qtbot.addWidget(cue_dialog)
    qtbot.mouseClick(cue_dialog.pushBtn, QtCore.Qt.LeftButton)
    assert len(cue_dialog.cueListWidget.selectedItems()) == 0


def test_select_all_cues_dialog(qtbot):
    cue_dialog = main.CueDialog()
    qtbot.mouseClick(cue_dialog.pushBtn, QtCore.Qt.LeftButton)
    qtbot.addWidget(cue_dialog)
    cue_list = cue_dialog.cueListWidget
    rec = cue_list.visualItemRect(cue_list.item(0))
    center = rec.center()
    assert cue_list.itemAt(center).text() == "All Cues"
    qtbot.mouseClick(cue_list.viewport(), QtCore.Qt.LeftButton, pos=center)
    assert len(cue_list.selectedItems()) == 4


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


def test_select_individual_caller_dialog_individual(qtbot, caller_data):
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
