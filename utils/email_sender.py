import smtplib
from email.mime.text import MIMEText


class EmailSender:
    def __init__(self, email: str, password: str):
        self.email = email

        self.smtp = smtplib.SMTP('smtp.mail.ru', 587)
        self.smtp.starttls()
        self.smtp.login(email, password)
        print(f"Logged in to {email}")

    def send(self, email: str, text: str, title: str):
        msg = MIMEText(text)
        msg['Subject'] = title

        self.smtp.sendmail(self.email, email, msg.as_string())
        print(f"Отправлен {title}")
        self.smtp.close()
