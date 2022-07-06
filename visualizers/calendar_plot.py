"""
Author: Neel Dhulipala
Project: Air Partners

Class for creating calendar plots reporting air quality on monthly basis.

Partially creditted to @meta4. https://github.com/meta4/mplcal
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
        """
        Args:
            pm: (str) identifies particular PM that is being analyzed (PM1, PM2.5, or PM10)
            year: (int) year when this data is from
            month: (int) month when this data is from
        """
        self.year = year
        self.month = month
        self.pm = pm
        # Subscripts for labels
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        # Dictionary for labeling calendar axis {keyword: (label, colorscale max, high threshold, low threshold)}
        label_dict = {
            'pm1': ('PM1'.translate(SUB), 8, 5, 2),
            'pm25': ('PM2.5'.translate(SUB), 20, 12, 5),
            'pm10': ('PM10'.translate(SUB), 50, 35, 20)
        }
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

        Args:
            df: (pandas.DataFrame) cleaned dataset of air quality over past month
        """
        # Check if the date at which data is generated is happening within designated month
        # and year; if it is, set end_date to most recent day; otherwise, set it to last day of month
        recent = df.iloc[-1]['timestamp']
        if self.month==recent.month and self.year==recent.year:
            end_date = recent.day
        else:
            end_date = calendar.monthrange(self.year, self.month)[1]
        # Reformat data so only data from that month is plotted
        df = df.set_index('timestamp').resample('1D').mean()
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
        # Create color spectrum
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
        f.suptitle(self.label + ' ' + m_names[self.month-1] + ' ' + str(self.year) + '\n',
                   fontsize=16, fontweight='bold')
        
        # Add colorbar
        cbar_ax = f.add_axes([0.85, 0.15, 0.05, 0.7])
        norm = matplotlib.colors.Normalize(vmin=0, vmax=self.scale)
        cbar = f.colorbar(matplotlib.cm.ScalarMappable(norm=norm, 
                                                cmap='Spectral_r'), 
                                                cax=cbar_ax)
        cbar.set_label(label=f'{self.label} [μg/m³]', fontsize=12)
        # Add dashed lines on colorbar representing key thresholds
        cbar.ax.hlines(self.high_thresh, 0, 2.5, colors='black', linestyles='dotted', linewidth=2)
        cbar.ax.hlines(self.low_thresh, 0, 2.5, colors='black', linestyles='dotted', linewidth=2)
