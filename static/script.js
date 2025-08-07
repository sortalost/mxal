document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const inboxBtn = document.getElementById("inbox-btn");
  const sentBtn = document.getElementById("sent-btn");
  const composeBtn = document.getElementById("compose-btn");
  const logoutBtn = document.getElementById("logout-btn");

  loginForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(loginForm));
    console.log(data)
    console.log(JSON.stringify(data))
    const res = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const out = await res.json();
    if (out.success) location.reload();
    else document.getElementById("login-error").textContent = out.message;
  });

  inboxBtn?.addEventListener("click", () => loadMails("inbox"));
  sentBtn?.addEventListener("click", () => loadMails("sent"));

  composeBtn?.addEventListener("click", () => {
    document.getElementById("compose-form").classList.remove("hidden");
    document.getElementById("email-view").classList.add("hidden");
    document.getElementById("email-list").innerHTML = "";
  });

  logoutBtn?.addEventListener("click", async () => {
    await fetch("/logout", { method: "POST" });
    location.reload();
  });

  document.getElementById("send-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    const res = await fetch("/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const out = await res.json();
    const status = document.getElementById("send-status");
    status.textContent = out.message;
    if (out.success) e.target.reset();
  });

  async function loadMails(folder) {
    const res = await fetch(`/${folder}`);
    const out = await res.json();
    const list = document.getElementById("email-list");
    const view = document.getElementById("email-view");
    const compose = document.getElementById("compose-form");

    list.innerHTML = "";
    view.classList.add("hidden");
    compose.classList.add("hidden");

    out.forEach((msg, i) => {
      const card = document.createElement("div");
      card.innerHTML = `
        <strong>${msg.subject || "(No subject)"}</strong><br>
        From: ${msg.from}<br>
        <small>${msg.date}</small>
      `;
      card.onclick = () => readMail(i, folder);
      list.appendChild(card);
    });
  }

  async function readMail(index, folder) {
    const res = await fetch(`/read/${folder}/${index}`);
    const out = await res.json();
    const view = document.getElementById("email-view");

    document.getElementById("read-subject").textContent = out.subject;
    document.getElementById("read-from").textContent = out.from;
    document.getElementById("read-date").textContent = out.date;

    const iframe = document.getElementById("read-body");
    iframe.srcdoc = out.body;

    view.classList.remove("hidden");
  }
});
