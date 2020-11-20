#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This holds the functions to draw the graph on the user interface using matplotlib.
"""
from PyQt5.QtWidgets import QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
from conversationalbrowser import data_manipulation as dm

matplotlib.use("Qt5Agg")


def rmmpl(self):
    """
    removes existing graph
    """
    self.mplvl.removeWidget(self.canvas)
    self.canvas.close()
    fig = Figure()
    fig.add_subplot(111)
    self.canvas = FigureCanvas(fig)
    self.mplvl.addWidget(self.canvas)
    self.canvas.draw()


def addmpl(self, fig):
    """
    Adds a figure to the UI
    :param self:
    :param fig: this contains the values that are to be displayed on the plot
    """
    self.canvas = FigureCanvas(fig)
    self.mplvl.addWidget(self.canvas)
    self.canvas.draw()


def initmpl(self):
    """
    this is used to initialise a blank plot when the application is first run.
    """
    fig = Figure()
    fig.add_subplot(111)
    self.canvas = FigureCanvas(fig)
    self.mplvl.addWidget(self.canvas)
    self.canvas.draw()


def displaympl(self, model, callerIds):
    """
    This is used to display the graph upon Display button click.
    :param callerIds:
    :param model:
    :param self:
    :return:
    """

    if model.fileContents is None:
        return QMessageBox.critical(
            self, "File Not Loaded", "Data not loaded, please load data first!"
        )

    fig = Figure()  # New graph setup
    ax = fig.add_subplot(111)
    df = model.fileContents

    if callerIds.selected[0][1] == 0:
        # This means select all ids has been chosen
        pass
    else:
        df = dm.get_list_of_call_id_df(df, [i[0] for i in callerIds.selected])

    caller_gender = self.callerGenderDropdown.currentText()
    receiver_gender = self.receiverGenderDropdown.currentText()

    if caller_gender == "Caller Male":
        caller_gender = "caller_M"
    elif caller_gender == "Caller Female":
        caller_gender = "caller_F"
    else:
        caller_gender = None

    if receiver_gender == "Receiver Female":
        receiver_gender = "receiver_F"
    elif receiver_gender == "Receiver Male":
        receiver_gender = "receiver_M"
    else:
        receiver_gender = None

    df = dm.get_rows_by_caller_and_receiver(df, caller_gender, receiver_gender)

    cue = self.cueDropdown.currentText()

    if cue in ["Filler", "Laughter", "Silence"]:
        cue = cue.lower()
        cue_types = {cue: 0}
        df = dm.get_non_verbal_speech_only(df, cue)
    elif cue == "Backchat":
        cue = "bc"
        cue_types = {cue: 0}
        df = dm.get_non_verbal_speech_only(df, cue)
    else:
        cue_types = {"laughter": 0, "silence": 0, "filler": 0, "bc": 0}

    if self.occurrencesRadioBtn.isChecked():
        if self.callerGenderDropdown.isEnabled() and self.receiverGenderDropdown.isEnabled():
            result = dm.occurrence_of_each_event(df, cue_types)
            ax.set_title("Total Cue Occurrences")
        elif not self.callerGenderDropdown.isEnabled():
            result = {}
            for cue in cue_types:
                try:
                    cue_result = dm.occurrence_of_event(df, cue)
                except ValueError:
                    return
                result[cue] = cue_result[0]  # This gets the occurrence of each cue of the caller
            if "silence" in result:
                result.pop("silence")  # Remove silence since this applies for both parties, not individually
            ax.set_title("Total Cue Occurrences for Receivers")
        else:
            result = {}
            for cue in cue_types:
                try:
                    cue_result = dm.occurrence_of_event(df, cue)
                except ValueError:
                    return
                result[cue] = cue_result[1]  # This gets occurrence of each cue of the receiver
            if "silence" in result:
                result.pop("silence")
            ax.set_title("Total Cue Occurrences for Callers")
        ax.bar(result.keys(), result.values())
        ax.set_xlabel("Cue")
        ax.set_ylabel("Total Number of Occurrences")
    else:
        result = dm.total_time_of_each_event(df, cue_types)
        ax.bar(result.keys(), result.values())
        ax.set_title("Cue Duration")
        ax.set_xlabel("Cue")
        ax.set_ylabel("Total Duration Time (s)")

    self.mplvl.removeWidget(self.canvas)
    self.canvas.close()
    self.canvas = FigureCanvas(fig)
    self.mplvl.addWidget(self.canvas)
    self.canvas.draw()
