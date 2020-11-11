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


class Model:
    def __init__(self):
        self.fileContents = ""
        self.fileName = None
        self.fileContent = ""

    def set_file_name(self, file):
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
