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
from numpy import arange, concatenate

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
    df = model.fileContents

    # Get the dataframe of relevant call IDs
    if callerIds.selected[0][1] == 0:
        # This means select all ids has been chosen
        pass
    else:
        df = dm.get_list_of_call_id_df(df, [i[0] for i in callerIds.selected])

    # Get relevant genders and the corresponding dataframe
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

    # Get the cue types
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
    try:
        if self.occurrencesRadioBtn.isChecked():
            if self.chartDropdown.currentText() == "Display Totals":
                get_total_cue_data(self, df, cue_types, fig, "occurrences")
            else:
                get_occurrences_per_call(self, df, cue_types, fig)
        else:
            if self.chartDropdown.currentText() == "Display Totals":
                get_total_cue_data(self, df, cue_types, fig, "durations")
            else:
                get_duration_per_call(self, df, cue_types, fig)
    except ValueError:
        error_dialog = QMessageBox()
        error_dialog.setText("Caller/Receiver Combination Not Valid")
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.exec_()
    # Display the actual graph
    self.mplvl.removeWidget(self.canvas)
    self.canvas.close()
    self.canvas = FigureCanvas(fig)
    self.mplvl.addWidget(self.canvas)
    self.canvas.draw()


def get_duration_per_call(self, df, cue_types, fig):
    cue_names = list(cue_types.keys())
    cue_results = []
    for cue in cue_names:
        # this holds the cue results temporarily
        try:
            cue_results_temp = dm.get_all_event_durations(df, cue)
        except ValueError:
            fig.add_subplot(111)
            raise
        if (
            self.callerGenderDropdown.isEnabled()
            and self.receiverGenderDropdown.isEnabled()
        ):
            cue_results.append(concatenate((cue_results_temp[0], cue_results_temp[1])))
        elif self.callerGenderDropdown.isEnabled():
            # so this is if caller is enabled, but not receiver. Remove every second since that's receiver data
            cue_results.append(cue_results_temp[0])
        else:
            # receiver only info. Remove any caller data
            cue_results.append(cue_results_temp[1])

    ax = []
    num_bins = 90
    for index, cue in enumerate(cue_results):
        if len(cue_names) == 1:
            ax.append(fig.add_subplot(111))
        else:
            ax.append(fig.add_subplot(2, 2, index + 1))
        ax[index].set(xlabel="Duration (s)", ylabel="Number of Occurrences")
        ax[index].set_title(cue_names[index])
        ax[index].hist(cue, bins=num_bins)
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    fig.suptitle("Cue Event Duration")


def get_occurrences_per_call(self, df, cue_types, fig):
    """
    This will get the occurrences for all callers of the cues
    :return:
    """
    if df.empty:
        fig.add_subplot(111)
        raise ValueError
    cue_names = list(cue_types.keys())
    cue_results = []
    ids = dm.get_all_call_ids(df)
    for cue in cue_names:
        cue_results_temp = []
        for call in ids:
            cue_results_temp.append(
                dm.occurrence_of_event(dm.get_call_df(df, call), cue)
            )
        if (
            self.callerGenderDropdown.isEnabled()
            and self.receiverGenderDropdown.isEnabled()
        ):
            cue_results.append(
                sorted([val for pair in cue_results_temp for val in pair])
            )
        elif self.callerGenderDropdown.isEnabled():
            # so this is if caller is enabled, but not receiver. Remove every second since thats receiver data
            sorted_list = sorted(
                [val for sublist in cue_results_temp for val in sublist]
            )
            del sorted_list[1:2]
            cue_results.append(sorted_list)
        else:
            # receiver only info. Remove any caller data
            sorted_list = sorted([val for pair in cue_results_temp for val in pair])
            del sorted_list[::2]
            cue_results.append(sorted_list)

    X = arange(len(cue_results[0]))
    ax = []
    for index, cue in enumerate(cue_results):
        if len(cue_names) == 1:
            ax.append(fig.add_subplot(111))
        else:
            ax.append(fig.add_subplot(2, 2, index + 1))
        ax[index].set(xlabel="Participant Number", ylabel="Total Occurrences Count")
        ax[index].set_title(cue_names[index])
        ax[index].bar(X, cue)

    fig.subplots_adjust(hspace=0.4, wspace=0.3)
    fig.suptitle("Total Occurrences for All Participants")


def get_total_cue_data(self, df, cue_types, fig, radio_type):
    ax = fig.add_subplot(111)
    if df.empty:
        raise ValueError
    if (
        self.callerGenderDropdown.isEnabled()
        and self.receiverGenderDropdown.isEnabled()
    ):
        if radio_type == "occurrences":
            result = dm.occurrence_of_each_event(df, cue_types)
            ax.set_title("Total Cue Occurrences")
            ax.set_ylabel("Total Number of Occurrences")
        else:
            result = dm.total_time_of_each_event(df, cue_types)
            ax.set_title("Total Cue Duration")
            ax.set_ylabel("Total Duration")
    elif not self.callerGenderDropdown.isEnabled():
        result = {}
        for cue in cue_types:
            if radio_type == "occurrences":
                cue_result = dm.occurrence_of_event(df, cue)
            else:
                cue_result = dm.total_time_of_event(df, cue)
            result[cue] = cue_result[
                0
            ]  # This gets the occurrence of each cue of the caller
        if "silence" in result:
            result.pop(
                "silence"
            )  # Remove silence since this applies for both parties, not individually
        if radio_type == "occurrences":
            ax.set_title("Total Cue Occurrences for Receivers")
            ax.set_ylabel("Total Occurrences")
        else:
            ax.set_title("Total Cue Duration for Receivers")
            ax.set_ylabel("Total Duration")
    else:
        result = {}
        for cue in cue_types:
            if radio_type == "occurrences":
                cue_result = dm.occurrence_of_event(df, cue)
            else:
                cue_result = dm.total_time_of_event(df, cue)
            result[cue] = cue_result[
                1
            ]  # This gets occurrence of each cue of the receiver
        if "silence" in result:
            result.pop("silence")
        if radio_type == "occurrences":
            ax.set_title("Total Cue Occurrences for Callers")
        else:
            ax.set_title("Total Cue Duration for Callers")
    if self.averageCheckbox.isChecked():
        for cue in result:
            result[cue] = result[cue] / len(dm.get_all_call_ids(df))
        ax.set_title("Average " + ax.get_title() + " Per Call")
        ax.set_ylabel("Average " + ax.get_ylabel())
    ax.bar(result.keys(), result.values())
    ax.set_xlabel("Cue")
