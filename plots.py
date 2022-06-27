"""
Author: Neel Dhulipala
Project: Air Partners

Prototype of static reporting pipeline. Used primarily for testing scripts (for now).
"""

import sys
from import_data import DataImporter
from create_plots import *
from report_generation import generate_report
import data_analysis.quantaq_pipeline as qp
from datetime import datetime


# STATICS
YEAR = int(sys.argv[1])
MONTH = int(sys.argv[2])

# Import sensor data
di = DataImporter(year=YEAR, month=MONTH)
sn_list, sn_dict = di.get_PM_data()


# create date string for data storage
date_str = str(YEAR) + '-0' + str(MONTH) if MONTH<=9 else str(YEAR) + '-' + str(MONTH)

# plot graphs
pl = Plotter(date_str, sn_list, sn_dict)

# calendar plots
pl.plot_and_export(calendar_plot, pm='pm1', month=MONTH, year=YEAR)
pl.plot_and_export(calendar_plot, pm='pm25',month=MONTH, year=YEAR)
pl.plot_and_export(calendar_plot, pm='pm10',month=MONTH, year=YEAR)
print('Calendars plotted')
plt.close()

# timeplots with thresholds
pl.plot_and_export(timeplot_threshold, pm=None)
print('Timelines plotted')
plt.close()

# diurnal plots
pl.plot_and_export(diurnal_plot, pm='pm1')
pl.plot_and_export(diurnal_plot, pm='pm25')
pl.plot_and_export(diurnal_plot, pm='pm10')
print('Diurnals plotted')
plt.close()

# wind polar plots (computationally expensive)
pl.plot_and_export(wind_polar_plot, pm='pm1')
pl.plot_and_export(wind_polar_plot, pm='pm25')
pl.plot_and_export(wind_polar_plot, pm='pm10')
print('Wind polar plots plotted')
plt.close()
