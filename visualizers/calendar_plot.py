"""
Author: Neel Dhulipala
Project: Air Partners

Class for creating calendar plots reporting air quality on monthly basis.
"""

import calendar
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from datetime import date
import seaborn as sns

calendar.setfirstweekday(6) # Sunday is 1st day in US
w_days = 'Sun Mon Tue Wed Thu Fri Sat'.split()
m_names = '''
January February March April
May June July August
September October November December'''.split()

class CalendarPlot(object):
    """
    Class including functions needed for creating calendar plots.
    """
    def __init__(self, pm, year, month):
        self.year = year
        self.month = month
        self.pm = pm
        # Dictionary for labeling calendar axis
        label_dict = {'pm1': ('PM1', 10, 5, 2), 'pm25': ('PM2.5', 20, 12, 5), 'pm10': ('PM10', 40, 25, 12)}
        self.label = label_dict[pm][0]
        # Color scale maximum for different PMs
        self.scale = label_dict[pm][1]
        # Threshold values
        self.high_thresh = label_dict[pm][2]
        self.low_thresh = label_dict[pm][3]
        # Create a list of lists for each week
        self.cal = calendar.monthcalendar(year, month)
        # Save the PM data in the same format
        self.pm_vals = [[0 for day in week] for week in self.cal]

    def _get_colors(self):    
        """
        Get palettable colors from Seaborn

        Returns:
            A color palette object
        """
        smap = sns.color_palette('Spectral_r', self.scale)
        return smap

    def _monthday_to_index(self, day):
        """
        Gives index of the day in terms of where it is on the calendar 
        grid.

        Args:
            day - (int) a given day in the calendar month
        Returns:
            None
        """
        for week_n, week in enumerate(self.cal):
            try:
                i = week.index(day)
                return week_n, i
            except ValueError:
                pass
         # couldn't find the day
        raise ValueError("There aren't {} days in the month".format(day))

    def add_pm_vals(self, df):
        """
        Assign PM value for each day in the month based on air quality DataFrame
        """
        # Check if the date at which data is generated is happening within designated month
        # and year; if it is, set end_date to today; otherwise, set it to last day of month
        today = date.today()
        if self.month==today.month and self.year==today.year:
            end_date = today.day
        else:
            end_date = calendar.monthrange(self.year, self.month)[1]
        start_date = end_date - df.shape[0]
        # Doing days in reversed order, for the case that a sensor was 
        # installed in middle of month
        for day in reversed(range(start_date, end_date)):
            week, w_day = self._monthday_to_index(day+1)
            pm_val = df.iloc[day - (start_date)][self.pm]
            if np.isnan(pm_val):
                self.pm_vals[week][w_day] = 0
            else:
                self.pm_vals[week][w_day] = df.iloc[day - (start_date)][self.pm]

    def show(self):
        """
        Create the calendar to be displayed
        """
        color_list = self._get_colors()

        # Create grid of subplots, where each subplot is a day in the calendar
        f, axs = plt.subplots(len(self.cal), 7, sharex=True, sharey=True)
        for week, ax_row in enumerate(axs):
            for week_day, ax in enumerate(ax_row):
                ax.set_xticks([])
                ax.set_yticks([])
                # Create numbers for the days in the calendar where they belong
                if self.cal[week][week_day] != 0:
                    ax.text(.5, .5,
                            str(self.cal[week][week_day]),
                            fontsize=16,
                            verticalalignment='center',
                            horizontalalignment='center')
                    # TODO: change this scale to make sense with PM 2.5 values
                    pm_val = self.pm_vals[week][week_day]
                    # if PM value is very high, color of day is last color on palette
                    if pm_val >= self.scale:
                        ax.set_facecolor(color_list[-1])
                    # if PM value is zero, no PM data from that day, leave white
                    elif pm_val == 0:
                        ax.set_facecolor('white')
                    # otherwise, color day appropriately based on scale
                    else:
                        ax.set_facecolor(color_list[int(self.pm_vals[week][week_day])])

        # use the titles of the first row as the weekdays
        for n, day in enumerate(w_days):
            axs[0][n].set_title(day)

        # Place subplots in a close grid
        f.subplots_adjust(hspace=0)
        f.subplots_adjust(wspace=0)
        f.subplots_adjust(right=0.8)
        f.suptitle(m_names[self.month-1] + ' ' + str(self.year) + '\n',
                   fontsize=16, fontweight='bold')
        
        # Add colorbar
        cbar_ax = f.add_axes([0.85, 0.15, 0.05, 0.7])
        norm = matplotlib.colors.Normalize(vmin=0, vmax=self.scale)
        cbar = f.colorbar(matplotlib.cm.ScalarMappable(norm=norm, 
                                                cmap='Spectral_r'), 
                                                cax=cbar_ax, 
                                                label=f'Concentrations of {self.label} [μg/m³]')
        # Add dashed lines on colorbar representing key thresholds
        cbar.ax.hlines(self.high_thresh, 0, 2.5, colors='black', linestyles='dotted', linewidth=2)
        cbar.ax.hlines(self.low_thresh, 0, 2.5, colors='black', linestyles='dotted', linewidth=2)
