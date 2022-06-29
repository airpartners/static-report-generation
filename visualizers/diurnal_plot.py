"""
Author: Neel Dhulipala
Project: Air Partners

Class for creating diurnal (daily) plots that show air quality trends on any weekday and weekend.
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Subscripts (for captions and labels)
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

class DiurnalPlot(object):
    def __init__(self, pm):
        self.pm = pm
    
    def process_data(self, df, get_weekdays=True, resampling=False):
        """
        Process dataframe for plotting.

        Args:
            df: (pandas.DataFrame) cleaned dataset containing air quality data of the month
            get_weekdays: (bool) if True, creates column in df to specify weekdays and weekends
            resampling: (bool) if True, resamples dataset by every 10 minutes for cleaner graph
        """
        # if get_weekdays, add boolean column 'weekday' where 1 represents weekday, 0 represents weekend
        if get_weekdays:
            df['weekday'] = [df.iloc[row]['timestamp'].weekday() < 5 for row in range(df.shape[0])]
        
        # if resampling, resample dataframe for every 10 minutes
        df = df.set_index('timestamp').resample('10T').mean()
        
        # Create time column for indexing
        df['time'] = df.index.map(lambda x: x.strftime("%H:%M"))       

        return df
    

    def show(self, df, weekday=True):
        label_dict = {
            'pm1': 'PM1'.translate(SUB),
            'pm25': 'PM 2.5'.translate(SUB),
            'pm10': 'PM 10'.translate(SUB)
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
        else:
            axes.plot(df_mean.index,df_mean, label = 'mean', color='red')
            axes.plot(df_mean.index,df_median, label = 'median', color='purple')
            axes.fill_between(df_mean.index,df_q1,df_q3, alpha=0.2, label = '25-75 percentile', color='C1')
            axes.fill_between(df_mean.index,df_05,df_95, alpha=0.2, label = '5-95 percentile', color='C2')
            # Adjust settings of plot
            axes.xaxis.set_major_locator(MaxNLocator(15.8)) 
            axes.legend()
            if weekday:
                axes.set_ylabel(f"{label_dict[self.pm]} [μg/m³] Weekday", fontsize=12)
            else:
                axes.set_ylabel(f"{label_dict[self.pm]} [μg/m³] Weekend", fontsize=12)
            for tick in axes.get_xticklabels():
                tick.set_rotation(45)
