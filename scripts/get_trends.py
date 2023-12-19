"""
    Determine and illustrate relative frequency of searches on rugby, football and tennis.

    Either data scrape the trend data (till Google tells us no more) or download it from the
    website as a csv file and then load it separately.

    Display in line or bar graph format and either by day or overall for the entire period.
"""
import sys
import argparse

from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
import pandas as pd
from pandas.errors import EmptyDataError

# shared key values
OVERALL = "overall"
PLOT_TYPE = "plot_type"
CSV_FILE = "csv_file"


def plot(graph_type, searches_pd, data_to_plot):
    """Display a plot of the data provided, either as a line diagram or as a bar graph"""
    pd.options.plotting.backend = "plotly"

    fig = searches_pd[data_to_plot].plot.bar() if graph_type == 'bar' \
        else searches_pd[data_to_plot].plot()
    fig.update_layout(
        title_text='Search volume for Rugby football and tennis',
        legend_title_text='Search terms'
    )
    fig.show()


def do_data_scrape():
    """ Use pytrends package to retrieve the data on search frequency"""

    # define the terms for which we will be looking for search frequency
    kw_list = ['rugby', 'football', 'tennis']

    # Configuring connection
    pytrend = TrendReq()

     # Building payload where we request for the last three months
    pytrend.build_payload(kw_list=kw_list, timeframe='today 3-m')

    # Interrogate google trends via pytrend, respnse error means google is grumpy
    try:

        results = pytrend.interest_over_time().drop(columns='isPartial')

        if results is not None:
            column_names = list(results.columns.values)
        else:
            column_names = []

        return results, column_names

    except ResponseError:
        print("Google is on to us.. try later")
        return None, []


def process_csv_input(file_name):
    """Process the given csv file and retrieve the data as a panda data frame"""
    try:
        results = pd.read_csv(file_name, skiprows=[0, 1])
    except OSError as os_error:
        print(f"Unable to open {file_name}: {os_error}", file=sys.stderr)
        return None, []
    except EmptyDataError as de_error:
        print(f"Invalid data in file {file_name}, error: {str(de_error)}")
        return None, []

    column_names = list(results.columns.values)
    # first column is the x-axes value, the rest are the variables to plot
    vars_to_plot = column_names[1:]

    return results, vars_to_plot


def get_configuration():
    """Obtain the parameters passed to us and decide what we are drawing, data source etc"""
    parser = argparse.ArgumentParser(description="Compare trending terms.. web scrape or from csv",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-c", "--csv", help="Name of CSV file, otherwise will web scrape")
    parser.add_argument("-p", "--plot", help="type of plot, specify line or bar")
    parser.add_argument("-o", "--overall", action='store_true', help="Summarize across date range")

    args = parser.parse_args()

    if args.plot and args.plot not in ["line", "bar"]:
        print("Sorry, plot type must be line or bar")
        return None

    settings = {
        OVERALL: bool(args.overall),
        PLOT_TYPE: args.plot if args.plot else "line",
        CSV_FILE: args.csv if args.csv else ""
    }
    return settings


def run_script():
    """get configuration info, data scrape or obtain data from csv and plot"""

    config = get_configuration()

    if config is None:
        return "failed"

    csv = config[CSV_FILE]

    # Process csv data if we were told about it, otherwise we must data scrape
    searches, variables = process_csv_input(csv) if csv else \
        do_data_scrape()

    if searches is None:
        print("Sorry no data received")
        return "failed"

    # Do we want overall summary over the entire time frame or on a daily basis?
    if config[OVERALL]:
        totals = []
        for variable in variables:
            totals.append(searches[variable].sum())

        overall_df = pd.DataFrame({"Totals": totals}, index=variables)

        plot(config[PLOT_TYPE], overall_df, "Totals")
    else:
        plot(config[PLOT_TYPE], searches, variables)

    return "OK"

if __name__ == "__main__":
    RESULT = run_script()
    if RESULT != "OK":
        sys.exit(1)
