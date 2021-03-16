import pandas as pd
import time
from datetime import datetime
from timing_util import fetch_min_time, mark_attendance,change_time_format

timeFormat = '%H:%M:%S'

def assign_attendance(duration_df, min_time, sheet_date):
    attendance_df = duration_df.copy(deep = True)
    attendance_df[sheet_date] = 'Absent'

    for i, row in attendance_df.iterrows(): 
        #print(row)
        attendance_df[sheet_date][i] = mark_attendance(attendance_df['Duration'][i], min_time)

    return attendance_df

def calculate_duration(s_df, sorted_df, end_time):
    duration_df = s_df.copy(deep = True)
    duration_df['Duration'] = '00:00:00'

    temp_df = s_df.copy(deep = True)
    temp_df['Last Joined'] = '00:00:00'
    temp_df['Duration'] = '00:00:00'
    temp_df['status'] = 'UNKNOWN'

    for i, row in sorted_df.iterrows() :
        for j, obj in temp_df.iterrows() :
            
            if obj['Name'] == row['Full Name'] :
                #print(obj)

                time1 = obj['Last Joined']
                time2 = change_time_format(row['Timestamp'].split(" ")[1])

                

                if obj['status'] == 'UNKNOWN' :
                    temp_df['Last Joined'][j] = time2
                    temp_df['status'][j] = 'Joined'



                elif row['User Action'] == 'Left' :
                    diff = datetime.strptime(time2, timeFormat) - datetime.strptime(time1, timeFormat)
                    new_duration = datetime.strptime(obj['Duration'], timeFormat) + diff
                    timestampStr = str(new_duration).split(" ")[1]

                    temp_df['Duration'][j] = timestampStr
                    duration_df['Duration'][j] = timestampStr


                    #temp_df.replace({'Duration': { j : timestampStr } } )
                    #duration_df.replace({'Duration': { j : timestampStr } } )
                    
                    temp_df['status'][j] = 'Left'
                    
                    

                else :
                    temp_df['status'][j] = 'Left'
                    temp_df['Last Joined'][j] = time2

    for j, obj in temp_df.iterrows():
        
        if obj['status'] == 'Joined' and obj['Last Joined'] < end_time :

            time1 = obj['Last Joined']
            time2 = end_time
            
            diff = datetime.strptime(time2, timeFormat) - datetime.strptime(time1, timeFormat)
            new_duration = datetime.strptime(obj['Duration'], timeFormat) + diff
            timestampStr = str(new_duration).split(" ")[1]

            #temp_df.replace({'Duration': { j : timestampStr } } )
            #duration_df.replace({'Duration': { j : timestampStr } } )

            temp_df['Duration'][j] = timestampStr
            duration_df['Duration'][j] = timestampStr
                
            temp_df['status'][j] = 'Class Over'
                
                
            
    print("Temporary DataFrame")               
    print(temp_df)
    print("duration DataFrame")
    print(duration_df)

    return duration_df



def fetch_attendance(s_df, sorted_df, s_time, e_time, sheet_date):
    
    duration_df = calculate_duration(s_df, sorted_df, e_time)

    
    

    if s_time == "00:00:00" :
        min_time = "00:00:01"
        attendance_df  = assign_attendance(duration_df, min_time, sheet_date)

    else:
        min_time = fetch_min_time(s_time, sorted_df, e_time)
        attendance_df  = assign_attendance(duration_df, min_time, sheet_date)

    return(attendance_df)