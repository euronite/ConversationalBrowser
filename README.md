# Conversational Data Browser

[![YourActionName Actions Status](https://github.com/Euronite/ConversationalBrowser/workflows/unit-test-and-lint/badge.svg)](https://github.com/Euronite/ConversationalBrowser/actions)

Level 4 Individual Project

main.py is the file that should be run to start the application.
The conversationalbrowser/ folder contains the user
interface files under the folder ui/. The folder also contains three python files.
data_manipulation.py is how
the application extracts required data from the dataset, graph.py which controls
the displaying of the graphs, and the model which contains the classes that
hold the various data.

## Build instructions

### Requirements

* Python 3.7 and above. May work for Python 3.5 and 3.6 but has not been tested.
* Packages: listed in `requirements.txt`
* pip3 installed. This comes automatically using Anaconda on Windows.
* Default file explorer. Windows, OSX and Ubuntu already have this installed by default.
* Tested using an Anaconda virtual environment on Windows 10
  (may need to install Anaconda) for ease of use.
* Tested on Ubuntu Linux 20.10. Should work on older versions.

### Linux

* Update pip using either `pip3 install --upgrade pip` or `pip install
  --upgrade pip` on what is being used.
* Ensure you have pip3 installed and Python 3.X. This has been tested
  with 3.7 and 3.8.
* Download the files using either the code download as zip or git clone.
* In terminal, same folder as the main.py and requirements.txt, run
  `pip3 install -r requirements.txt` or
  `pip install -r requirements.txt` (depending on version).
* Then do python main.py
* To edit the user interface using QtDesigner, do
  `cd /usr/lib/x86_64-linux-gnu/qt5/bin/` to get to the folder
  containing QtDesigner and then run `./designer`.

### Windows

* Update pip using `pip install --upgrade pip`
* A couple of ways. Recommended way is to have Anaconda installed.
* In the Anaconda Prompt navigate to the folder containing requirements.txt
  and run `pip install -r requirements.txt`. Filelock installation error
  may occur but shouldn't affect the running of the program.
* Then do python main.py
* To run the QtDesigner to change the UI, designer.exe will be under `....Lib\site-packages\pyqt5_tools`

### Test Steps

* Testing is automated if the code is hosted on Github, using Github Actions.
* Testing can be run locally by executing `pytest --cov=./ tests/` in the root directory.

## Documentation

Docs for the code can be found in the repository as a html file under html/index.html

### Troubleshooting

* If there is a marshal data too short error, try
  `pip3 install --upgrade --force-reinstall <package that is not working on>`.
  If this fails, it probably means your pip installation is broken. Follow the
  relevant uninstall/reinstall guides
  for your system.
* Mac systems might have some issues with pip installation of packages.
  The workaround is to install the packages manually and ignore the version
  number.
