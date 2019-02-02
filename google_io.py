import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#import oauth2client
#from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('google-creds_2.json')) # json credentials you downloaded earlier

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('google-creds_2.json', scope) # get email and key from creds
#credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds

file = gspread.authorize(credentials) # authenticate with Google

sheet = file.open("sbb2017").sheet1 # open sheet

allRecs = sheet.get_all_records();

print(sheet.row_values(3))
print("\n\n")
print(sheet.col_values(3))
#print(sheet.get_all_records())
#for cell in all_cells:
#	print(cell.value)
