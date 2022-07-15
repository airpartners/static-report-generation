"""
Author: Neel Dhulipala
Project: Air Partners

Class for creating diurnal (daily) plots that show air quality trends on any weekday and weekend.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Subscripts (for captions and labels)
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

class DiurnalPlot(object):
    """
    Class for creating diurnal (daily) plots.
    """
    def __init__(self, pm):
        """
        Args:
            pm: (str) type of PM used for analysis
        """
        self.pm = pm
    
    def convert_timestamps(self, df):
        """
        Convert all timestamp strings to datetime objects

        :param df: (pd.DataFrame) dataframe containing sensor data
        :returns: df with timestamps converted to datetime

        Code copied from quantaq_pipeline.py, written by Hwei-Shin Harrimam
        """
        #timestamp is already in UTC
        df = df.assign(timestamp=pd.to_datetime(df['timestamp']))
        # timestamp contains "local" time (but expresses it in UTC, so 18:59 Eastern is expressed as 18:59 UTC)
        # need to change the timezone without altering the hour of day.
        # So, convert to datetime, remove automatically applied UTC timezone, and convert to US/Eastern time.
        dti = pd.to_datetime(df['timestamp']).dt.tz_localize(None).dt.tz_localize('US/Eastern')
        df = df.assign(timestamp_local=dti)

        #order by timestamp asc instead of desc
        df = df.sort_values(by=['timestamp'])
        return df
    
    def process_data(self, df, get_weekdays=True, resampling=True):
        """
        Process dataframe for plotting.

        Args:
            df: (pandas.DataFrame) cleaned dataset containing air quality data of the month
            get_weekdays: (bool) if True, creates column in df to specify weekdays and weekends
            resampling: (bool) if True, resamples dataset by every 10 minutes for cleaner graph
        """
        # localize timestamps
        df = self.convert_timestamps(df)
        # if get_weekdays, add boolean column 'weekday' where 1 represents weekday, 0 represents weekend
        if get_weekdays:
            df['weekday'] = [df.iloc[row]['timestamp'].weekday() < 5 for row in range(df.shape[0])]
        
        # if resampling, resample dataframe for every 10 minutes
        if resampling:
            df = df.set_index('timestamp').resample('10T').mean()
        
        # Create time column for indexing
        df['time'] = df.index.map(lambda x: x.strftime("%H:%M"))       

        return df

    def _military_to_regular(self, time):
        """
        Change military time to regular time for xticks.

        Args:
            time: (Any) xtick for the diurnal plot in military time
        Returns:
            (string) regular time version of military time
        """
        # get string of time
        time = str(time)
        # if time xtick is empty, return it
        if time=='':
            return time
        # get datetime format of time so we can look at hours
        format = '%H:%M'
        dtime = datetime.strptime(time, format)
        # if hour is 0, set hour to 12
        if dtime.hour == 0:
            dtime = dtime.replace(hour=12)
            time = dtime.strftime(format)
            time = time + 'AM'
        # if hour is greater than 0 but less than 12, add an AM
        elif dtime.hour < 12:
            time = time + 'AM'
        # if hour is 12, add PM
        elif dtime.hour == 12:
            time = time + 'PM'
        # if hour is greater than 12, subtract 12 from the time and add PM
        elif dtime.hour > 12:
            dtime = dtime.replace(hour=dtime.hour-12)
            time = dtime.strftime(format)
            time = time + 'PM'
        return time


    def show(self, df, weekday=True):
        """
        Create diurnal plot figure that can be shown on report.

        Args:
            df: (pandas.DataFrame) cleaned dataset containing air quality data of the month
            weekday: (bool) if True, create diurnal plot for weekdays; if False, for weekends
        """
        label_dict = {
            'pm1': 'PM1'.translate(SUB),
            'pm25': 'PM2.5'.translate(SUB),
            'pm10': 'PM10'.translate(SUB)
        }
        # If weekday, filter out rows that are weekends, and vice versa
        if 'weekday' in df:
            if weekday:
                df = df[df['weekday']==1]
            else:
                df = df[df['weekday']==0]
        # Groupby time and calculate metrics
        df = df.groupby('time')[self.pm]
        df_mean = df.mean()
        df_median = df.median()
        df_q1 = df.quantile(q=0.25)
        df_q3 = df.quantile(q=0.75)
        df_05 = df.quantile(q=0.05)
        df_95 = df.quantile(q=0.95)
        #print(f'\tMean: {df_mean}\n\tMedian: {df_median}\n\tQ1: {df_q1}\n\tQ3: {df_q3}\n\t05: {df_05}\n\t95: {df_95}')
        # Plot results (note that df_mean.index returns time; can be replaced by any other metric to get index)
        fig,axes=plt.subplots(1,1,figsize=(8,5))
        # if there is not enough data for analysis, display warning on report
        if len(df_mean)==0:
            error = plt.imread('_images/error-404.png')
            axes.set_xticks([]); axes.set_yticks([])
            axes.imshow(error)
        # otherwise, plot the data, creating solid lines for mean and median and shadings for percentile differences
        else:
            axes.plot(df_mean.index,df_mean, label = 'mean', color='purple', linewidth=4)
            axes.plot(df_mean.index,df_median, label = 'median', color='red')
            axes.fill_between(df_mean.index,df_q1,df_q3,alpha=0.4, 
                                                        label = '25-75 percentile', 
                                                        color='#19a127', 
                                                        linewidth=0)
            axes.fill_between(df_mean.index,df_05,df_95,alpha=0.2,
                                                        label = '5-95 percentile',
                                                        color='#9f78cc',
                                                        linewidth=0)
            # Adjust settings of plot
            axes.xaxis.set_major_locator(MaxNLocator(15.8)) 
            axes.legend()
            if weekday:
                axes.set_ylabel(f"{label_dict[self.pm]} [μg/m³] Weekday", fontsize=18)
            else:
                axes.set_ylabel(f"{label_dict[self.pm]} [μg/m³] Weekend", fontsize=18)
            # Change xticks to show regular time; xticks presented in intervals of step
            step = 15
            axes.set_xticks(np.arange(0, len(df_mean.index), step))
            times = [self._military_to_regular(time) for time in df_mean.index]
            axes.set_xticklabels(times[::step], rotation=45, fontsize=15)
