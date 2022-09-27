from __future__ import print_function
from wsgiref import headers
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import pandas as pd
from sqlalchemy import create_engine
import pymysql


dbs  = [['homegate.ch', 'homegatedb'],['immoscout.ch', 'immoscoutdb'],['comparis.ch','comparisdb'],['flatfox.ch','flatfoxdb']]

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
    <h3>Records Inserted yesterday</h3>
    <div>
    """ + tex + """ 
    </div>  
        </body>
    </html>
"""

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
subject = "New Records in Database(yesterday)  testing...."
sender = {"name":"Jide Awonusi","email":"francollimassociates@gmail.com"}
replyTo = {"name":"Jide Awonusi","email":"francollimassociates@gmail.com"}
html_content = html_2
to = [{"email":"awonusiolajide@yahoo.com","name":"jAido"}, {"email":"timiade1993@gmail.com","name":"jAido"}]
params = {"parameter":"My param value","subject":"New Subject"}
send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=replyTo, html_content=html_content, sender=sender, subject=subject)

try:
    api_response = api_instance.send_transac_email(send_smtp_email)
    print(api_response)
except ApiException as e:
    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)