import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("NeedSheet").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)

print("Total record:{}".format(len(list_of_hashes)))
c=len(list_of_hashes)+1

#Code to insert into Google Sheet
row = ["Add category","Add Phone Number","Add time(may be vacant)","Add text"]
index = 2
sheet.insert_row(row, index)