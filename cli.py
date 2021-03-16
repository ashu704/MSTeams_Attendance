import sys
import click

from calculator import attendance_list_init, processed_list, duration_calculator, update_attendance_file, calc_min_time
@click.command()
#@click.argument('teamsfile', default = None)
#@click.argument('end_time', default = None, type = str )


def main():

    again = "y"
    while(again == 'y'):

        teamsfile = click.prompt("What is the complete file name of attendance list? ")
        click.echo(f"The name you gave is *{teamsfile}*")

        starttime = click.prompt("What is the class starting time(hhmm) ? ")
        endtime   = click.prompt("What is the class ending time(hhmm) ?   ")
        

        
        student_list_file = 'StudentList.csv'
        Teams_file = str(teamsfile)
        start_time = starttime[:2] + ":"+starttime[2:] + ':00'
        end_time = endtime[:2] + ":"+endtime[2:] + ':00'

        click.echo(f"The starting time you gave is {start_time}")
        click.echo(f"The ending time you gave is   {end_time}")
        
        attendance_file_name = attendance_list_init(student_list_file, Teams_file)
        teams_list = processed_list(Teams_file)

        duration_list = duration_calculator(attendance_file_name, teams_list,end_time)

        min_time = calc_min_time(teams_list, end_time, start_time)
        update_attendance_file(duration_list, attendance_file_name, min_time)

        again = click.prompt("Do you want to continue? (y/n) ")
    

if __name__ == '__main__':
    main()
    
   
    
