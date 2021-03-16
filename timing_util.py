import sys
import click
import time
from datetime import datetime


timeFormat = '%H:%M:%S'

def fetch_min_time(s_time_str, sorted_df, e_time_str):

    if s_time_str == "00:00:00" :
        min_time_str = "00:00:01"

    else: 

        join_time_str = sorted_df['Timestamp'][1].split(" ")[1]
        #join_time = datetime.strptime(join_time_str, timeFormat)
        #s_time = datetime.strptime(s_time_str, timeFormat).seconds
        
        if datetime.strptime(join_time_str, timeFormat) > datetime.strptime(s_time_str, timeFormat):
            optimized_time = join_time_str
            
        else:
            optimized_time = s_time_str

        max_time = datetime.strptime(e_time_str, timeFormat) - datetime.strptime(optimized_time, timeFormat)
        min_time = int(0.75 * max_time.seconds)
        min_time_str = time.strftime('%H:%M:%S', time.gmtime(min_time))
        print("Minimum Duration : ", min_time_str)
        
    return min_time_str

def mark_attendance(time_str, min_time):
    
    if datetime.strptime(time_str, timeFormat) > datetime.strptime(min_time, timeFormat):
        marked = 'Present'
        return 'Present'

    else:
        return 'Absent'

def change_time_format(timestamp_str):
    
    hh = timestamp_str.split(":")[0]
    hour = int(hh)
    if hour < 8 :
        hour = hour + 12
        hh = str(hour)

    elif hour > 7 and hour < 10 :
        hh =  '0' + hh
    mmss = timestamp_str.split(':',1)[1]
    hhmmss = str(hh + ':' + mmss)
    return hhmmss