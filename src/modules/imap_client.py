import imaplib
import email
from email.utils import parsedate_to_datetime

IMAP_SERVER = "mail.cock.li"
IMAP_PORT = 993

def test_login(user, password):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(user, password)
        mail.logout()
        return True
    except:
        return False

def fetch_folder(user, password, folder, start=0, limit=10):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(user, password)
    status, _ = mail.select(folder, readonly=True)
    if status != "OK":
        raise Exception(f"Could not select folder: {folder}")
    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    email_ids.reverse()
    selected_ids = email_ids[start:start + limit]
    try:
        date_str = parsedate_to_datetime(msg["Date"]).strftime("%d/%m/%Y %I:%M %p, %a")
    except:
        date_str = msg.get('Date') or "unknown"
    messages = []
    for eid in selected_ids:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        try:
            date_str = parsedate_to_datetime(msg["Date"]).strftime("%d/%m/%Y %I:%M %p, %a")
        except:
            date_str = msg.get('Date') or "unknown"
        messages.append({
            "id": eid.decode(),
            "from": msg["From"],
            "subject": msg["Subject"],
            "date": date_str
        })
    mail.close()
    mail.logout()
    return messages, len(email_ids)


def fetch_email(user, password, email_id, folder):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(user, password)
    mail.select(folder)
    result, msg_data = mail.fetch(email_id, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)
    body_plain = ""
    body_html = None
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition"))
            if ctype == "text/plain" and "attachment" not in disp:
                body_plain += part.get_payload(decode=True).decode(errors="ignore")
            elif ctype == "text/html" and "attachment" not in disp:
                body_html = part.get_payload(decode=True).decode(errors="ignore")
    else:
        if msg.get_content_type() == "text/plain":
            body_plain = msg.get_payload(decode=True).decode(errors="ignore")
        elif msg.get_content_type() == "text/html":
            body_html = msg.get_payload(decode=True).decode(errors="ignore")
    mail.close()
    mail.logout()
    return {
        "from": msg["From"],
        "subject": msg["Subject"],
        "date": parsedate_to_datetime(msg["Date"]).strftime("%A, %d %B %Y @ %I:%M %p"),
        "body": body_html if body_html else f"<pre>{body_plain}</pre>"
    }
