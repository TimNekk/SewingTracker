import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/sprea...","https://www.googleapis.com/auth/drive...","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("SewingTracker")

if __name__ == "__main__":
    pass