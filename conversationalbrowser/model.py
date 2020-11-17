#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This holds the model object which is essentially the dataframe that can then be passed to the data_manipulation files.
"""

import pandas as pd
from conversationalbrowser import data_manipulation as dm


def is_valid(file):
    """
    Returns True if the file exists and can be opened.  Returns False otherwise.
    """
    try:
        file = open(file, "r")
        file.close()
        return True
    except FileNotFoundError:
        return False


class CallerModel:
    def __init__(self):
        self.selected = []

    def set_selected_items(self, id_list):
        self.selected = id_list


class Model:
    def __init__(self):
        self.fileContents = ""
        self.fileName = None
        self.fileContent = ""
        self.callerIds = []

    def set_file_name(self, file):
        """
        :param file: file name to retrieve contents from
        """
        if is_valid(file):
            self.fileName = file
            self.fileContents = pd.read_csv(file, names=dm.header_names)
        else:
            self.fileName = ""

    def get_file_content(self):
        """
        Gets the file content data
        :return: dataframe
        """
        return self.fileContents

    def set_caller_ids(self, id_list):
        self.callerIds = id_list
