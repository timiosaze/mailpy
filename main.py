import smtplib, ssl
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


port = 465

user = 'timilthomas2018@gmail.com'
password = 'zemiglhungaiugen'    
msg = MIMEMultipart()

# Do you think I should add a context? default one throws another exception 
# of invalid authentication, as the server is talking 'with itself'
context = None
dbs  = [['homegate.ch', 'homegatedb'],['immoscout.ch', 'immoscoutdb'],['comparis.ch','comparisdb']]

ls = list()
text = list()
html = list()
for db in dbs:
    st = db[0].capitalize()
    # print(st)
    cnx = create_engine('mysql+pymysql://python:password@localhost/' + db[1]) 

    sql = """SELECT DATE_FORMAT(created_at, '%%W %%d, %%M %%Y'), COUNT(*) AS number_of_records FROM properties WHERE DATE(created_at) = CURDATE() - INTERVAL 1 DAY GROUP BY DATE_FORMAT(created_at, '%%W %%d, %%M %%Y')"""
    df = pd.read_sql(sql,cnx)
    df = df.rename(columns={"DATE_FORMAT(created_at, '%W %d, %M %Y')":"Date"})
    # print("")
    te = db[0].capitalize()
    text.append(te)
    
    html.append(df.to_html())

# Record the MIME types of both parts - text/plain and text/html.
tex = ""
for (a,b) in zip(text,html):
    tex = tex + "<h2>" + a + "</h2>" + "<br" + "<div>" + b + "</div>" 

html_2 =  """\
    <html>
    <head>
    <style> 
    table {
        border-collapse: collapse;
    }

    th, td {
        text-align: left;
        padding: 16px;
    }

    tr:nth-child(even){background-color: #f2f2f2}

    th {
        background-color: #04AA6D;
        color: white;
    }
    </style>
    </head>
    <body>
    <div>
    """ + tex + """ 
    </div>  
        </body>
    </html>
"""

part2 = MIMEText(html_2, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.

 
msg.attach(part2) 


server = smtplib.SMTP_SSL('smtp.gmail.com', port=port, context=context) 
server.set_debuglevel(1)
server.login(user, password)
server.sendmail(user, ['timiade1993@gmail.com', 'francollimassociates@gmail.com'], msg.as_string())

server.quit()