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
from numpy import arange

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

    if self.occurrencesRadioBtn.isChecked():
        if self.chartDropdown.currentText() == "Display Totals":
            display_barchart(self, df, cue_types, ax, "occurrences")
        else:
            get_occurrences_per_call(self, df, cue_types, ax)
    else:
        if self.chartDropdown.currentText() == "Display Totals":
            display_barchart(self, df, cue_types, ax, "durations")
        else:
            display_histogram(self, df, cue_types, ax, "durations")


    # Display the actual graph
    self.mplvl.removeWidget(self.canvas)
    self.canvas.close()
    self.canvas = FigureCanvas(fig)
    self.mplvl.addWidget(self.canvas)
    self.canvas.draw()

def get_occurrences_per_call(self, df, cue_types, ax):
    """
    This will get the occurrences for all 160 callers of the cues
    :return:
    """
    cue_names = cue_types.keys()
    cue_results = []
    ids = dm.get_all_call_ids(df)
    for cue in cue_names:
        cue_results_temp = []
        for call in ids:
                cue_results_temp.append(dm.occurrence_of_event(dm.get_call_df(df, call), cue))
        if self.callerGenderDropdown.isEnabled() and self.receiverGenderDropdown.isEnabled():
            cue_results.append(sorted([val for sublist in cue_results_temp for val in sublist]))
        elif self.callerGenderDropdown.isEnabled():
            # so this is if caller is enabled, but not receiver. Remove every second since thats receiver data
            sorted_list = sorted([val for sublist in cue_results_temp for val in sublist])
            del sorted_list[1:2]
            cue_results.append(sorted_list)
        else:
            # receiver only info. Remove any caller data
            sorted_list = sorted([val for sublist in cue_results_temp for val in sublist])
            del sorted_list[::2]
            cue_results.append(sorted_list)

    ax.set_title("Occurrences of Cue For Each Caller")
    ax.set_xlabel("Caller Number")
    ax.set_ylabel("Total Times Occurred")
    X = arange(len(cue_results[0]))
    if len(cue_results) == 1:
        ax.bar(X, cue_results[0])
        return
    step = 0.00
    for cue in cue_results:
        ax.bar(X + step, cue, width=0.4)
        step += 0.4
    ax.legend(cue_names, loc=2)


def display_barchart(self, df, cue_types, ax, radio_type):
    if self.callerGenderDropdown.isEnabled() and self.receiverGenderDropdown.isEnabled():
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
            try:
                if radio_type == "occurrences":
                    cue_result = dm.occurrence_of_event(df, cue)
                else:
                    cue_result = dm.total_time_of_event(df, cue)
            except ValueError:
                return
            result[cue] = cue_result[0]  # This gets the occurrence of each cue of the caller
        if "silence" in result:
            result.pop("silence")  # Remove silence since this applies for both parties, not individually
        if radio_type == "occurrences":
            ax.set_title("Total Cue Occurrences for Receivers")
            ax.set_ylabel("Total Occurrences")
        else:
            ax.set_title("Total Cue Duration for Receivers")
            ax.set_ylabel("Total Duration")
    else:
        result = {}
        for cue in cue_types:
            try:
                if radio_type == "occurrences":
                    cue_result = dm.occurrence_of_event(df, cue)
                else:
                    cue_result = dm.total_time_of_event(df, cue)
            except ValueError:
                return
            result[cue] = cue_result[1]  # This gets occurrence of each cue of the receiver
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


def display_histogram(self, df, cue_types, ax, radio_type):
    if self.callerGenderDropdown.isEnabled() and self.receiverGenderDropdown.isEnabled():
        if radio_type == "occurrences":
            results = []  # this will hold the results for each cue type
            all_ids = dm.get_all_call_ids(df)
            for cue in cue_types:
                # for each cue, get the occurrences per call, sort and add the results to results var.
                result = []
                for call in all_ids:
                    # remove caller or receiver if that is disabled
                    sub_result = dm.occurrence_of_event(dm.get_call_df(df, call), cue)

                    if self.callerGenderDropdown.isEnabled() and self.receiverGenderDropdown.isEnabled() == False:
                        for res in sub_result:
                            res.pop(0)
                    elif self.callerGenderDropdown.isEnabled() == False and self.receiverGenderDropdown.isEnabled():
                        for res in sub_result:
                            res.pop(1)
                    result.append(sub_result)
                # sort list and flatten results
                results.append(sorted([val for sublist in result for val in sublist]))
            w = -0.2
            for each_cue, cue_name in zip(results, cue_types):
                ax.bar(arange(len(each_cue)) + w, each_cue, width=0.2, align="center")
                w += 0.2
