import pandas as pd
import pymysql
from sqlalchemy import create_engine, alias
import mysql.connector
dbs  = [['immoscout.ch', 'immoscoutdb'],['comparis.ch','comparisdb']]

ls = list()
for db in dbs:
    st = db[0].capitalize()
    print(st)
    cnx = create_engine('mysql+pymysql://root:password@localhost/' + db[1]) 

    sql = """SELECT DATE_FORMAT(created_at, '%%W %%d, %%M %%Y'), COUNT(*) AS number_of_records FROM properties GROUP BY DATE_FORMAT(created_at, '%%W %%d, %%M %%Y')"""
    df = pd.read_sql(sql,cnx)
    df = df.rename(columns={"DATE_FORMAT(created_at, '%W %d, %M %Y')":"Date"})
    print(df)
    print("")


# print("affected rows = " + str(cursor.rowcount))