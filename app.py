from flask import Flask, request, session, jsonify, render_template
from flask_cors import CORS
import imaplib, smtplib, email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'rtyhnmloiudsxcvbnmloi'  # Change in prod
CORS(app, supports_credentials=True)

# IMAP + SMTP Settings
IMAP_SERVER = 'mail.cock.li'
IMAP_PORT = 993
SMTP_SERVER = 'mail.cock.li'
SMTP_PORT = 587

# Helpers
def imap_connect():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(session['email'], session['password'])
    return mail

def smtp_connect():
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(session['email'], session['password'])
    return server

# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    print(data)
    session['email'] = data.get('email')
    session['password'] = data['password']
    try:
        imap = imap_connect()
        imap.logout()
        return jsonify({'status': 'ok'})
    except:
        return jsonify({'status': 'fail'}), 401

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'status': 'logged out'})

@app.route('/inbox')
def inbox():
    if 'email' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    mail = imap_connect()
    mail.select('inbox')
    typ, data = mail.search(None, 'ALL')
    mail_ids = data[0].split()[-10:][::-1]  # latest 10
    mails = []
    for num in mail_ids:
        typ, msg_data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        mails.append({
            'id': num.decode(),
            'from': msg['From'],
            'subject': msg['Subject'],
            'date': msg['Date']
        })
    mail.logout()
    return jsonify(mails)

@app.route('/read')
def read():
    mail_id = request.args.get('id')
    if 'email' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    mail = imap_connect()
    mail.select('inbox')
    typ, msg_data = mail.fetch(mail_id, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = msg.get_payload(decode=True).decode()
    mail.logout()
    return jsonify({
        'from': msg['From'],
        'subject': msg['Subject'],
        'date': msg['Date'],
        'body': body
    })

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    msg = MIMEMultipart()
    msg['From'] = session['email']
    msg['To'] = data['to']
    msg['Subject'] = data['subject']
    msg.attach(MIMEText(data['body'], 'plain'))

    server = smtp_connect()
    server.sendmail(session['email'], data['to'], msg.as_string())
    server.quit()
    return jsonify({'status': 'sent'})

if __name__ == '__main__':
    app.run(debug=True)
