function refreshInbox() {
    fetch("{{ url_for('api_inbox') }}")
      .then(res => res.json())
      .then(data => {
          let desktopBody = document.querySelector("#inbox-table-body");
          let mobileList = document.querySelector("#inbox-mobile-list");

          if (desktopBody) desktopBody.innerHTML = "";
          if (mobileList) mobileList.innerHTML = "";

          data.forEach(msg => {
              if (desktopBody) {
                  desktopBody.innerHTML += `
                    <tr>
                        <td class="text-truncate" style="max-width: 150px;">${msg.from}</td>
                        <td><a href="/view/${msg.id}" class="text-decoration-none">${msg.subject}</a></td>
                        <td>${msg.date}</td>
                    </tr>`;
              }
              if (mobileList) {
                  mobileList.innerHTML += `
                    <a href="/view/${msg.id}" class="text-decoration-none text-dark">
                      <div class="card mb-2 shadow-sm">
                        <div class="card-body">
                          <div class="fw-bold text-truncate">${msg.subject}</div>
                          <div class="small text-muted">${msg.from}</div>
                          <div class="small">${msg.date}</div>
                        </div>
                      </div>
                    </a>`;
              }
          });
      });
}

setInterval(refreshInbox, 30000);