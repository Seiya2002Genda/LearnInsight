console.log("School Administrator page loaded.");


/* =========================
   School Performance
========================= */

async function loadSchoolPerformance(){

    try{

        console.log("Loading school performance data...");

        const res = await fetch("/api/school_performance");
        const data = await res.json();

        console.log("School performance:", data);

        const container = document.getElementById("schoolPerformanceData");

        if(!container) return;

        container.innerHTML = `
            <p><strong>Average Score:</strong> ${data.avg_score}</p>
            <p><strong>Total Study Time:</strong> ${data.total_study_time}</p>
            <p><strong>Total Records:</strong> ${data.records}</p>
        `;

    }catch(error){

        console.error("Error loading school performance:", error);

    }

}


/* =========================
   Teacher Monitoring
========================= */

async function loadTeacherMonitoring(){

    try{

        console.log("Loading teacher monitoring data...");

        const res = await fetch("/api/teacher_monitoring");
        const data = await res.json();

        console.log("Teacher monitoring:", data);

        const container = document.getElementById("teacherMonitoringData");

        if(!container) return;

        container.innerHTML = "";

        data.forEach(teacher=>{

            const div = document.createElement("div");

            div.innerHTML = `
                <p>
                    <strong>${teacher.username}</strong><br>
                    Total Requests: ${teacher.total_requests}<br>
                    Approved: ${teacher.approved_requests}<br>
                    Pending: ${teacher.pending_requests}
                </p>
            `;

            container.appendChild(div);

        });

    }catch(error){

        console.error("Error loading teacher monitoring:", error);

    }

}


/* =========================
   Administrative Reports
========================= */

async function generateAdminReport(){

    try{

        console.log("Generating administrative report...");

        const res = await fetch("/api/admin_report");
        const data = await res.json();

        console.log("Admin report:", data);

        const container = document.getElementById("adminReportData");

        if(!container) return;

        container.innerHTML = `
            <p><strong>Total Users:</strong> ${data.total_users}</p>
            <p><strong>Total Students:</strong> ${data.total_students}</p>
            <p><strong>Total Teachers:</strong> ${data.total_teachers}</p>
            <p><strong>Total School Admins:</strong> ${data.total_school_admins}</p>
            <p><strong>Average Score:</strong> ${data.average_score}</p>
            <p><strong>Total Study Time:</strong> ${data.total_study_time}</p>
            <p><strong>Total Learning Records:</strong> ${data.total_learning_records}</p>
            <p><strong>Pending Class Requests:</strong> ${data.pending_requests}</p>
            <p><strong>Approved Class Requests:</strong> ${data.approved_requests}</p>
        `;

    }catch(error){

        console.error("Error generating report:", error);

    }

}


/* =========================
   Page Initialize
========================= */

document.addEventListener("DOMContentLoaded", function(){

    loadSchoolPerformance();
    loadTeacherMonitoring();

});