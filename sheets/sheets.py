import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("SewingTracker").worksheets()[0]

print(sheet.update_cell(2, 2, "TEST"))

if __name__ == "__main__":
    pass