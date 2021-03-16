import csv
import collections
import time
from datetime import datetime
from operator import attrgetter




timeFormat = '%H:%M:%S'

def attendance_list_init(student_list_file, Teams_file):

    attendance_file_name = " "
    
    with open(Teams_file, 'r', encoding='utf16') as f:
        f_reader = csv.DictReader(f, delimiter = '\t')

        
        for row in f_reader:
            attendance_file_name = row['Timestamp'].split(",")[0]
            
                

    attendance_file_name = attendance_file_name.replace("/" , "-")
    attendance_file_name = attendance_file_name + "_Attendance.csv"
    print(attendance_file_name)


    #attendance_file_name = Teams_file.split('.')[0] + "_Attendance.csv" 

    with open(student_list_file, 'r') as student_list:
        student_list_reader = csv.DictReader(student_list, delimiter = ',')


        with open(attendance_file_name, 'w') as new_file:
            fieldnames = ['Full_Name', 'Roll_Number','Duration','Marked']
            csv_writer = csv.DictWriter(new_file, fieldnames= fieldnames, delimiter=',')
        
            csv_writer.writeheader()

            for row in student_list_reader:
                csv_writer.writerow({'Full_Name': row['Name'], 'Roll_Number': row['Roll No'],'Duration': 0,'Marked': 'Absent'})

    return attendance_file_name

            

        

def processed_list(Teams_file):
    Teams_list = []

    with open(Teams_file, 'r', encoding='utf16') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = '\t')

        
        
        User_Action = collections.namedtuple('User_Action', ['Name', 'Action', "Timestamp"])

        for obj in csv_reader:
            s = obj['Timestamp'].split(" ")[1]
            temp = User_Action(obj['Full Name'], obj['User Action'], s)
            Teams_list.append(temp)

        for index, obj in enumerate(Teams_list):

            hour = int(obj.Timestamp.split(":")[0])
            hh = obj.Timestamp.split(":")[0]
            if hour < 8 :
                hour = hour + 12
                hh = str(hour)
            elif hour > 7 and hour < 10 :
                hh =  '0' + hh
            mmss = obj.Timestamp.split(':',1)[1]
            hhmmss = str(hh + ':' + mmss)
            obj = obj._replace(Timestamp = hhmmss)
            Teams_list[index] = obj
            

    Teams_list.sort(key=attrgetter('Timestamp'))

    return Teams_list


def duration_calculator(attendance_file_name, Teams_list, end_time):



    duration_list = []

    

    with open(attendance_file_name, 'r', newline='\n') as new_file:
        new_file_reader = csv.reader(new_file, delimiter = ',')

        student_status = collections.namedtuple('student_status', ['Name', "Roll_No", 'Status', 'Last_joined', "Duration"])
        
        next(new_file_reader)
        for obj in new_file_reader:
            #print("first objext", obj)
            status = student_status(obj[0], obj[1], 'UNKNOWN', "00:00:00", "00:00:00")
            duration_list.append(status)
            
    for i in Teams_list:

        #print('i_object  ', i)

        for index, obj in enumerate(duration_list) :
            
            if obj.Name == i.Name :
                #print(obj)

                time1 = obj.Last_joined
                time2 = i.Timestamp

                

                if obj.Status == 'UNKNOWN' :
                    obj = obj._replace(Last_joined = time2)
                    obj = obj._replace(Status = i.Action)
                    duration_list[index] = obj


                elif i.Action == 'Left' :
                    diff = datetime.strptime(time2, timeFormat) - datetime.strptime(time1, timeFormat)
                    new_duration = datetime.strptime(obj.Duration, timeFormat) + diff
                    timestampStr = str(new_duration).split(" ")[1]
                    obj = obj._replace(Duration = timestampStr)
                    obj = obj._replace(Status = 'Left')
                    duration_list[index] = obj
                    

                else :
                    #diff = datetime.strptime(time2, timeFormat) - datetime.strptime(time1, timeFormat)
                    #new_duration = datetime.strptime(obj.Duration, timeFormat) + diff
                    #timestampStr = str(new_duration).split(" ")[1]
                    #obj = obj._replace(Duration = timestampStr)
                    obj = obj._replace(Last_joined = time2)
                    obj = obj._replace(Status = i.Action)
                    duration_list[index] = obj

                #print(obj)
                #print('\n')

                
    #print('\n\n',"---------next sess----------", '\n\n')

    for index, obj in enumerate(duration_list) :

        if obj.Status == 'Joined' and obj.Last_joined < end_time:

            #print(obj)

            time1 = obj.Last_joined
            time2 = end_time

            diff = datetime.strptime(time2, timeFormat) - datetime.strptime(time1, timeFormat)
            new_duration = datetime.strptime(obj.Duration, timeFormat) + diff
            timestampStr = str(new_duration).split(" ")[1]

            obj = obj._replace(Duration = timestampStr)
            obj = obj._replace(Status = 'TimeUp')
            duration_list[index] = obj      

            #print(obj)
            #print('\n') 

    
    
    
    #for row in duration_list:
        #print(row)           

    return duration_list            

def calc_min_time(sorted_list, end_time, start_time):
    join_time_str = sorted_list[0].Timestamp

    if datetime.strptime(join_time_str, timeFormat) > datetime.strptime(start_time, timeFormat):
        optimized_time = join_time_str
        
    else:
        optimized_time = start_time

    
    max_time = datetime.strptime(end_time, timeFormat) - datetime.strptime(start_time, timeFormat)
    min_time = int(0.75 * max_time.seconds)
    min_time_str = time.strftime('%H:%M:%S', time.gmtime(min_time))
    print("Minimum Duration : ", min_time_str)
    return min_time_str    
        
def update_attendance_file(duration_list,attendance_file_name, min_time ='00:35:00' ):    
    
    with open(attendance_file_name, 'w', newfile = '') as attendance_file:

        fieldnames = ['Full_Name', 'Roll_Number','Duration','Marked']
        csv_writer = csv.DictWriter(attendance_file, fieldnames= fieldnames, delimiter=',')
    
        csv_writer.writeheader()

        for row in duration_list[:]:
            
            marked = 'Absent'
            time1 = row.Duration
            time2 = min_time
            #time2 = '00:35:00'

            if datetime.strptime(time1, timeFormat) > datetime.strptime(time2, timeFormat):
                marked = 'Present'
            
            csv_writer.writerow({'Full_Name': row.Name, 'Roll_Number': row.Roll_No,'Duration': row.Duration, 'Marked': marked})
    



'''
student_list_file = 'StudentList_ edited.csv'
Teams_file = 'meetingAttendanceList (6).csv'
end_time = '13:20:00'
attendance_file_name = attendance_list_init(student_list_file, Teams_file)

duration_list = duration_calculator(attendance_file_name, processed_list(Teams_file),end_time)
update_attendance_file(duration_list, attendance_file_name)
'''    
