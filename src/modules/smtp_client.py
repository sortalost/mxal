import smtplib
import imaplib
import time
from flask import flash
from email.mime.text import MIMEText
from email.utils import formatdate
from .imap_client import IMAP_PORT, IMAP_SERVER

SMTP_SERVER = "mail.cock.li"
SMTP_PORT = 465

def send_email(user, password, to_address, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to_address
    msg["Date"] = formatdate(localtime=True)
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(user, password)
        server.sendmail(user, [to_address], msg.as_string())
    with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT) as imap:
        imap.login(user, password)
        status, _ = imap.append(
            "Sent", 
            "\\Seen",
            imaplib.Time2Internaldate(time.time()),
            msg.as_bytes()
        )
        if status != "OK":
            flash("Could not append to 'Sent', check folder name:")
            typ, data = imap.list()
            for line in data:
                flash(line.decode())
        imap.logout()
