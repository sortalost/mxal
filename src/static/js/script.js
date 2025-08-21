document.addEventListener("DOMContentLoaded", () => {
  const loadMoreBtn = document.getElementById("load-more");
  const inboxTableBody = document.getElementById("inbox-table-body");
  const loadMoreMobileBtn = document.getElementById("load-more-mobile");
  const inboxMobileList = document.getElementById("inbox-mobile-list");

  // Detect current folder dynamically
  const page = window.location.pathname.replace(/\/$/, '').split('/').pop();

  // --- LOAD MORE EMAILS ---
  async function fetchMoreEmails() {
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

  // Event listeners
  if (loadMoreBtn) loadMoreBtn.addEventListener("click", fetchMoreEmails);
  if (loadMoreMobileBtn) loadMoreMobileBtn.addEventListener("click", fetchMoreEmails);

  // --- AUTO-POLL FOR NEW EMAILS ---
  // Notification div
  let newEmailNotif = document.createElement("div");
  newEmailNotif.id = "new-email-notification";
  newEmailNotif.style.display = "none";
  newEmailNotif.style.position = "sticky";
  newEmailNotif.style.top = "0";
  newEmailNotif.style.backgroundColor = "#fffae6";
  newEmailNotif.style.padding = "8px";
  newEmailNotif.style.textAlign = "center";
  newEmailNotif.style.fontWeight = "bold";
  inboxTableBody.parentElement.prepend(newEmailNotif);

  // Track the latest email ID (handle empty inbox)
  let firstRow = inboxTableBody.firstElementChild; // <a> instead of text node
  let latestEmailId = firstRow?.getAttribute("href")?.split("/").pop() || 0;

  // Append or prepend messages
  function appendMessages(messages, prepend = true) {
    messages.forEach(msg => {
      // Desktop row
      const row = document.createElement("a");
      row.href = `/${page}/${msg.id}`;
      row.className = "list-row";
      row.innerHTML = `
        <div class="row-left"><div class="from">${msg.from}</div></div>
        <div class="row-center"><div class="subject">${msg.subject}</div></div>
        <div class="row-right"><div class="date">${msg.date}</div></div>
      `;
      if (prepend) inboxTableBody.prepend(row);
      else inboxTableBody.appendChild(row);

      // Mobile
      if (inboxMobileList) {
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
        if (prepend) inboxMobileList.prepend(cardLink);
        else inboxMobileList.appendChild(cardLink);
      }
    });
  }

  // Fetch new emails automatically
  async function fetchNewEmails() {
    try {
      const response = await fetch(`/api/${page}?start=0&limit=${window.INBOX_DATA.limit}`);
      if (!response.ok) return;

      const messages = await response.json();

      // Only messages with ID > latestEmailId
      const newMessages = messages.filter(msg => parseInt(msg.id) > parseInt(latestEmailId));

      if (newMessages.length) {
        appendMessages(newMessages.reverse(), true); // prepend
        latestEmailId = newMessages[0].id;
        window.INBOX_DATA.loadedCount += newMessages.length;

        // Show notification
        newEmailNotif.textContent = `${newMessages.length} new email${newMessages.length > 1 ? "s" : ""}`;
        newEmailNotif.style.display = "block";

        setTimeout(() => newEmailNotif.style.display = "none", 5000);
      }

    } catch (err) {
      console.error("Error fetching new emails:", err);
    }
  }

  // Poll every 30 seconds
  setInterval(fetchNewEmails, 30000);
});
