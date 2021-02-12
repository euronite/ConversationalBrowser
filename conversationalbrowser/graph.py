#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This holds the functions to draw the graph on the user interface using matplotlib.
"""
from PyQt5.QtWidgets import QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams as mpl_rcParams
from matplotlib import use as mpl_use
from conversationalbrowser import data_manipulation as dm
from numpy import arange, concatenate
from pandas import concat as pd_concat
import matplotlib.pyplot as pyplot
pyplot.style.use('fivethirtyeight')
mpl_rcParams.update({'font.size': 10})
mpl_use("Qt5Agg")


def export(self, location):
    """
    Exports graph in the location user specifies
    :param self:
    :param location:
    :return:
    """
    try:
        self.model.figure.savefig(location)
    except IOError:
        raise


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


def displaympl(self, model, call_model):
    """
    This is used to display the graph upon Display button click.
    :param call_model:
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
    df, cue_types = get_df(self, call_model, df)
    try:
        if df.empty:
            error_dialog("Caller/Receiver Combination Not Found")
        elif self.occurrencesRadioBtn.isChecked():
            if self.chartDropdown.currentText() == "Display Totals":
                get_total_cue_data(self, df, cue_types, fig, "occurrences")
            else:
                get_occurrences_per_call(self, df, cue_types, fig)
        else:
            if self.chartDropdown.currentText() == "Display Totals":
                get_total_cue_data(self, df, cue_types, fig, "durations")
            else:
                get_duration_per_call(self, df, cue_types, fig)
    except Exception as e:
        error_dialog(f"Exception occurred: {e}")

    # Display the actual graph
    self.mplvl.removeWidget(self.canvas)
    self.canvas.close()
    self.canvas = FigureCanvas(fig)
    self.mplvl.addWidget(self.canvas)
    self.canvas.draw()
    model.set_figure(fig)


def get_df(self, call_model, df):
    """
    This gets the dataframe which has the parameters which the data is constrained by. Returns dataframe of what to use.
    :param self:
    :param call_model:
    :param df:
    :return:
    """
    # Get the dataframe of relevant call IDs
    if call_model.selected[0][1] != 0:
        df = dm.get_list_of_call_id_df(df, [i[0] for i in call_model.selected])

    # Get relevant genders and the corresponding dataframe
    caller_gender = self.callerGenderDropdown.currentText()
    receiver_gender = self.receiverGenderDropdown.currentText()

    caller, receiver = None, None
    if caller_gender == "Caller Male":
        caller = "caller_M"
    elif caller_gender == "Caller Female":
        caller = "caller_F"
    if receiver_gender == "Receiver Female":
        receiver = "receiver_F"
    elif receiver_gender == "Receiver Male":
        receiver = "receiver_M"
    df = dm.get_rows_by_caller_and_receiver(df, caller, receiver)

    # Get the cue types
    cue_types = {}
    temp_df = []
    for cue_pair in call_model.cues_selected:
        cue = cue_pair[0]
        if cue == "All Cues":
            cue_types = {"filler": 0, "laughter": 0, "silence": 0, "bc": 0}
            break
        if cue == "Back-channel":
            cue = "bc"
        cue = cue.lower()
        cue_types[cue] = 0
        temp_df.append(dm.get_non_verbal_speech_only(df, cue))
    # Get the cue data and concatenate to make final df
    if temp_df:
        df = pd_concat(temp_df)

    return df, cue_types


def error_dialog(message):
    dialog = QMessageBox()
    dialog.setText(message)
    dialog.setStandardButtons(QMessageBox.Ok)
    dialog.setIcon(QMessageBox.Critical)
    dialog.exec_()


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
    x = arange(len(cue_results[0]))
    ax = []
    for index, cue in enumerate(cue_results):
        if len(cue_names) == 1:
            ax.append(fig.add_subplot(111))
        else:
            ax.append(fig.add_subplot(2, 2, index + 1))
        ax[index].set(xlabel="Participant Number", ylabel="Total Occurrences Count")
        ax[index].set_title(cue_names[index])
        ax[index].bar(x, cue)

    fig.subplots_adjust(hspace=0.4, wspace=0.3)
    fig.suptitle("Total Occurrences for All Participants")


def get_total_cue_data(self, df, cue_types, fig, radio_type):
    ax = fig.add_subplot(111)
    average = self.averageCheckbox.isChecked()
    caller_or_receiver = False
    if (
        self.callerGenderDropdown.isEnabled()
        and self.receiverGenderDropdown.isEnabled()
    ):
        if radio_type == "occurrences":
            result = dm.occurrence_of_each_event(df, cue_types)
        else:
            result = dm.total_time_of_each_event(df, cue_types)
    elif not self.callerGenderDropdown.isEnabled():
        caller_or_receiver = "Receivers"
        result = {}
        for cue in cue_types:
            if radio_type == "occurrences":
                cue_result = dm.occurrence_of_event(df, cue)
            else:
                cue_result = dm.total_time_of_event(df, cue)
            # This gets the occurrence of each cue of the caller
            result[cue] = cue_result[0]
    else:
        caller_or_receiver = "Callers"
        result = {}
        for cue in cue_types:
            if radio_type == "occurrences":
                cue_result = dm.occurrence_of_event(df, cue)
            else:
                cue_result = dm.total_time_of_event(df, cue)
            # This gets occurrence of each cue of the receiver
            result[cue] = cue_result[1]

    if average:
        for cue in result:
            result[cue] = result[cue] / len(dm.get_all_call_ids(df))
    ax.bar(result.keys(), result.values())
    set_label(ax, caller_or_receiver, radio_type, average)


def set_label(ax, caller_or_receiver, radio_type, average):
    title = ""
    x_label = "Cue"
    y_label = ""
    if radio_type == "occurrences":
        title += "Total Cue Occurrences"
        y_label += "Total Number of Occurrences"
    else:
        title += "Total Cue Duration"
        y_label += "Total Duration (s)"

    if caller_or_receiver:
        title += " for " + caller_or_receiver

    if average:
        title = f"Average {title} Per Call"
        y_label = f"Average {y_label}"

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
