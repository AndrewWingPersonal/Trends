"""Test that we fail gracefully when bad input provided"""

import pytest
from scripts.get_trends import get_configuration, run_script

def test_no_valid_config(mocker):
    """test that we fail gracefully when no valid config"""
    mocker.patch("scripts.get_trends.get_configuration", return_value=None)
    assert run_script() == 'failed'
 
def test_no_valid_csv_file(mocker):
    config = {'overall': None, "plot_type": "line", "csv_file": "does_not_exist.csv"}
    mocker.patch("scripts.get_trends.get_configuration", return_value=config)
    assert run_script() == 'failed'

def test_no_csv_in_file(mocker):
    config = {'overall': None, "plot_type": "line", "csv_file": "contents_invalid.csv"}
    mocker.patch("scripts.get_trends.get_configuration", return_value=config)
    assert run_script() == 'failed'

   