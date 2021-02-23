#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This holds the model object which is essentially the dataframe that can then be passed to the data_manipulation files.
"""
from pandas import read_csv
from conversationalbrowser import data_manipulation as dm


def is_valid(file):
    """ Returns True if the file exists and can be opened.  Returns False otherwise. """
    try:
        file = open(file, "r")
        file.close()
        return True
    except FileNotFoundError:
        return False


def input_is_valid(df) -> bool:
    """ This checks the input and ensures it is in the correct format. """
    if len(df.columns) != 5:
        return False
    return True


class CallerModel:
    """ This holds the data for caller id dialog selections, as well as cues selected. """

    def __init__(self):
        self.selected = []
        self.cues_selected = []

    def set_selected_items(self, id_list):
        self.selected = id_list


class Model:
    """ This holds the file contents of the csv as a dataframe, and also the graph figure. """

    def __init__(self):
        self.fileContents = None
        self.fileName = None
        self.callerIds = []
        self.figure = None

    def set_file_name(self, file: str):
        """
        This sets the file name and reads in the data, while modifying the dataframe to include receiever and caller
        columns for easier data processing.
        :param file: file name to retrieve contents from
        """
        if is_valid(file):
            self.fileName = file
            self.fileContents = read_csv(file, names=dm.header_names)
            if input_is_valid(self.fileContents):
               self.fileContents = dm.receiver_and_caller_column(self.fileContents)
            else:
                raise Exception("File incorrectly formatted! Please check that it has these columns: call id, topic, "
                                "person with cue type, start time, end time.")
        else:
            self.fileName = ""

    def get_file_content(self):
        """
        Gets the file content data
        :return: dataframe
        """
        return self.fileContents

    def set_caller_ids(self, id_list: list):
        self.callerIds = id_list

    def set_figure(self, fig):
        self.figure = fig
