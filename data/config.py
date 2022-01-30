from dataclasses import dataclass

from environs import Env


env = Env()
env.read_env()

input_path = env.str('input_xlsx_file_path')


default_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.116 YaBrowser/22.1.1.1544 Yowser/2.5 Safari/537.36",
    "referer": "https://www.mvideo.ru/product-list-page?q=sadf+sadf&category=vstraivaemye-holodilniki-100"
}
