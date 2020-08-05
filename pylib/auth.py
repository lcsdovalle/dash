from google.oauth2 import service_account
import googleapiclient.discovery

class authService():
        def __init__(self,jsonfile,email):
                self.userEmail = email
                self.SERVICE_ACCOUNT_FILE = jsonfile
                self.SCOPES = [
                'https://www.googleapis.com/auth/admin.directory.user',
                'https://www.googleapis.com/auth/admin.directory.user.alias',
                'https://www.googleapis.com/auth/admin.directory.user.alias.readonly',
                'https://www.googleapis.com/auth/admin.directory.user.readonly',
                'https://www.googleapis.com/auth/admin.directory.user.security',
                'https://www.googleapis.com/auth/admin.directory.userschema',
                'https://www.googleapis.com/auth/admin.directory.userschema.readonly',
                'https://www.googleapis.com/auth/admin.directory.customer',
                'https://www.googleapis.com/auth/admin.directory.customer.readonly',
                'https://www.googleapis.com/auth/admin.directory.device.chromeos',
                'https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly',
                'https://www.googleapis.com/auth/admin.directory.device.mobile',
                'https://www.googleapis.com/auth/admin.directory.device.mobile.action',
                'https://www.googleapis.com/auth/admin.directory.device.mobile.readonly',
                'https://www.googleapis.com/auth/admin.directory.domain',
                'https://www.googleapis.com/auth/admin.directory.domain.readonly',
                'https://www.googleapis.com/auth/admin.directory.group',
                'https://www.googleapis.com/auth/admin.directory.group.member',
                'https://www.googleapis.com/auth/admin.directory.group.member.readonly',
                'https://www.googleapis.com/auth/admin.directory.group.readonly',
                'https://www.googleapis.com/auth/admin.directory.notifications',
                'https://www.googleapis.com/auth/admin.directory.orgunit',
                'https://www.googleapis.com/auth/admin.directory.orgunit.readonly',
                'https://www.googleapis.com/auth/admin.directory.resource.calendar',
                'https://www.googleapis.com/auth/admin.directory.resource.calendar.readonly',
                'https://www.googleapis.com/auth/admin.directory.rolemanagement',
                'https://www.googleapis.com/auth/admin.directory.rolemanagement.readonly',
                'https://www.googleapis.com/auth/classroom.topics',
                'https://www.googleapis.com/auth/classroom.announcements',
                'https://www.googleapis.com/auth/classroom.announcements.readonly',
                'https://www.googleapis.com/auth/classroom.courses',
                'https://www.googleapis.com/auth/classroom.courses.readonly',
                'https://www.googleapis.com/auth/classroom.coursework.me',
                'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
                'https://www.googleapis.com/auth/classroom.coursework.students',
                'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
                'https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly',
                'https://www.googleapis.com/auth/classroom.guardianlinks.students',
                'https://www.googleapis.com/auth/classroom.guardianlinks.students.readonly',
                'https://www.googleapis.com/auth/classroom.profile.emails',
                'https://www.googleapis.com/auth/classroom.profile.photos',
                'https://www.googleapis.com/auth/classroom.push-notifications',
                'https://www.googleapis.com/auth/classroom.rosters',
                'https://www.googleapis.com/auth/classroom.rosters.readonly',
                'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
                'https://www.googleapis.com/auth/classroom.student-submissions.students.readonly',
                'https://www.googleapis.com/auth/classroom.topics',
                'https://www.googleapis.com/auth/classroom.topics.readonly',             
                ]
        def getService(self,*args,**kwargs):
                credentials = service_account.Credentials.from_service_account_file(
                        self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
                delegated_credentials = credentials.with_subject(self.userEmail)

                return googleapiclient.discovery.build(args[0], args[1], credentials=delegated_credentials)
        def setScope(self,scopes):
                pass        

# auth = authService('jsons/credential.json','lucas@gsaladeaula.com.br').getService('admin','directory_v1')
# users = auth.users().list(customer="my_customer").execute()
# print(users)

