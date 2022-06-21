"""
Author: Neel Dhulipala
Project: Air Partners

Prototype of static reporting pipeline. Used primarily for testing scripts (for now).
"""

from data_import import DataImporter
from create_plots import *

# STATICS (for testing)
YEAR = 2022
MONTH = 4

# import sensor data
di = DataImporter(year=YEAR, month=MONTH)
sn_list, sn_dict = di.get_PM_data()
iem_df = di.get_iem_data()

# create date string for data storage
date_str = str(YEAR) + '-0' + str(MONTH) if MONTH<=9 else str(YEAR) + '-' + str(MONTH)

# plot graphs
pl = Plotter(date_str, sn_list, sn_dict)
pl.plot_and_export(calendar_plot, month=MONTH, year=YEAR)
pl.plot_and_export(timeplot_threshold)
pl.plot_and_export(time_of_day_plot)
pl.plot_and_export(daily_average_plot)
pl.plot_and_export(wind_polar_plot, month=MONTH, iem_df=iem_df)