# Conversational Data Browser

[![YourActionName Actions Status](https://github.com/Euronite/ConversationalBrowser/workflows/unit-test-and-lint/badge.svg)](https://github.com/Euronite/ConversationalBrowser/actions)

Level 4 Individual Project

## Installation Guide

You  may want to use a virtual environment.

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

### Windows

* Update pip using `pip install --upgrade pip`
* A couple of ways. Recommended way is to have Anaconda installed.
* In the Anaconda Prompt navigate to the folder containing requirements.txt
  and run `pip install -r requirements.txt`. Filelock installation error
  may occur but shouldn't affect the running of the program.
* Then do python main.py

### Troubleshooting

* If there is a marshal data too short error, try
  `pip3 install --upgrade --force-reinstall <package that is not working on>`.
  If this fails, it probably means your pip installation is broken. Follow the
  relevant uninstall/reinstall guides
  for your system.
* Mac systems might have some issues with pip installation of packages.
  The workaround is to install the packages manually and ignore the version
  number.
