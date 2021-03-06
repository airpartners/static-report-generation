#!/bin/sh

:<<'END'

Author: Neel Dhulipala
Project: Air Partners

Shell script to run pipeline. Imports data through API, creates plots and organizing them, and
generating reports from those visualizations. Shell is used for saving memory between running
different Python files, increasing efficiency, and Shell's date module is useful for getting
the last month and year of data collection.

END

# # get last month
month=$(date -d "last month" '+%m')

# get year
year=$(date '+%Y')
# if last month was December, then we are in previous year
[ $month -eq "12" ] && ((year--)) || year=$year

echo "Date": $year-$month

# import data
python3 import_data.py $year $month
sleep 5

# create plots
python3 plots.py $year $month
sleep 5

# generate reports (computationally expensive)
python3 report_generation.py $year $month
sleep 5

# send automatic email with zip file
python3 send_email.py $year $month
sleep 2

# delete year-month folder and zip files locally
rm -rf $year-$month
rm -rf zips/*
