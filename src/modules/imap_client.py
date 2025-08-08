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

def fetch_inbox(user, password):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(user, password)
    mail.select("inbox")

    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    messages = []

    for eid in email_ids[-15:]:
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
    return messages[::-1]
