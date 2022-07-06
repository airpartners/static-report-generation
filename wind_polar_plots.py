"""
Author: Neel Dhulipala
Project: Air Partners

Prototype of static reporting pipeline. Makes wind polar plots, which are very
computationally expensive.
"""

from calendar import weekday
import sys
from import_data import DataImporter
from utils.create_plots import *
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

# wind polar plots (computationally expensive)
pl.plot_and_export(wind_polar_plot, pm='pm1')
pl.plot_and_export(wind_polar_plot, pm='pm25')
pl.plot_and_export(wind_polar_plot, pm='pm10')
print('Wind polar plots plotted')
plt.close()