async function login() {
  const res = await fetch('/api/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    credentials: 'include',
    body: JSON.stringify({
      email: document.getElementById('email').value,
      password: document.getElementById('password').value
    })
  });
  if (res.ok) {
    document.getElementById('login-box').style.display = 'none';
    document.getElementById('mailbox').style.display = 'block';
    document.getElementById('user-email').textContent = document.getElementById('email').value;
    loadInbox();
  } else {
    alert('Login failed');
  }
}

async function loadInbox() {
  const res = await fetch('/api/inbox', {credentials: 'include'});
  const data = await res.json();
  const box = document.getElementById('inbox');
  box.innerHTML = '';
  data.forEach(mail => {
    const div = document.createElement('div');
    div.className = 'mail-item';
    div.innerHTML = `<b>${mail.subject}</b><br>${mail.from} - ${mail.date}`;
    div.onclick = () => readMail(mail.id);
    box.appendChild(div);
  });
}

async function readMail(id) {
  const res = await fetch('/api/read?id=' + id, {credentials: 'include'});
  const mail = await res.json();
  document.getElementById('read-subject').textContent = mail.subject;
  document.getElementById('read-from').textContent = mail.from + ' | ' + mail.date;
  document.getElementById('read-body').textContent = mail.body;
  document.getElementById('inbox').style.display = 'none';
  document.getElementById('read-view').style.display = 'block';
}

function hideRead() {
  document.getElementById('read-view').style.display = 'none';
  document.getElementById('inbox').style.display = 'block';
}

function showCompose() {
  document.getElementById('compose-box').style.display = 'block';
}

function hideCompose() {
  document.getElementById('compose-box').style.display = 'none';
}

async function send() {
  await fetch('/api/send', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    credentials: 'include',
    body: JSON.stringify({
      to: document.getElementById('to').value,
      subject: document.getElementById('subject').value,
      body: document.getElementById('body').value
    })
  });
  alert('Sent!');
  hideCompose();
  loadInbox();
}

async function logout() {
  await fetch('/api/logout', {credentials: 'include'});
  location.reload();
}
