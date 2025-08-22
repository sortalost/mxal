# mxal
basic email client for cock.li since their web interface doesnt work due to a roundcube vulnerability.

### todo
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
