'''
File: make__dim_date.py
Project: fz_tools
Created Date: 2023-10-13
Author: Adge Denkers
Email: adge.denkers@gmail.com
-----
Last Modified: 2023-10-13
Modified By: Adge Denkers
Email: adge.denkers@gmail.com
-----
Copyright (c) 2023 denkers.co
'''


import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# Function to see if it is a leap year
def is_leap_year(date_obj):
    year = date_obj.year
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# Function to get week of month
def week_of_month(dt):
    first_day = dt.replace(day=1)
    dom = dt.day
    adjusted_dom = dom + first_day.weekday()
    return (adjusted_dom - 1) // 7 + 1

def calculate_pay_period(date):
    pp_start = datetime(2023, 1, 1)  # starting date of first pay period
    days_since_start = (date - pp_start).days
    ppn = days_since_start // 14 + 1
    ppd = days_since_start % 14 + 1
    ppw = (ppd - 1) // 7 + 1
    pp = f'23-{ppn:02d}'
    pp_end = pp_start + timedelta(days=ppn*14-1)
    pp_start = pp_start + timedelta(days=(ppn-1)*14)
    pay_day = 1 if ppd == 6 else 0
    return ppn, ppd, ppw, pp, pp_start, pp_end, pay_day


# Generate date range
dates = pd.date_range(start="1/1/2023", end="1/31/2023")

# Initialize data dictionary
data_dict = {col: [] for col in ['date', 'day', 'suffix', 'dow_name', 'dow_num', 'doy', 'weekend', 'woy', 'fow', 'low', 'wom', 'month', 'moy_name', 'fom', 'lom', 'gov_quarter', 'year', 'cy', 'fy', 'date','day','suffix','dow_name','dow_num','doy','weekend','woy','fow','low','wom','month','moy_name','fom','lom','gov_quarter','year','cy','fy','leap_year','53_weeks','disp_date','disp_mm_yyyy','disp_mm_dd_yyyy','disp_date_suffix','ppid','pp','ppy','ppn','ppw','ppd','pp_start','pp_end','pay_day']}

# Iterate over date range and populate data
for date in dates:
    data_dict['date'].append(date.date())
    print(date.date())
