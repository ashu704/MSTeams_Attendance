import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import pandas as pd
import os
import openpyxl


from excel_attendance import fetch_attendance

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 600, height = 600, bg = 'lightsteelblue')
canvas1.pack()

def getExcel ():
    global df
    
    import_file_path = filedialog.askopenfilename()
    df = pd.read_excel (import_file_path)
    
    #print (df)

def getStudentList ():
    global s_df

    import_file_path = filedialog.askopenfilename()
    s_df = pd.read_excel (import_file_path)
    
    #print (s_df)

def start_time():
    global s_timestamp 
    s_timestamp = simpledialog.askstring("Start Time of class", "Enter time as hh:mm (24 hr format)") + ':00'
    if s_timestamp == "0:00" :
        s_timestamp = "00:00:00"

    print(s_timestamp)
    

def end_time():
    global e_timestamp
    e_timestamp = simpledialog.askstring("End Time of class", "Enter time as hh:mm (24 hr format)") + ':00'
    if e_timestamp == "0:00" :
        e_timestamp = "19:00:00"

    print(e_timestamp)



def saveAttendance ():
   
    
    import_file_path = filedialog.askdirectory()
    if not os.path.isdir(import_file_path):
        os.makedirs(import_file_path)
    print(import_file_path)
    if not os.path.isfile(os.path.join(import_file_path, 'Total Attendance.xlsx')):
          
        dest_filename = 'Total Attendance.xlsx' 
        sheet_date = df['Timestamp'][1].split(",")[0]
        sheet_date = sheet_date.replace('/','.')

        sorted_df = df.sort_values(by = 'Timestamp')

        print(sorted_df)

        #print(sorted_df.items())
        
        attendance_df = fetch_attendance(s_df, sorted_df, s_timestamp, e_timestamp, sheet_date)
        attendance_df.to_excel(os.path.join(import_file_path, dest_filename), sheet_name = sheet_date, index = False)
        
    else :
          
        dest_filename = 'Total Attendance.xlsx'
        sheet_date = df['Timestamp'][1].split(",")[0]
        sheet_date = sheet_date.replace('/','.')

        sorted_df = df.sort_values(by = 'Timestamp')

        #print(sorted_df.items())

        attendance_df = fetch_attendance(s_df, sorted_df, s_timestamp, e_timestamp, sheet_date)

        #attendance_df.to_excel("Myfile.xlsx")
        #attendance_df.to_excel(os.path.join(import_file_path, dest_filename), sheet_name = sheet_date, index = False)
        
        with pd.ExcelWriter(os.path.join(import_file_path, dest_filename), engine='openpyxl',mode='a') as writer:
            attendance_df.to_excel(writer, sheet_name = sheet_date, index = False)

        
    
browseButton_Excel = tk.Button(text='Import Excel File', command=getExcel, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(300, 100, window=browseButton_Excel)

browseButton_Excel = tk.Button(text='Import Student File', command=getStudentList, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(300, 200, window=browseButton_Excel)

browseButton_Excel = tk.Button(text='Save Attendance', command=saveAttendance, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(300, 300, window=browseButton_Excel)


browseButton_Excel = tk.Button(text='Class Start Time', command=start_time, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(200, 400, window=browseButton_Excel)

browseButton_Excel = tk.Button(text='Class End Time', command=end_time, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(400, 400, window=browseButton_Excel)


root.mainloop()