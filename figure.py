"""
Author: Neel Dhulipala
Project: Air Partners

File to create singular files when needed. 
To run from command line, activate virtual environment, then run:

        $ python3 figure.py <YEAR> <MONTH> <FIGURE_TYPE> <SENSOR_ID> <PM>

Where <YEAR> and <MONTH> are replaced with the appropriate year and month from
when the data is from, <FIGURE_TYPE> is replaced with the name of the function
that creates the figure you want to create, <SENSOR_ID> is replaced with the
sensor where the data is from, and <PM> is replaced with the PM you want to analyze.

This dictionary should be used for identifying which PM to use:
- PM 1: 'pm1'
- PM 2.5: 'pm25'
- PM 10: 'pm10'

If you choose to make a timeplot, which includes the plots for all three PMs, set <PM>
to None.
"""

import pandas as pd
import matplotlib.pyplot as plt
from calendar import monthrange
from datetime import datetime
import data_analysis.quantaq_pipeline as qp
from utils.create_plots import *
import sys

# Following _ functions are helpers that call plotting functions
def _calendar(df, pm, month, year):
        calendar_plot(df, pm=pm, month=month, year=year)

def _wind(df, pm, month, year):
        wind_polar_plot(df, pm)

def _timeplot(df, pm, month, year):
        timeplot_threshold(df)

def _diurnal(df, pm, month, year):
        diurnal_plot(df, pm)

# Downloads data from designated timeframe and plots it using designated plot function
def create_singular_figure(year, month, plot_function, sensor, pm):
        """
        Creates figure of your choice and plots it.

        Args:
                year: (int) year of when you want data from
                month: (int) month of year where you want data from
                plot_function: (string) type of plot you want to generate
                sensor: (string) the sensor you want to pull data from
                pm: (string) particulate matter you want to plot (if plot_function is timeplot_thresholds, pm=None)
        """
        # parsing variables
        year = int(year)
        month = int(month)
        func_dict = {'calendar_plot': _calendar, 
                     'timeplot_threshold': _timeplot,
                     'wind_polar_plot': _wind,
                     'diurnal_plot': _diurnal}
        plot_function = func_dict[plot_function]

        def _get_start_end_dates(year_int_YYYY, month_int):
                # get number of days in month_int of that year
                no_of_days = monthrange(year_int_YYYY, month_int)[1]
                # get start and end dates in type datetime
                start_date = datetime(year_int_YYYY, month_int, 1)
                end_date = datetime(year_int_YYYY, month_int, no_of_days)
                return start_date, end_date


        start_date, end_date = _get_start_end_dates(2022, 6)
        mod_handler = qp.ModPMHandler(start_date=start_date, end_date=end_date)

        df = mod_handler.load_df(sensor, start_date, end_date)

        plot_function(df, pm, month, year)
        plt.show()

if __name__=='__main__':
        create_singular_figure(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
