console.log("System Administrator page loaded.");

/* =========================
   User Management
========================= */

function loadUserList() {

    console.log("Loading users...");

    fetch("/api/users")
        .then(response => response.json())
        .then(data => {

            console.log("User list:", data);

        })
        .catch(error => {
            console.error("Error loading users:", error);
        });
}


function createUser(userData) {

    fetch("/api/create_user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {

        console.log("User created:", data);
        loadUserList();

    })
    .catch(error => {
        console.error("Error creating user:", error);
    });

}


/* =========================
   Database Control
========================= */

function checkDatabaseStatus() {

    console.log("Checking database status...");

    fetch("/api/database_status")
        .then(response => response.json())
        .then(data => {

            console.log("Database status:", data);

        })
        .catch(error => {
            console.error("Database error:", error);
        });
}


/* =========================
   Platform Security
========================= */

function checkSecurityLogs() {

    console.log("Checking security logs...");

    fetch("/api/security_logs")
        .then(response => response.json())
        .then(data => {

            console.log("Security logs:", data);

        })
        .catch(error => {
            console.error("Security log error:", error);
        });
}


/* =========================
   Page Initialize
========================= */

document.addEventListener("DOMContentLoaded", function () {

    loadUserList();
    checkDatabaseStatus();
    checkSecurityLogs();

});