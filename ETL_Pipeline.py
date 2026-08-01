#==========================
# Requirements
#===========================
import pandas as pd
import os
from dotenv import load_dotenv
import logging
from sqlalchemy import create_engine
import time
load_dotenv()

#===========================
# Structure of Output
#===========================

pd.set_option('display.max_columns',None)

pd.set_option('display.width',None)

pd.set_option('display.max_colwidth',None)

#============================
# Logging Structure
#===========================

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

info_handler = logging.FileHandler("info.log")
info_handler.setLevel(logging.INFO)

warn_handler = logging.FileHandler("Warnings.log")
warn_handler.setLevel(logging.WARNING)

formatter = logging.Formatter(
   "%(asctime)s - %(levelname)s - %(message)s",
   datefmt="%Y-%m-%d %H:%M:%S"
)

info_handler.setFormatter(formatter)
warn_handler.setFormatter(formatter)

logger.addHandler(info_handler)
logger.addHandler(warn_handler)

#=======================
# Extract
#=======================

def extract():                                                                  # Extract Function
    
    try:  
     
     logger.info("Extraction Process is started")                                                                         

     Employees = pd.read_csv(os.getenv("Emp_file"))                              # Employees Csv File Extracted

     Departments = pd.read_csv(os.getenv("Department_file"))                           # Departments Csv File Extracted

     Attendance = pd.read_csv(os.getenv("Attendance_file"))                            # Attendance Csv File Extracted

     Performance = pd.read_csv(os.getenv("Performance_file"))                          # Performance Csv file Extracted

     Salary = pd.read_csv(os.getenv("Salary_file"))                                   # Salary Csv file Extracted

     logger.info("Extract Process is Completed")

    except FileNotFoundError as e:
       
       logger.error(f"File is missing: {e}")

    return Employees,Departments,Attendance,Performance,Salary                        

#===============================
# Transformation
#===============================

def transform(Employees,Departments,Attendance,Performance,Salary):

    try:
     
     logger.info("Transformation Process is started...")

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

     # Employees Transformation

     Employees[string_cols] = Employees[string_cols].apply(lambda col:col.str.strip())

     Employees[date_cols] = Employees[date_cols].apply(lambda col:col.str.strip())

     Employees[date_cols] = Employees[date_cols].apply(pd.to_datetime) 

     Employees["Phone"] = Employees["Phone"].apply(lambda x: x if pd.isna(x) or x.startswith("+91") else "+91" + x)

     Employees[string_cols] = Employees[string_cols].astype("string")

     Employees = Employees.drop_duplicates()

     Employees["Phone_Null_Flag"] = Employees["Phone"].apply(lambda x:True if pd.isna(x) else False)

     Employees["Email_Null_Flag"] = Employees["Email"].apply(lambda x:True if pd.isna(x) else False)

     Employees["Education_Null_Flag"] = Employees["Education"].apply(lambda x:True if pd.isna(x) else False)

     Employees["Blood_Group_Null_Flag"] = Employees["Blood_Group"].apply(lambda x:True if pd.isna(x) else False)

     Employees["Emergency_Contact_Null_Flag"] = Employees["Emergency_Contact"].apply(lambda x:True if pd.isna(x) else False)

     Employees["Dept_ID_Null_Flag"] = Employees["Dept_ID"].apply(lambda x: True if pd.isna(x) else False)

     Employees["Gender"] = Employees["Gender"].str.title()

     null_dept_count = Employees["Dept_ID"].isnull().sum()

     if null_dept_count > 0:
        
        logger.warning(f"{null_dept_count} employees have no Dept_id orphan records detected")


     # Departments Performance

     Departments.columns = Departments.columns.str.strip()

     Departments["Dept_ID"] = Departments["Dept_ID"].str.strip()

     Departments["Dept_Name"] = Departments["Dept_Name"].str.strip()

     Departments["Location"] = Departments["Location"].str.strip()

     Departments["Manager_ID"] = Departments["Manager_ID"].str.strip()

     #Attendance Transformation

     Attendance.columns = Attendance.columns.str.strip()

     Attendance["Att_ID"] = Attendance["Att_ID"].str.strip()

     Attendance["Emp_ID"] = Attendance["Emp_ID"].str.strip()

     Attendance["Leave_Type"] = Attendance["Leave_Type"].str.strip()

     Attendance["Recorded_By"] = Attendance["Recorded_By"].str.strip()

     Attendance["Leave_Type"] = Attendance["Leave_Type"].str.title()

     Attendance["Leave_Type_Flag"] = Attendance["Leave_Type"].apply(lambda x:True if pd.isna(x) else False)

     Attendance["WFH_Days_Flag"] = Attendance["WFH_Days"].apply(lambda x: True if pd.isna(x) else False)


    # Performance Transformation
     
     Performance.columns = Performance.columns.str.strip()

     Performance["Self_Rating"] = Performance["Self_Rating"].astype("float64")

     Performance["Perf_ID"] = Performance["Perf_ID"].str.strip()

     Performance["Emp_ID"] = Performance["Emp_ID"].str.strip()

     Performance["Quarter"] = Performance["Quarter"].str.strip()

     Performance["Rating"] = Performance["Rating"].str.strip()

     Performance["Manager_Feedback_Flag"] = Performance["Manager_Feedback"].apply(lambda x: True if pd.isna(x) else False )

     Performance["Self_Rating"] = Performance["Self_Rating"].fillna(Performance["Self_Rating"].mean())

     Performance["Promotion_Recommended"] = Performance["Promotion_Recommended"].apply(lambda x: True if pd.isna(x) else False)

    # Salaries Transformation

     Salary.columns = Salary.columns.str.strip()

     Salary["Bonus"] = Salary["Bonus"].astype("float64")

     Salary["Bonus_Null_Flag"] = Salary["Bonus"].apply(lambda x: True if pd.isna(x) else False)

     Salary["Bonus"] = Salary["Bonus"].fillna(Salary["Bonus"].median())

     Salary["Effective_To"] = pd.to_datetime(Salary["Effective_To"])

     Salary["Effective_From"] = pd.to_datetime(Salary["Effective_From"])

     Salary["Effective_To_Null_Flag"] = Salary["Effective_To"].apply(lambda x: True if pd.isna(x) else False)

     logger.info("Transformation Process is Completed")

     return Employees,Departments,Attendance,Performance,Salary

    except Exception as e:
       
      logger.error(f"Failed to transform: {e}")

#===========================
# Load
#===========================

def load(Employees, Departments, Attendance, Performance, Salary):

   try:

      logging.info("Load Process is Started....")

      db_url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

      engine = create_engine(db_url)

      tables = {
         "Employees": Employees,
         "Departments": Departments,
         "Attendance": Attendance,
         "Performance": Performance,
         "Salary": Salary
      }

      for table_name, df in tables.items():

         logging.info(f"Loading {table_name} into MySQL...")

         df.to_sql(table_name,con=engine, if_exists="replace", index=False)

         logging.info(f"{table_name} Loaded Successfully - {len(df)} rows")

      logger.info("Load Process is Completed Successfuully")

   except Exception as e:

      logger.error(f"Failed to load: {e}")

Employees, Departments, Attendance, Performance, Salary = extract()
transformed_data = transform(Employees, Departments, Attendance, Performance, Salary)

if transformed_data is not None:
   load(*transformed_data)
else:
   logger.error("Load skipped because the transformation process failed")
