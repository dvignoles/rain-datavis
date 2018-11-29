# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 12:21:22 2018
For use with Local Climatogical Data retrieved through 
@author: dvign
"""
#TODO: Switch from 'SOD' report type for daily sums to summed hourly values per Day
    #Some 'SOD' daily totals are missing despite there being hourly records

#TODO: Generalize code / refactor

#sum2018nyc_V2
#all_hourly and all_daily contain completed dataframes

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#MAC
#filename = "/Users/user/Desktop/DANIEL_VIGNOLES/Fall2018/noaa_LCD/summer2018nyc.csv"

#Windows
filename = "C:\\Users\\dvign\\Desktop\\asrc\\Fall2018\\noaa_LCD\\summer2018nyc.csv"

#NO-DATA values
na_vals = ['',-9999,'T']

#indexing of file
nrows = 13369

lag_start_index = 0
cp_start_index = 4683
jfk_start_index = 8826

lag_rows = 4683
cp_rows = jfk_start_index - cp_start_index -1
jfk_rows = nrows- cp_rows + lag_rows

#Dataframes by station
cols = ["STATION_NAME","REPORTTPYE","HOURLYPrecip","DAILYPrecip","MonthlyTotalLiquidPrecip"]
col_renames = ["station","report_type","hourly_prec","daily_prec","monthly_total_prec"]

#FUll Central Park Precipitaion DataFrame
cp_df = pd.read_csv(filename, header = 0, skiprows = range(1,cp_start_index+1), nrows = cp_rows, index_col = 5, na_values = na_vals, parse_dates = True)
cp_df = cp_df[cols]
cp_df.columns = col_renames
cp_df.index.name = 'date_time'

#FUll Laguardia Precipitaiton DataFrame
lag_df = pd.read_csv(filename, header = 0, nrows = cp_start_index, index_col = 5, na_values = na_vals, parse_dates = True)

lag_df = lag_df[cols]
lag_df.columns = col_renames
lag_df.index.name = 'date_time'

#FULL JFK Precipitiaton DataFrame
jfk_df = pd.read_csv(filename, header = 0, skiprows = range(1,jfk_start_index), nrows = jfk_rows, index_col = 5, na_values = na_vals, parse_dates = True)
jfk_df = jfk_df[cols]
jfk_df.columns = col_renames
jfk_df.index.name = 'date_time'

#Clean/Convert Numeric Data
numeric = ["hourly_prec","daily_prec","monthly_total_prec"]
for col in numeric:
    cp_df[col] = cp_df[col].str.replace('[^\d.]+', '').astype(np.float64)
    lag_df[col] = lag_df[col].str.replace('[^\d.]+', '').astype(np.float64)
    jfk_df[col] = jfk_df[col].str.replace('[^\d.]+', '').astype(np.float64)

#####FILTERING BY REPORT_TYPE######
hourly_cols = ['station','report_type','hourly_prec']
daymonth_cols = ['station','report_type','daily_prec','monthly_total_prec']

#Central Park by Report Type
cp_fm15_indices = cp_df['report_type'] == 'FM-15'
cp_sod_indices = cp_df['report_type'] == 'SOD'

cp_hourly = cp_df.loc[cp_fm15_indices,hourly_cols]
cp_hourly.columns = ['station','report_type','CP_hourly_prec']
cp_hourly = cp_hourly [['CP_hourly_prec']]

cp_daily = cp_df.loc[cp_sod_indices,daymonth_cols]
cp_daily.columns = ['station','report_type','CP_daily_prec','CP_monthly_total_prec']
cp_daily = cp_daily[['CP_daily_prec','CP_monthly_total_prec']]

#LAG by report type
lag_fm15_indices = lag_df['report_type'] == 'FM-15'
lag_sod_indices = lag_df['report_type'] == 'SOD'

lag_hourly = lag_df.loc[lag_fm15_indices,hourly_cols]
lag_hourly.columns = ['station','report_type','LAG_hourly_prec']
lag_hourly = lag_hourly [['LAG_hourly_prec']]

lag_daily = lag_df.loc[lag_sod_indices,daymonth_cols]
lag_daily.columns = ['station','report_type','LAG_daily_prec','LAG_monthly_total_prec']
lag_daily = lag_daily[['LAG_daily_prec','LAG_monthly_total_prec']]


#JFK by report type
jfk_fm15_indices = jfk_df['report_type'] == 'FM-15'
jfk_sod_indices = jfk_df['report_type'] == 'SOD'

jfk_hourly = jfk_df.loc[jfk_fm15_indices,hourly_cols]
jfk_hourly.columns = ['station','report_type','JFK_hourly_prec']
jfk_hourly = jfk_hourly [['JFK_hourly_prec']]

jfk_daily = jfk_df.loc[jfk_sod_indices,daymonth_cols]
jfk_daily.columns = ['station','report_type','JFK_daily_prec','JFK_monthly_total_prec']
jfk_daily = jfk_daily[['JFK_daily_prec','JFK_monthly_total_prec']]


#Group stations back together for Plotting 
temp = pd.merge_ordered(cp_hourly,lag_hourly, on = 'date_time')
all_hourly = pd.merge_ordered(temp,jfk_hourly, on = 'date_time')

temp = pd.merge_ordered(cp_daily, lag_daily, on = 'date_time')
all_daily = pd.merge_ordered(temp, jfk_daily, on = 'date_time')



daily_stations = ['CP_daily_prec','LAG_daily_prec','JFK_daily_prec']

june = np.array(['2018-06-01','2018-06-30'],dtype = np.datetime64)
july = np.array(['2018-07-01','2018-07-31'],dtype = np.datetime64)
august = np.array(['2018-08-01','2018-08-31'],dtype = np.datetime64)
september = np.array(['2018-09-01','2018-09-30'],dtype = np.datetime64)

select = [0,1,3,5]

#Daily totals by month
june_daily = all_daily.iloc[0:30, select]
july_daily = all_daily.iloc[30:61,select]
august_daily = all_daily.iloc[61:92,select]
september_daily = all_daily.iloc[92:,select]

#Hourly totals by month
june_hourly = all_hourly[all_hourly['date_time'].apply(pd.Timestamp.month_name) == 'June']
july_hourly = all_hourly[all_hourly['date_time'].apply(pd.Timestamp.month_name) == 'July']
august_hourly = all_hourly[all_hourly['date_time'].apply(pd.Timestamp.month_name) == 'August']
september_hourly = all_hourly[all_hourly['date_time'].apply(pd.Timestamp.month_name) == 'September']

def getDay(dt):
    return dt.day

#Signifcant Rainfall Days
august11 = august_hourly[august_hourly['date_time'].apply(getDay) == 11]
july17 = july_hourly[july_hourly['date_time'].apply(getDay) == 17]
september18 = september_hourly[september_hourly['date_time'].apply(getDay) == 18]


days30 = np.arange(1,31)
days_30 = list(map(str,days30))

days31 = np.arange(1,32)
days_31 = list(map(str,days31))
daily_stations = ['CP_daily_prec','LAG_daily_prec','JFK_daily_prec']

def pltbyMonth():
    fig,axes = plt.subplots(2,2, sharey = True, figsize = (12,8))
    
    june_daily.plot(y = daily_stations, x = 'date_time', kind = 'bar',ax = axes[0,0], legend = False)
    axes[0,0].set_xticklabels(days_30)
    axes[0,0].set_title("June 2018")
    
    july_daily.plot(y = daily_stations, x = 'date_time', kind = 'bar',ax = axes[0,1], legend = False)
    axes[0,1].set_xticklabels(days_31)
    axes[0,1].set_title('July 2018')
    
    august_daily.plot(y = daily_stations, x = 'date_time', kind = 'bar',ax = axes[1,0], legend = False)
    axes[1,0].set_xticklabels(days_31)
    axes[1,0].set_title('August 2018')
    
    september_daily.plot(y = daily_stations, x = 'date_time', kind = 'bar',ax = axes[1,1], legend = False)
    axes[1,1].set_xticklabels(days_30)
    axes[1,1].set_title('September 2018')
    
    for row in axes:
        for ax in row:
            ax.tick_params(axis = 'x' ,labelrotation = 90)
            ax.set_ylabel('Inches')
            ax.set_xlabel('Day')
    
    
    handles, labels = axes[0,0].get_legend_handles_labels()
    labels = ['Central Park','Laguardia','JFK']
    fig.legend(handles, labels, loc='best')
    fig.suptitle("Daily Rainfall Summer 2018 NYC Local Weather Stations")
    plt.subplots_adjust(top=0.918,
        bottom=0.064,
        left=0.055,
        right=0.965,
        hspace=0.211,
        wspace=0.049)
    return fig

hourly_stations = ['CP_hourly_prec','LAG_hourly_prec','JFK_hourly_prec']

hours_24 = list(map(str,np.arange(1,25)))
hours = []
for hour in hours_24:
    hour = hour + ':00'
    hours.append(hour)
                    
def pltDay(df):
    fig, ax = plt.subplots()
    df.plot(x = 'date_time', y = hourly_stations, kind = 'bar', ax = ax)
    
    ax.set_ylim(0,2)
    
    label_size = 'xx-large'
    tick_size = 'large'
    
    
    ax.set_xticklabels(hours)
    ax.set_xlabel('Time', fontsize = label_size)
    ax.set_ylabel('Inches', fontsize = label_size)
    ax.tick_params(labelsize = tick_size)
    
    stations = ['Central Park', 'Laguardia', 'JFK']
    ax.legend(stations, fontsize = label_size, title = 'Weather Station')
    
    day = df['date_time'].iloc[1].strftime('%B %d, %Y')
    ax.set_title(day + ' Hourly Rainfall NYC', fontsize = label_size)
    
    
    fig.set_size_inches(12,10)
    return fig

pltDay(august11).savefig('aug11_a_hourly')
pltDay(july17).savefig('july17_a__hourly')
pltDay(september18).savefig('sep18_a_hourly')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    