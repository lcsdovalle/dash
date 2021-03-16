import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="json\cred_api.json"
PROJECT_ID = "getedu-api-293018"
DB = 'chromedash'
from google.cloud import bigquery
from flask.pylib.MyBigQuery import Stream, Reader, Update
from flask.pylib.pycsv import PyCsv
from flask.pylib.googleadmin import authService, ChromeBooks, User
import datetime

## PARA USO MANUAL
datacorte = '2021-03-08T23:59:00Z'
datacorte = datetime.datetime.strptime(datacorte,"%Y-%m-%dT%H:%M:%SZ")
timestamp_datacorte = datacorte.timestamp()
timestamp_datacorte

# # PARA USO AUTOMÁTICO, BUSCA SEMPRE A ÚLTIMA DATA
# datacorte = datetime.datetime.today() - datetime.timedelta(days=1)
# timestamp_datacorte = datacorte.timestamp()