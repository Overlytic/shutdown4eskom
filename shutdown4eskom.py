#!/usr/bin/env python3

import pandas as pd
from datetime import datetime as dt

# import sched
# import time
# import os
# from plyer import notification

def fetch_loadshed_data(area_name):
    # Fetch load shedding schedule data from eskom calendar
    url = "https://github.com/beyarkay/eskom-calendar/releases/download/latest/machine_friendly.csv"
    df_raw = pd.read_csv(url, parse_dates=['start', 'finsh'])
    
    # Filter Area 
    if area_name :
        df =  (df_raw
               .query(f"area_name == '{area_name}'")
               .reset_index(drop=True)
               .copy()
              )            
    else:
        df = df_raw
    
    return(df)

def next_loadshed_time(load_shedding_data):
    # Check if load shedding is scheduled within a specified time window
    # Return True if scheduled, False otherwise
    
    df = load_shedding_data
    
    # Time Now
    my_tz = df.start[0].tz
    date_now = dt.now(tz=my_tz)

    # Filter and Sort
    df = df[df['start'] > date_now]
    df = df.sort_values('start')
    
    # Next Load shedding time
    time_next = df.start.dt.to_pydatetime()[0]
    
    return(time_next)

def display_warning():
    notification.notify(
        title='Load Shedding Warning',
        message='Load shedding is scheduled. The system will hibernate in 5 minutes.',
        timeout=10
    )

def shutdown_desktop():
    os.system('shutdown /s /t 0')

if __name__ == "__main__":
    area_name = 'city-of-cape-town-area-9' # pinelands
    data_loadshed = fetch_loadshed_data(area_name)
    time_next_loadshed = next_loadshed_time(data_loadshed)
    
    print(f"Next Loadshedding is at: {dt.strftime(time_next_loadshed, '%Y-%m-%d %H:%M:%S')}")
        
    # if is_load_shedding_scheduled(load_shedding_data):
    #     scheduler = sched.scheduler(time.time, time.sleep)
    #     warning_time = 5 * 60  # 5 minutes before hibernation
    #     scheduler.enter(warning_time, 1, display_warning, ())
    #     scheduler.enter(warning_time + 5 * 60, 2, shutdown_desktop, ())
    #     scheduler.run()
