def is_valid(file):
    """
    returns True if the file exists and can be
    opened.  Returns False otherwise.
    """
    try:
        file = open(file, "r")
        file.close()
        return True
    except FileNotFoundError:
        return False


class Model:
    def __init__(self):
        """
        Initializes the two members the class holds:
        the file name and its contents.
        """
        self.fileContents = ""
        self.fileName = None
        self.fileContent = ""

    def set_file_name(self, file):
        """
        sets the member fileName to the value of the argument
        if the file exists.  Otherwise resets both the filename
        and file contents members.
        """
        if is_valid(file):
            self.fileName = file
            self.fileContents = open(file, "r").read()
        else:
            self.fileName = ""

    def get_file_name(self):
        """
        Returns the name of the file name member.
        """
        return self.fileName
