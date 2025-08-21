document.addEventListener("DOMContentLoaded", () => {
  const loadMoreBtn = document.getElementById("load-more");
  const inboxTableBody = document.getElementById("inbox-table-body");
  const loadMoreMobileBtn = document.getElementById("load-more-mobile");
  const inboxMobileList = document.getElementById("inbox-mobile-list");

  // Detect current folder dynamically (e.g. "inbox", "sent")
  const page = window.location.pathname.replace(/\/$/, '').split('/').pop();

  // --- LOAD MORE EMAILS ---
  async function fetchMoreEmails() {
    if (!inboxTableBody) return;
    const start = window.INBOX_DATA.loadedCount;
    const limit = window.INBOX_DATA.limit;

    try {
      const response = await fetch(`/api/${page}?start=${start}&limit=${limit}`);
      if (!response.ok) throw new Error("Failed to fetch emails");

      const messages = await response.json();

      if (!messages.length) {
        if (loadMoreBtn) loadMoreBtn.disabled = true;
        if (loadMoreMobileBtn) loadMoreMobileBtn.disabled = true;
        return;
      }

      appendMessages(messages, false); // append to bottom
      window.INBOX_DATA.loadedCount += messages.length;
    } catch (err) {
      console.error("Error loading more emails:", err);
    }
  }

  if (loadMoreBtn) loadMoreBtn.addEventListener("click", fetchMoreEmails);
  if (loadMoreMobileBtn) loadMoreMobileBtn.addEventListener("click", fetchMoreEmails);

  // --- DOM APPEND/PREPEND HELPERS ---
  function createDesktopRow(msg) {
    const row = document.createElement("a");
    row.href = `/${page}/${msg.id}`;
    row.className = "list-row";
    row.innerHTML = `
      <div class="row-left"><div class="from">${msg.from}</div></div>
      <div class="row-center"><div class="subject">${msg.subject}</div></div>
      <div class="row-right"><div class="date">${msg.date}</div></div>
    `;
    return row;
  }

  function createMobileCard(msg) {
    const cardLink = document.createElement("a");
    cardLink.href = `/${page}/${msg.id}`;
    cardLink.className = "card-link";
    cardLink.innerHTML = `
      <article class="card">
        <div class="card-top">
          <div class="subject">${msg.subject}</div>
          <div class="date">${msg.date}</div>
        </div>
        <div class="card-bottom">
          <div class="from">${msg.from}</div>
        </div>
      </article>
    `;
    return cardLink;
  }

  function appendMessages(messages, prepend = true) {
    if (!inboxTableBody) return;
    messages.forEach(msg => {
      const row = createDesktopRow(msg);
      if (prepend) inboxTableBody.prepend(row);
      else inboxTableBody.appendChild(row);

      if (inboxMobileList) {
        const card = createMobileCard(msg);
        if (prepend) inboxMobileList.prepend(card);
        else inboxMobileList.appendChild(card);
      }
    });
  }

  // --- AUTO-POLL FOR NEW EMAILS ---
  if (!inboxTableBody) return; // nothing to do if inbox DOM isn't present

  // Notification div (simple)
  const newEmailNotif = document.createElement("div");
  newEmailNotif.id = "new-email-notification";
  newEmailNotif.style.display = "none";
  newEmailNotif.style.position = "sticky";
  newEmailNotif.style.top = "0";
  newEmailNotif.style.backgroundColor = "#fffae6";
  newEmailNotif.style.padding = "8px";
  newEmailNotif.style.textAlign = "center";
  newEmailNotif.style.fontWeight = "bold";
  // prepend to parent if possible, otherwise to body as fallback
  if (inboxTableBody.parentElement) inboxTableBody.parentElement.prepend(newEmailNotif);
  else document.body.prepend(newEmailNotif);

  // Determine the numeric latest ID we currently have (safe parse)
  const firstRow = inboxTableBody.firstElementChild;
  let latestIdNum = 0;
  if (firstRow) {
    const href = firstRow.getAttribute("href") || "";
    const lastPart = href.replace(/\/$/, '').split("/").pop() || "0";
    latestIdNum = parseInt(lastPart, 10) || 0;
  }

  async function fetchNewEmails() {
    try {
      const response = await fetch(`/api/${page}?start=0&limit=${window.INBOX_DATA.limit}`);
      if (!response.ok) return;

      const messages = await response.json();
      if (!Array.isArray(messages) || messages.length === 0) return;

      // Keep only messages with numeric ID > latestIdNum
      const newMessages = messages.filter(m => {
        const idn = parseInt(m.id, 10);
        return !Number.isNaN(idn) && idn > latestIdNum;
      });

      if (newMessages.length) {
        // Sort ascending by id so when we prepend in order, the final top is newest
        newMessages.sort((a, b) => (parseInt(a.id, 10) || 0) - (parseInt(b.id, 10) || 0));

        appendMessages(newMessages, true); // prepend

        // update latestIdNum to the largest id we just added
        const maxNewId = Math.max(...newMessages.map(m => parseInt(m.id, 10) || 0));
        latestIdNum = Math.max(latestIdNum, maxNewId);

        // update loadedCount
        window.INBOX_DATA.loadedCount += newMessages.length;

        // notify user briefly
        newEmailNotif.textContent = `${newMessages.length} new email${newMessages.length > 1 ? "s" : ""}`;
        newEmailNotif.style.display = "block";
        setTimeout(() => { newEmailNotif.style.display = "none"; }, 5000);
      }
    } catch (err) {
      console.error("Error fetching new emails:", err);
    }
  }

  // initial immediate check (so user doesn't wait 30s)
  fetchNewEmails().catch(() => { /* ignore */ });

  // Poll every 30 seconds
  setInterval(fetchNewEmails, 30000);
});
