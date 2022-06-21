"""
Author: Neel Dhulipala
Project: Air Partners

Script for importing necessary data for air quality analysis for static reporting.
"""


import pandas as pd
from calendar import monthrange
import quantaq
from quantaq.utils import to_dataframe
from datetime import datetime
from data_analysis.iem import fetch_data

client = quantaq.QuantAQAPIClient(api_key="VSZMMY8VT8FIRNIIXWTD2G7V")

# STATICS (for testing)
YEAR = 2022
MONTH = 4

class DataImporter(object):
    """
    Imports necessary sensor and wind data for analysis.
    """

    def __init__(self, year, month):
        self.year = year
        self.month = month

    def get_sensor_list(self):
        devices_raw = to_dataframe(client.devices.list(filter="city,like,%_oxbury%"))
        devices_simplified = devices_raw.iloc[:,[4,3,11,15,16,5,7,8,10,12]]
        return devices_simplified, devices_raw


    def _data_month(self, sensor_sn):        
        df = []
        if self.month == 12:
            start_date = '{0}-{1}-01'.format(self.year, self.month)
            end_date = '{0}-{1}-01'.format(self.year+1, 1)
        else:
            start_date = '{0}-{1}-01'.format(self.year, self.month)
            end_date = '{0}-{1}-01'.format(self.year, self.month+1)
        number_of_days = len(pd.date_range(start=start_date, end=end_date))
        c = 1
        for each in pd.date_range(start=start_date,end=end_date):
            df.append(to_dataframe(client.data.bydate(sn=sensor_sn, date=str(each.date()))))
            print('\r Day Progress: {0} / {1}'.format(c,number_of_days), end='', flush=True)
            c+=1
        df = pd.concat(df)
        if not df.empty:
            df_simplified = df.iloc[:,[0,1,2,4,5,7,8]]
            return df_simplified
        else:
            return df

    def get_iem_data(self):
        def get_start_end_dates(month_int, year_int_YYYY):
            # get number of days in month_int of that year
            no_of_days = monthrange(year_int_YYYY, month_int)[1]
            # get start and end dates in type datetime
            start_date = datetime(year_int_YYYY, month_int, 1)
            end_date = datetime(year_int_YYYY, month_int, no_of_days)
            return start_date, end_date

        start, end = get_start_end_dates(self.month, self.year)
        iem_df = fetch_data(start, end)
        return iem_df

    def get_PM_data(self):
        df_sensor_list, _ = self.get_sensor_list()

        sn_list = list(df_sensor_list.sn)
        sn_count = len(sn_list)
        sn_dict = {}

        # Get IEM data for inputting into sensor data
        iem_df = self.get_iem_data()

        sensor_count = 1
        for sn in sn_list:
            print('\rSensor Progress: {0} / {1}\n'.format(sensor_count, sn_count), end='', flush=True)
            df = self._data_month(sn) 
            # Add month column in df so extraneous days can be filtered out later
            df['month'] = [df.iloc[row]['timestamp_local'].month for row in range(df.shape[0])]
            sn_dict[sn] = df
            sensor_count+=1
        print('\nDone!')
        return sn_list, sn_dict


if __name__ == '__main__':
    di = DataImporter(year=YEAR, month=MONTH)
    sn_list, sn_dict = di.get_PM_data()