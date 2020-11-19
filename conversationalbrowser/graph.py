#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This holds the functions to draw the graph on the user interface using matplotlib.
"""
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
    :param model:
    :param self:
    :return:
    """

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
        result = dm.occurrence_of_each_event(df, cue_types)
        ax.bar(result.keys(), result.values())
        ax.set_title("Cue Occurrences")
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
