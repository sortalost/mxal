import imaplib
import email

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

def fetch_inbox(user, password, start=0, limit=10):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(user, password)
    mail.select("inbox")
    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    email_ids.reverse()
    selected_ids = email_ids[start:start + limit]
    messages = []
    for eid in selected_ids:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        messages.append({
            "from": msg["From"],
            "subject": msg["Subject"],
            "date": msg["Date"]
        })
    mail.close()
    mail.logout()
    return messages, len(email_ids)
