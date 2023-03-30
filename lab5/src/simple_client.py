import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

def send_email(to, body, format):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'адрес отправителя'
    sender_password = 'пароль для почты для доступа ненадёжных приложений'

    if format == 'txt':
        msg = MIMEText(body, 'plain')
    elif format == 'html':
        msg = MIMEMultipart()
        html = MIMEText(body, 'html')
        msg.attach(html)

    msg['From'] = sender_email
    msg['To'] = to

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, to, msg.as_string())

if __name__ == '__main__':
    to = sys.argv[1]
    format = sys.argv[2]
    body_file_name = sys.argv[3]
    with open(body_file_name, 'r') as f:
        body = f.read()

    send_email(to, body, format)
    