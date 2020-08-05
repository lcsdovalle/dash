from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from google.oauth2 import service_account
import googleapiclient.discovery
#https://github.com/googleapis/google-api-python-client/blob/master/samples/service_account/tasks.py
class authService():
    def __init__(self,scopes,jsonfile,email=None):
            self.userEmail = email
            self.SERVICE_ACCOUNT_FILE = jsonfile
            self.SCOPES = scopes
    def getService(self,*args,**kwargs):
            credentials = service_account.Credentials.from_service_account_file(
                    self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
            if self.userEmail is not None:                
                delegated_credentials = credentials.with_subject(self.userEmail)
                credentials = delegated_credentials

            return googleapiclient.discovery.build(args[0], args[1], credentials=credentials)
    def setScope(self,scopes):
            pass        

# auth = authService('jsons/credential.json','lucas@gsaladeaula.com.br').getService('admin','directory_v1')
# users = auth.users().list(customer="my_customer").execute()
# print(users)
class clientAuth():

    def __init__(self,creds,scopes):
        # If modifying these scopes, delete the file token.pickle.
        self.SCOPES = scopes
        # print(SCOPES)
        self.service = None
        self.creds = creds
        

    def getService(self,*args):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build(args[0], args[1], credentials=creds)
        return self.service        

#     def spreadSheet(self,SPREADSHEET_ID,RANGE_NAME=None):
#         SPREADSHEET_ID = SPREADSHEET_ID
#         RANGE_NAME = RANGE_NAME
#     # Call the Sheets API
#         sheet = self.service.spreadsheets()
#         result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
#                                     range=RANGE_NAME).execute()
#         values = result.get('values', [])
#         # The ID and range of a sample spreadsheet.


#         if not values:
#             print('No data found.')
#         else:
#             print('Name, Major:')
#             for row in values:
#                 # Print columns A and E, which correspond to indices 0 and 4.
#                 print('%s, %s' % (row[0], row[4]))
# scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# service = clientAuth('jsons/client_cred.json',scopes).getService('sheets','v4')

# values = service.spreadsheets().values().get(spreadsheetId='1XbkJNqrl7F8Bu8lFJIWi44PO5AJtUe1NnRD7pQ2ZQzk',range='Página1').execute()
# print(values)
