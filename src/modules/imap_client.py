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
    result, data = mail.uid("search", None, "ALL")
    if result != "OK":
        raise Exception("Could not search folder")
    email_uids = data[0].split()
    email_uids.reverse()
    selected_uids = email_uids[start:start + limit]
    messages = []
    for uid in selected_uids:
        _, msg_data = mail.uid("fetch", uid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        try:
            date_str = parsedate_to_datetime(msg["Date"]).strftime("%d/%m/%Y %I:%M %p, %a")
        except:
            date_str = msg.get("Date") or "unknown"
        messages.append({
            "id": uid.decode(),
            "from": msg["From"],
            "subject": msg["Subject"],
            "date": date_str
        })
    mail.close()
    mail.logout()
    return messages, len(email_uids)


def fetch_email(user, password, uid, folder):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(user, password)
    mail.select(folder)
    result, msg_data = mail.uid("fetch", uid, "(RFC822)")
    if result != "OK":
        raise Exception(f"Could not fetch message UID {uid} from {folder}")
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
    try:
        date_str = parsedate_to_datetime(msg["Date"]).strftime("%d/%m/%Y %I:%M %p, %a")
    except:
        date_str = msg.get("Date") or "unknown"
    return {
        "id": uid,
        "from": msg["From"],
        "subject": msg["Subject"],
        "date": date_str,
        "body": body_html if body_html else f"<pre>{body_plain}</pre>"
    }


def trash_email(user, password, uid, from_folder, trash_folder="Trash"):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(user, password)
    status, _ = mail.select(from_folder)
    if status != "OK":
        mail.logout()
        flash(f"Could not open folder: {from_folder}")
        return None
    result, data = mail.uid("COPY", f"{uid}", f'"{trash_folder}"')
    if result[0] != "OK":
        mail.logout()
        flash(f"Failed to copy message {uid} to {trash_folder}")
        return None
    mail.uid("STORE", uid, "+FLAGS", "(\Deleted)")
    mail.expunge()
    mail.close()
    mail.logout()
    return True
