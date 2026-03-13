console.log("System Administrator page loaded.");

/* =========================
   USER LIST
========================= */
function loadUserList() {
    fetch("/api/users")
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("user-table-body");
            table.innerHTML = "";
            data.forEach(user => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>${user.role}</td>
                    <td>
                        <button onclick="deleteUser(${user.id})">
                            Delete
                        </button>
                    </td>
                `;
                table.appendChild(row);
            });
        })
        .catch(error => {
            console.error("User load error", error);
        });
}

/* =========================
   CREATE USER
========================= */
function createUser() {
    const userData = {
        username: document.getElementById("new-username").value,
        email: document.getElementById("new-email").value,
        password: document.getElementById("new-password").value,
        role: document.getElementById("new-role").value
    };

    fetch("/api/create_user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData)
    })
        .then(res => res.json())
        .then(() => {
            alert("User created");
            loadUserList();
        })
        .catch(error => {
            console.error("Create user error", error);
        });
}

/* =========================
   DELETE USER
========================= */
function deleteUser(id) {
    if (!confirm("Delete this user?")) return;
    fetch(`/api/delete_user/${id}`, {
        method: "DELETE"
    })
        .then(res => res.json())
        .then(() => {
            loadUserList();
        })
        .catch(error => {
            console.error("Delete error", error);
        });
}

/* =========================
   DATABASE STATUS
========================= */
function checkDatabaseStatus() {
    fetch("/api/database_status")
        .then(res => res.json())
        .then(data => {
            document.getElementById("database-status").innerText =
                `Status: ${data.status} | Tables: ${data.tables}`;

        })
        .catch(error => {
            console.error("Database error", error);
        });
}

/* =========================
   SECURITY LOGS
========================= */
function checkSecurityLogs() {
    fetch("/api/security_logs")
        .then(res => res.json())
        .then(data => {
            const logs = document.getElementById("security-logs");
            logs.innerHTML = "";
            data.forEach(log => {
                const li = document.createElement("li");
                li.innerText =
                    `${log.action} → ${log.target} (${log.created_at})`;
                logs.appendChild(li);
            });
        })
        .catch(error => {
            console.error("Log error", error);
        });
}

/* =========================
   INIT
========================= */
document.addEventListener("DOMContentLoaded", function () {
    loadUserList();
    checkDatabaseStatus();
    checkSecurityLogs();
});