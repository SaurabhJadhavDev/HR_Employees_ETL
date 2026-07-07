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

#=======================
# Extract
#=======================

def extract():                                                                              #Extract Function

    Employees = pd.read_csv(os.getenv("Employees_file"))                              # Employees Csv File Extracted

    Departments = pd.read_csv(os.getenv("Department_file"))                           # Departments Csv File Extracted

    Attendance = pd.read_csv(os.getenv("Attendance_file"))                            # Attendance Csv File Extracted

    Performance = pd.read_csv(os.getenv("Performance_file"))                          # Performance Csv file Extracted

    Salary = pd.read_csv(os.getenv("Salary_file"))                                    # Salary Csv file Extracted

    return Employees,Departments,Attendance,Performance,Salary                        

#===============================
# Transformation
#===============================