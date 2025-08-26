# mxal
basic email client for cock.li since their web interface doesnt work due to a roundcube vulnerability.

### todo
- add sent emails to "Sent" folder in `smtp_client.py`:
    ```py
    with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT) as imap:
        imap.login(user, password)
        imap.append(
            "Sent", 
            "\\Seen",
            imaplib.Time2Internaldate(time.time()),
            msg.as_bytes()
            )
            imap.logout()
- add seen/unseen and remove `a:visited` css, in both functions in `imap_client.py`:
    ```py
    result, data = mail.fetch(eid, "(FLAGS RFC822.HEADER)")
    flags = data[0][0].decode()
    is_read = "\\Seen" in flags
    ```
- attachment handling (both, while sending and receiving) (?)
- delete emails (?)
- search emails:
    ```py
    mails=[]
    status, ids = mail.search(None, '(SUBJECT "search_term")')
    # ids will be a list of matching email UIDs
    for num in ids[0].split():
        status, data = mail.fetch(num, "(RFC822)")
        mails.append(data[0][1])  # raw email
    ```
