**Introduction**

Contains a python script called get_trends.py which uses the pytrends library module
to obtain data from the google trends website:

https://trends.google.com/trends/

Currently this compares the number of searches over three months of the rugby, football and tennis
search terms. Either the relative number of searches over the three months can be displayed or the variation over time during those three months. Additionally line or bar graps can be displayed.
Please see usage instructions below. 

As google deoes not support automated scraping of data and periodically throws errors if too many
searches are carried out, the script also supports displaying data from a csv file which can be
obtained from the website manually. Other terms could be searched if desired.

Note that versions before python3 are not supported by the script

**Installation**

You are advised to create a virtual environemt

python3 -m venv venv

Then activate the environment:

source venv/bin/activate (on windows .\venv\scripts\activate.bat)

Install production dependencies:

pip install -r installation.txt

Install test code dependencies:

pip install -r installation-test.txt

**Usage Instructions**

usage: get_trends.py [-h] [-c CSV] [-p PLOT] [-o]

Compare trending terms.. web scrape or from csv

optional arguments:
  -h, --help            show this help message and exit
  -c CSV, --csv CSV     Name of CSV file, otherwise will web scrape (default: None)
  -p PLOT, --plot PLOT  type of plot, specify line or bar (default: line)
  -o, --overall         Summarize across date range (default: False)

**Testing**

Script code has been (py)linted.

Dynamic tests can be invoked from the command line by using the "pytest" command.