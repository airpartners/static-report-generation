"""
Author: Neel Dhulipala, Andrew DeCandia
Project: Air Partners

Script for importing necessary data for air quality analysis for static reporting.
"""


import pandas as pd
from calendar import monthrange
import quantaq
from quantaq.utils import to_dataframe
from datetime import datetime
from data_analysis.iem import fetch_data
import data_analysis.quantaq_pipeline as qp

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

        start_date, end_date = self._get_start_end_dates(self.year, self.month)

        mod_handler = qp.ModPMHandler(start_date=start_date, end_date=end_date)

        # Check if pckl file exists, pull data otherwise
        try:
            start_date, end_date = self._get_start_end_dates(self.year, self.month)
            df = mod_handler.load_df(sensor_sn, start_date, end_date)
            print("Data pulled from Pickle file")
        # Otherwise download it from API
        except:
            # try:
            #     # Pull dataframe from API, will return the dataframe and will also pickle the results for you to open and use later
            #     df = mod_handler.from_api(sensor_sn)
            # except:
            #     # If there is a request protocol error, create an empty dataframe (temp solution)
                df = pd.DataFrame()
        return df

    def _get_start_end_dates(self, year_int_YYYY, month_int):
        # get number of days in month_int of that year
        no_of_days = monthrange(year_int_YYYY, month_int)[1]
        # get start and end dates in type datetime
        start_date = datetime(year_int_YYYY, month_int, 1)
        end_date = datetime(year_int_YYYY, month_int, no_of_days)
        return start_date, end_date

    def get_PM_data(self):
        """
        """
        df_sensor_list, _ = self.get_sensor_list()

        sn_list = list(df_sensor_list.sn)
        sn_count = len(sn_list)
        sn_dict = {}

        sensor_count = 1
        for sn in sn_list:
            print('\rSensor Progress: {0} / {1}\n'.format(sensor_count, sn_count), end='', flush=True)
            # If sensor data already exists in pickle file, use that
            
            df = self._data_month(sn)
            sn_dict[sn] = df
            sensor_count+=1
        print('\nDone!')
        return sn_list, sn_dict


if __name__ == '__main__':
    di = DataImporter(year=YEAR, month=MONTH)
    sn_list, sn_dict = di.get_PM_data()