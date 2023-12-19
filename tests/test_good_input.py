"""Run positive tests such as drawing a graph from csv data"""

import pytest
from scripts.get_trends import get_configuration, run_script

def test_good_input(mocker):
    """check that drawing up a graph from a csv file works OK"""
    config = {'overall': None, "plot_type": "line", "csv_file": "testdata.csv"}
    mocker.patch("scripts.get_trends.get_configuration", return_value=config)
    assert run_script() == 'OK'