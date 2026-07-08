#==========================
# Requirements
#===========================
import pandas as pd
import os
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO,filename="Logs.log",format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y - %m -%d  %H-%M-%S')
from sqlalchemy import create_engine
import time
load_dotenv()

pd.set_option('display.max_columns',None)

pd.set_option('display.width',None)

pd.set_option('display.max_colwidth',None)

#=======================
# Extract
#=======================

def extract():                                                                  #Extract Function
    
    try:  
     
     logging.info("Extraction Process is started")                                                                         

     Employees = pd.read_csv(os.getenv("Emp_file"))                              # Employees Csv File Extracted

     Departments = pd.read_csv(os.getenv("Department_file"))                           # Departments Csv File Extracted

     Attendance = pd.read_csv(os.getenv("Attendance_file"))                            # Attendance Csv File Extracted

     Performance = pd.read_csv(os.getenv("Performance_file"))                          # Performance Csv file Extracted

     Salary = pd.read_csv(os.getenv("Salary_file"))                                   # Salary Csv file Extracted

    except FileNotFoundError as e:
       
       logging.error(f"File is missing: {e}")

    logging.info("Extract Process is Completed")

    return Employees,Departments,Attendance,Performance,Salary                        

#===============================
# Transformation
#===============================

def transform(Employees,Departments,Attendance,Performance,Salary):

    try:

     Employees = Employees.replace(r'^\s*$', pd.NA, regex=True)

     Departments = Departments.replace(r'^\s*$',pd.NA,regex=True)

     Attendance = Attendance.replace(r'^\s*$',pd.NA,regex=True)

     Performance = Performance.replace(r'^\s*$',pd.NA,regex=True)

     Salary = Salary.replace(r'^\s*$',pd.NA,regex=True)

     Employees.columns = Employees.columns.str.strip()

     string_cols = [

        "Emp_ID","First_Name","Last_Name","Gender","Phone","Email","City","State","Dept_ID","Job_Title","Employment_Status","Education","Blood_Group","Emergency_Contact"
     ]

     date_cols = [
        "DOB","Join_Date"
     ]

     
     Employees[string_cols] = Employees[string_cols].apply(lambda col:col.str.strip())

     Employees[date_cols] = Employees[date_cols].apply(lambda col:col.str.strip())

     Employees[date_cols] = Employees[date_cols].apply(pd.to_datetime) 

     Employees["Phone"] = Employees["Phone"].apply(lambda x: x if pd.isna(x) or x.startswith("+91") else "+91" + x)

     Employees[string_cols] = Employees[string_cols].astype("string")


    except Exception as e:
       
       logging.error(f"Failed to transform: {e}")

    return Employees.info()

Employees, Departments, Attendance, Performance, Salary = extract()
show = transform(Employees, Departments, Attendance, Performance, Salary)
print(show)