import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="jsons\cred_api.json"
PROJECT_ID = "getedu-api-293018"
DB = 'chromedash'
from google.cloud import bigquery
from pylib.MyBigQuery import Stream, Reader
import datetime

## PARA USO MANUAL
datacorte = '2021-03-08T23:59:00Z'
datacorte = datetime.datetime.strptime(datacorte,"%Y-%m-%dT%H:%M:%SZ")
timestamp_datacorte = datacorte.timestamp()
timestamp_datacorte

# # PARA USO AUTOMÁTICO, BUSCA SEMPRE A ÚLTIMA DATA
# datacorte = datetime.datetime.today() - datetime.timedelta(days=1)
# timestamp_datacorte = datacorte.timestamp()

# inicio = "{}T00:01:00Z".format('2021-03-08')
# fim = "{}T23:59:00Z".format('2021-03-15')

ontem = datetime.datetime.today() - datetime.timedelta(days=1)
inicio = "{}T00:01:00Z".format(ontem.strftime('%Y-%m-%d'))
fim = "{}T23:59:00Z".format(ontem.strftime('%Y-%m-%d'))
