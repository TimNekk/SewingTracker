from dataclasses import dataclass

from environs import Env


env = Env()
env.read_env()

input_path = env.str('input_xlsx_file_path')

@dataclass
class Email:
    receiver = env.str('receiver_email')
    sender = env.str('sender_email')
    password = env.str('sender_email_password')


default_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.1.932 Yowser/2.5 Safari/537.36"
}
