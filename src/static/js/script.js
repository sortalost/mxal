let loadedCount = window.INBOX_DATA.loadedCount;
const limit = window.INBOX_DATA.limit;
const page = window.location.pathname.split('/').filter(Boolean).pop();

// Load More handler
document.getElementById("load-more").addEventListener("click", () => {
    fetch(`/api/inbox?start=${loadedCount}&limit=${limit}`)
        .then(res => res.json())
        .then(data => {
            if (!Array.isArray(data) || data.length === 0) {
                document.getElementById("load-more").textContent = "No more emails";
                document.getElementById("load-more").disabled = true;
                return;
            }
            appendMessages(data);
            loadedCount += data.length;
        })
        .catch(err => console.error("Error loading more emails:", err));
});

// Live refresh (every 30 seconds)
setInterval(() => {
    fetch(`/api/inbox?start=0&limit=${limit}`)
        .then(res => res.json())
        .then(data => {
            if (!Array.isArray(data)) return;

            const firstLoadedId = getFirstLoadedId();
            const newMessages = [];

            for (let msg of data) {
                if (msg.id > firstLoadedId) {
                    newMessages.push(msg);
                }
            }

            if (newMessages.length > 0) {
                prependMessages(newMessages);
                loadedCount += newMessages.length;
            }
        })
        .catch(err => console.error("Error refreshing inbox:", err));
}, 30000); // 30 seconds

// Helper functions
function appendMessages(messages) {
    const desktopBody = document.getElementById("inbox-table-body");
    const mobileList = document.getElementById("inbox-mobile-list");

    messages.forEach(msg => {
        desktopBody.innerHTML += `
            <tr data-id="${msg.id}">
                <td class="text-truncate" style="max-width: 150px;">${msg.from}</td>
                <td><a href="/view/${page}/${msg.id}" class="text-decoration-none">${msg.subject}</a></td>
                <td>${msg.date}</td>
            </tr>
        `;
        mobileList.innerHTML += `
            <a href="/view/${page}/${msg.id}" class="text-decoration-none text-dark" data-id="${msg.id}">
                <div class="card mb-2 shadow-sm">
                    <div class="card-body">
                        <div class="fw-bold text-truncate">${msg.subject}</div>
                        <div class="small text-muted">${msg.from}</div>
                        <div class="small">${msg.date}</div>
                    </div>
                </div>
            </a>
        `;
    });
}

function prependMessages(messages) {
    const desktopBody = document.getElementById("inbox-table-body");
    const mobileList = document.getElementById("inbox-mobile-list");

    messages.reverse().forEach(msg => {
        desktopBody.insertAdjacentHTML("afterbegin", `
            <tr data-id="${msg.id}">
                <td class="text-truncate" style="max-width: 150px;">${msg.from}</td>
                <td><a href="/view/${page}/${msg.id}" class="text-decoration-none">${msg.subject}</a></td>
                <td>${msg.date}</td>
            </tr>
        `);
        mobileList.insertAdjacentHTML("afterbegin", `
            <a href="/view/${page}/${msg.id}" class="text-decoration-none text-dark" data-id="${msg.id}">
                <div class="card mb-2 shadow-sm">
                    <div class="card-body">
                        <div class="fw-bold text-truncate">${msg.subject}</div>
                        <div class="small text-muted">${msg.from}</div>
                        <div class="small">${msg.date}</div>
                    </div>
                </div>
            </a>
        `);
    });
}

function getFirstLoadedId() {
    const firstRow = document.querySelector("#inbox-table-body tr");
    return firstRow ? parseInt(firstRow.dataset.id) : 0;
}
