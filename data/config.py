from environs import Env
from oauth2client.service_account import ServiceAccountCredentials



env = Env()
env.read_env()

input_path = env.str('input_xlsx_file_path')


default_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.116 YaBrowser/22.1.1.1544 Yowser/2.5 Safari/537.36",
    "referer": "https://www.mvideo.ru/product-list-page?q=sadf+sadf&category=vstraivaemye-holodilniki-100"
}

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("sheets/creds.json", scope)
