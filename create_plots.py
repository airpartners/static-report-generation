"""
Author: Neel Dhulipala
Project: Air Partners

Script for creating and exporting all figures needed for static reporting.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from visualizers.calendar_plot import CalendarPlot
from visualizers.timeplot_thresholds import Timeplot
from data_analysis.dataviz import OpenAirPlots

def calendar_plot(data_PM, month, year):
    # Reformat data so only data from that month is plotted
    data_PM = data_PM.set_index('timestamp_local').resample('1D').mean()
    data_PM = data_PM[data_PM['month'] == month]
    
    # Create calendar plot
    cal = CalendarPlot(year, month)
    cal.add_pm_vals(data_PM)
    cal.show()


def timeplot_threshold(data_PM):
    # Initialize and create timeplot
    tp = Timeplot(data_PM)
    tp.show()


def time_of_day_plot(dataPM):
    dataPM_10min = dataPM.set_index('timestamp_local').resample('10T').mean()
    dataPM_10min['hour_minute'] = dataPM_10min.index.strftime('%H:%M')
    dataPM_10min = dataPM_10min.groupby('hour_minute').mean()

    fig,axes=plt.subplots(1,1,figsize=(8,5))
    axes.plot(dataPM_10min.index,dataPM_10min.pm1, label = 'PM 1')
    axes.plot(dataPM_10min.index,dataPM_10min.pm25, label = 'PM 2.5')
    axes.plot(dataPM_10min.index,dataPM_10min.pm10, label = 'PM 10')
    axes.xaxis.set_major_locator(MaxNLocator(15.8)) 
    axes.legend()
    axes.set_ylabel("[μg/m³]")
    for tick in axes.get_xticklabels():
        tick.set_rotation(45)


def daily_average_plot(dataPM):
    dataPM_day = dataPM.set_index('timestamp_local').resample('1D').mean()
    plt.style.use('ggplot')

    _,axes=plt.subplots(1,1,figsize=(8,5))
    axes.plot(dataPM_day.pm1, label = 'PM 1')
    axes.plot(dataPM_day.pm25, label = 'PM 2.5')
    axes.plot(dataPM_day.pm10, label = 'PM 10')
    axes.set_ylabel("[μg/m³]")  
    axes.legend()
    for tick in axes.get_xticklabels():
        tick.set_rotation(45)


def _replace_with_iem(df, iem_df, is_tz_aware=True):
        """
        Wind speed and wind direction from the QuantAQ sensors are unreliable so we replace them with data from
        the IEM meteorology sensors.
        :param df: (pd.DataFrame) dataframe containing sensor data
        :param iem_df: (pd.DataFrame) dataframe containing meteorology data
        :param is_tz_aware: (optional bool) True if the raw, string representations of timestamps in df are time zone-aware
        """
        #convert str representation of timestamps to datetime
        iem_df = iem_df.assign(timestamp=pd.to_datetime(iem_df['valid']))

        #IEM data is recorded once every 5 mins, quantAQ data recorded once per minute, need to fill in rows in IEM data
        # to match quantAQ. So, for every IEM timestamp, we add 4 copies of the IEM data so that the IEM and QuantAQ dataframes
        # have the same number of rows:

        #create new timestamp column that matches the timestamps for the quantAQ data
        start, end = df.timestamp.min(), df.timestamp.max()
        if not is_tz_aware:
            start, end = start.tz_localize(None), end.tz_localize(None)
        dates = pd.date_range(start=start, end=end, freq='1Min')
        #fill new empty rows with the last valid value
        iem_df['timestamp'] = iem_df['timestamp'].dt.round('1Min') # this operation sometimes adds duplicates by rounding to the same minute.
        iem_df = iem_df.set_index('timestamp')
        # delete duplicate timestamps before reindexing, or pandas complains
        iem_df = iem_df.loc[~iem_df.index.duplicated(), :]

        #reindex meteorology data to match original dataframe
        iem_df = iem_df.reindex(dates, method='pad')

        #convert timestamp index back into a column
        iem_df = iem_df.reset_index().rename(columns={"index": "timestamp"})
        #some values might be NaN due to timestamp mismatch, fill them with the next valid value
        iem_df = iem_df.fillna(method='bfill')

        #assign the new wind direction and wind speed columns to the quantAQ dataframe
        df = df.assign(wind_dir=iem_df['drct'])
        df = df.assign(wind_speed=iem_df['sped'] * (1609/3600))  #converting to m/s, 1609 meters per mile, 3600 seconds per hr
        return df

def wind_polar_plot(data_PM, month, iem_df):
    # Get data only from specified month
    data_PM = data_PM[data_PM['month'] == month]

    # Add wind variables to df
    data_PM = _replace_with_iem(data_PM, iem_df)
    
    #df = df.rename(columns={"timestamp_local": "date", "wind_speed": "ws", "wind_dir": "wd"})
    #df.wd = df.wd.replace(0.0, 360.0)
    df = data_PM[['timestamp_local', 'wind_speed', 'wind_dir', 'pm25']]
    # Format the dataPM to be read in R and plot wind data
    air_plt = OpenAirPlots()
    air_plt.polar_plot(df, '2022-04/Graphs/wind_polar_plot/', ['pm25'])
    #ro.r.polarPlot(dataPM, pollutant = p, main = f"{p.upper()} Polar Plot")
    
    # Take current image, save image again using matplotlib
    img = plt.imread(fname='2022-04/Graphs/wind_polar_plot/_polar_pm25.png')
    plt.figure()
    plt.imshow(img)
    plt.grid(None)
    plt.xticks([])
    plt.yticks([])


class Plotter(object):

    def __init__(self, year_month, sn_list, sn_dict):
        self.year_month = year_month
        self.sn_list = sn_list
        self.sn_dict = sn_dict


    def plot_and_export(self, plot_function, *args, **kwargs):
        try:
            os.mkdir('{}'.format(self.year_month))
        except:
            pass
        try:
            os.mkdir('{}/Graphs/'.format(self.year_month))
        except: 
            pass
        try:
            os.mkdir('{}/Graphs/'.format(self.year_month)+str(plot_function.__name__))
        except: # Forgive my crime here, but it just avoids errors if the directory already exists
            pass
        for sn in self.sn_list:
            if not self.sn_dict[sn].empty:
                plot_function(self.sn_dict[sn], *args, **kwargs)
                plt.savefig('{1}/Graphs/{2}/{0}_{1}_{2}.jpeg'.format(sn, self.year_month, str(plot_function.__name__)), bbox_inches='tight',dpi = 300)
