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
dates = pd.date_range(start="1/1/2023", end="12/31/2050")

# Initialize data dictionary
data_dict = {col: [] for col in ['date', 'day', 'suffix', 'dow_name', 'dow_num', 'doy', 'weekend', 'woy', 'fow', 'low', 'wom', 'month', 'moy_name', 'fom', 'lom', 'gov_quarter', 'year', 'cy', 'fy']}

# Iterate over date range and populate data
for date in dates:
    data_dict['date'].append(date)
    data_dict['day'].append(date.day)
    data_dict['suffix'].append('th' if 4 <= date.day <= 20 or 24 <= date.day <= 30 else ['st', 'nd', 'rd'][(date.day % 10) - 1])
    data_dict['dow_name'].append(date.strftime('%A'))
    data_dict['dow_num'].append(date.isoweekday())
    data_dict['doy'].append(date.timetuple().tm_yday)
    data_dict['weekend'].append(1 if date.isoweekday() in [6, 7] else 0)
    data_dict['woy'].append(date.strftime('%U'))
    data_dict['fow'].append(date - timedelta(days=date.weekday()))
    data_dict['low'].append(date + timedelta(days=(6 - date.weekday())))
    data_dict['wom'].append(week_of_month(date))
    data_dict['month'].append(date.month)
    data_dict['moy_name'].append(date.strftime('%B'))
    data_dict['fom'].append(date.replace(day=1))
    data_dict['lom'].append((date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1))
    data_dict['gov_quarter'].append((date.month - 1) // 3 + 1)
    data_dict['year'].append(date.year)
    data_dict['cy'].append(date.year)
    data_dict['fy'].append(date.year if date.month >= 10 else date.year - 1)
    data_dict['leap_year'].append(int(is_leap_year(date)))
    data_dict['53_weeks'].append(int(date.strftime('%U')) == 53)
    data_dict['disp_date'].append(date.strftime('%Y-%m-%d'))
    data_dict['disp_mm_yyyy'].append(date.strftime('%m/%Y'))
    data_dict['disp_mm_dd_yyyy'].append(date.strftime('%m/%d/%Y'))
    data_dict['disp_date_suffix'].append(date.strftime('%Y%m%d'))
    ppn, ppd, ppw, pp, pp_start, pp_end, pay_day = calculate_pay_period(date)
    ppid = (date.year - 2023) * 27 + ppn  # Adjust formula as needed
    ppy = date.year - 2000
    data_dict['ppid'].append(ppid)
    data_dict['pp'].append(pp)
    data_dict['ppy'].append(ppy)
    data_dict['ppn'].append(ppn)
    data_dict['ppw'].append(ppw)
    data_dict['ppd'].append(ppd)
    data_dict['pp_start'].append(pp_start)
    data_dict['pp_end'].append(pp_end)
    data_dict['pay_day'].append(pay_day)
    

# Create DataFrame
df = pd.DataFrame(data_dict)
conn = sqlite3.connect('project.db')
df.to_sql(conn, 'dim_date', if_exists='replace', index=False)
conn.close()