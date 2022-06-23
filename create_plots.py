"""
Author: Neel Dhulipala
Project: Air Partners

Script for creating and exporting all figures needed for static reporting.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from visualizers.calendar_plot import CalendarPlot
from visualizers.timeplot_thresholds import Timeplot
from data_analysis.dataviz import OpenAirPlots

def calendar_plot(data_PM, pm, month, year):
    # Reformat data so only data from that month is plotted
    data_PM = data_PM.set_index('timestamp').resample('1D').mean()
    
    # Create calendar plot
    cal = CalendarPlot(pm, year, month)
    cal.add_pm_vals(data_PM)
    cal.show()


def timeplot_threshold(data_PM):
    # Initialize and create timeplot
    tp = Timeplot(data_PM)
    tp.show()


def diurnal_plot(dataPM, pm):
    label_dict = {'pm1': 'PM 1', 'pm25': 'PM 2.5', 'pm10': 'PM 10'}
    # Resample dataframe to every 10 minutes for cleaner results
    df = dataPM.set_index('timestamp').resample('10T').mean()
    # Create time column for indexing
    df['time'] = df.index.map(lambda x: x.strftime("%H:%M"))
    # Groupby time and calculate different metrics
    df = df.groupby('time')[pm]
    df_mean = df.mean()
    df_median = df.median()
    df_q1 = df.quantile(q=0.25)
    df_q3 = df.quantile(q=0.75)
    df_05 = df.quantile(q=0.05)
    df_95 = df.quantile(q=0.95)
    # Plot results (note that df_mean.index returns time; can be replaced by any other metric to get index)
    fig,axes=plt.subplots(1,1,figsize=(8,5))
    axes.plot(df_mean.index,df_mean, label = 'mean', color='C0')
    axes.plot(df_mean.index,df_median, label = 'median', color='C1')
    axes.fill_between(df_mean.index,df_q1,df_q3, alpha=0.2, label = '25-75 percentile', color='C1')
    axes.fill_between(df_mean.index,df_05,df_95, alpha=0.2, label = '5-95 percentile', color='C2')
    # Adjust settings of plot
    axes.xaxis.set_major_locator(MaxNLocator(15.8)) 
    axes.legend()
    axes.set_ylabel(f"{label_dict[pm]} [μg/m³]")
    for tick in axes.get_xticklabels():
        tick.set_rotation(45)

# def daily_average_plot(dataPM):
#     dataPM_day = dataPM.set_index('timestamp').resample('1D').mean()
#     plt.style.use('ggplot')

#     _,axes=plt.subplots(1,1,figsize=(8,5))
#     axes.plot(dataPM_day.pm1, label = 'PM 1')
#     axes.plot(dataPM_day.pm25, label = 'PM 2.5')
#     axes.plot(dataPM_day.pm10, label = 'PM 10')
#     axes.set_ylabel("[μg/m³]")  
#     axes.legend()
#     for tick in axes.get_xticklabels():
#         tick.set_rotation(45)


def wind_polar_plot(data_PM, pm):
    #df = df.rename(columns={"timestamp_local": "date", "wind_speed": "ws", "wind_dir": "wd"})
    #df.wd = df.wd.replace(0.0, 360.0)
    df = data_PM[['timestamp', 'wind_speed', 'wind_dir', 'pm25', 'pm10', 'pm1']]
    
    # Remove any points where wind data was unavailable. 
    df = df[df.wind_speed != 0]

    # Format the dataPM to be read in R and plot wind data
    air_plt = OpenAirPlots()
    air_plt.polar_plot(df, '2022-04/Graphs/wind_polar_plot/', [pm])
    #ro.r.polarPlot(dataPM, pollutant = p, main = f"{p.upper()} Polar Plot")
    
    # Take current image, save image again using matplotlib
    img = plt.imread(fname=f'2022-04/Graphs/wind_polar_plot/_polar_{pm}.png')
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


    def plot_and_export(self, plot_function, pm, **kwargs):
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
        # make directories for pollutants for graphs that are not timeplot graphs, which already plots for all 3 pollutants
        if str(plot_function.__name__)!='timeplot_threshold':
            try:
                os.mkdir('{0}/Graphs/{1}/{2}'.format(self.year_month, str(plot_function.__name__), pm))
            except: # Forgive my crime here, but it just avoids errors if the directory already exists
                pass
        for sn in self.sn_list:
            if not self.sn_dict[sn].empty:
                if pm == None:
                    plot_function(self.sn_dict[sn], **kwargs)
                    plt.savefig('{1}/Graphs/{2}/{0}_{1}_{2}.jpeg'.format(sn, self.year_month, str(plot_function.__name__)), bbox_inches='tight',dpi = 300)
                else:
                    plot_function(self.sn_dict[sn], pm, **kwargs)
                    plt.savefig('{1}/Graphs/{2}/{3}/{0}_{1}_{2}.jpeg'.format(sn, self.year_month, str(plot_function.__name__), pm), bbox_inches='tight',dpi = 300)