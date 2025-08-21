document.addEventListener("DOMContentLoaded", () => {
  const loadMoreBtn = document.getElementById("load-more");
  const inboxTableBody = document.getElementById("inbox-table-body");

  const loadMoreMobileBtn = document.getElementById("load-more-mobile");
  const inboxMobileList = document.getElementById("inbox-mobile-list");

  async function fetchMoreEmails() {
    const start = window.INBOX_DATA.loadedCount;
    const limit = window.INBOX_DATA.limit;

    try {
      const response = await fetch(`/api/inbox?start=${start}&limit=${limit}`);
      if (!response.ok) throw new Error("Failed to fetch emails");

      const messages = await response.json();

      // If no messages returned, disable button
      if (!messages.length) {
        loadMoreBtn.disabled = true;
        if (loadMoreMobileBtn) loadMoreMobileBtn.disabled = true;
        return;
      }

      // Append new messages to desktop layout
      messages.forEach(msg => {
        const row = document.createElement("a");
        row.href = `/view_email/inbox/${msg.id}`;
        row.className = "list-row";
        row.innerHTML = `
          <div class="row-left">
            <div class="from">${msg.from}</div>
          </div>
          <div class="row-center">
            <div class="subject">${msg.subject}</div>
          </div>
          <div class="row-right">
            <div class="date">${msg.date}</div>
          </div>
        `;
        inboxTableBody.appendChild(row);
      });

      // Append new messages to mobile layout
      if (inboxMobileList) {
        messages.forEach(msg => {
          const cardLink = document.createElement("a");
          cardLink.href = `/view_email/inbox/${msg.id}`;
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
          inboxMobileList.appendChild(cardLink);
        });
      }

      // Update loaded count
      window.INBOX_DATA.loadedCount += messages.length;

    } catch (err) {
      console.error("Error loading more emails:", err);
    }
  }

  // Event listeners
  if (loadMoreBtn) loadMoreBtn.addEventListener("click", fetchMoreEmails);
  if (loadMoreMobileBtn) loadMoreMobileBtn.addEventListener("click", fetchMoreEmails);
});
