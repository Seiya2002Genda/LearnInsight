console.log("School Administrator page loaded.");

/* =========================
   School Performance
========================= */

function loadSchoolPerformance() {

    console.log("Loading school performance data...");

    fetch("/api/school_performance")
        .then(response => response.json())
        .then(data => {

            console.log("School performance:", data);

        })
        .catch(error => {
            console.error("Error loading school performance:", error);
        });
}


/* =========================
   Teacher Monitoring
========================= */

function loadTeacherMonitoring() {

    console.log("Loading teacher monitoring data...");

    fetch("/api/teacher_monitoring")
        .then(response => response.json())
        .then(data => {

            console.log("Teacher monitoring:", data);

        })
        .catch(error => {
            console.error("Error loading teacher monitoring:", error);
        });
}


/* =========================
   Administrative Reports
========================= */

function generateAdminReport() {

    console.log("Generating administrative report...");

    fetch("/api/admin_report")
        .then(response => response.json())
        .then(data => {

            console.log("Admin report:", data);

        })
        .catch(error => {
            console.error("Error generating report:", error);
        });
}


/* =========================
   Page Initialize
========================= */

document.addEventListener("DOMContentLoaded", function () {

    loadSchoolPerformance();
    loadTeacherMonitoring();

});