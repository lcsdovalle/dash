import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="json\cred_api.json"
PROJECT_ID = "getedu-api-293018"
DB = 'chromedash'
from google.cloud import bigquery
from flask.pylib.MyBigQuery import Stream, Reader, Update
from flask.pylib.pycsv import PyCsv
from flask.pylib.googleadmin import authService, ChromeBooks, User
