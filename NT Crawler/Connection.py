import pyodbc
import sqlalchemy as sal
from sqlalchemy import create_engine
import pandas as pd


engine = sal.create_engine('mssql+pyodbc://LAPTOP-VIMAFH9F/SQLEXPRESS/Politics?driver=SQL Server?Trusted_Connection=yes')
conn = engine.connect()
print(engine.table_names())