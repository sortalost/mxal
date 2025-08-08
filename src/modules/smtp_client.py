import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "mail.cock.li"
SMTP_PORT = 465

def send_email(user, password, to_address, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to_address
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(user, password)
        server.sendmail(user, [to_address], msg.as_string())
