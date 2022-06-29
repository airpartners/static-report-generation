"""
Author: Neel Dhulipala
Project: Air Partners

Class for creating timeplots to show air quality trends throughout the month
on a minute (sampling) basis.
"""

from IPython.core.pylabtools import figsize
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt

class Timeplot(object):

    def __init__(self, df):
        self.df = df
    
    def detect_inactive_sensor(self, timedelta_to_consider_inactive_in_minutes):
        inactive = [0]
        for i in range(1, len(self.df)):
            timedelta = (self.df.timestamp.iloc[i] - self.df.timestamp.iloc[i-1]).total_seconds()/60
            if timedelta >= timedelta_to_consider_inactive_in_minutes:
                inactive.append(1)
                inactive[i-1] = 1
            else:
                inactive.append(0)
        self.df['inactive'] = inactive

    def thresholds_subplots(self, plot_number, threshold_lower, threshold_upper, fig_axs):
        # time variable
        ts = self.df.timestamp
        # subscripts for labels
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        # defining subplot numbers
        if plot_number == 0:
            pm = self.df.pm1
            ylabel = 'PM1'.translate(SUB)
            # ylim = (0, 25)
        elif plot_number == 1:
            pm = self.df.pm25
            ylabel = 'PM2.5'.translate(SUB)
            # ylim = (0, 100)
        elif plot_number == 2:
            pm = self.df.pm10
            ylabel = 'PM10'.translate(SUB)
            # ylim = (0, 200)
        fig_axs[plot_number].fill_between(ts, pm, 0, where=(self.df.inactive == 0), facecolor="limegreen", interpolate=True, alpha=1,label='Low: < {}'.format(threshold_lower))
        fig_axs[plot_number].fill_between(ts, pm, threshold_lower, where=(self.df.inactive == 0) & (pm >= threshold_lower), facecolor="gold", interpolate=False, alpha=1,label='Medium')
        fig_axs[plot_number].fill_between(ts, pm, threshold_upper, where=(pm >= threshold_upper), facecolor="orangered", interpolate=False, alpha=1,label='High: > {}'.format(threshold_upper))
        fig_axs[plot_number].set_ylabel('{}\n[μg/m³]'.format(ylabel), fontsize=12)
        #fig_axs[plot_number].set_ylim(ylim)
        
        handles, labels = fig_axs[plot_number].get_legend_handles_labels()
        fig_axs[plot_number].legend(handles[::-1], labels[::-1],bbox_to_anchor=(1.0,0.5),loc = 'center left')

        try:
            percent_above_upper = (pm >= threshold_upper).value_counts(True).sort_values()[1]
        except:
            percent_above_upper = 0

        at = AnchoredText(
            "{}% of time above 24h threshold for healthy air".format(round((percent_above_upper * 100),1)), prop=dict(size=15), frameon=False, loc='upper right')
            #at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
        fig_axs[plot_number].add_artist(at)

    def show(self):
        _, axs = plt.subplots(3, sharex=True, sharey=False, figsize=(17,6))
        plt.subplots_adjust(hspace=.0)
        plt.xticks(rotation=45)

        # Check for inactive sensors
        self.detect_inactive_sensor(5)

        # Threshold values assigned according to annual EPA standards (PM1 estimated)
        self.thresholds_subplots(0, 2, 5, axs)
        self.thresholds_subplots(1, 5, 12, axs)
        # TODO: assign values for PM10 according to EPA and WHO standards
        self.thresholds_subplots(2, 20, 35, axs)

        # Hide x labels and tick labels for all but bottom plot.
        for ax in axs:
            ax.label_outer()