document.addEventListener("DOMContentLoaded", function () {
    console.log("Teacher page loaded.");
    const rows = document.querySelectorAll(".student-table tbody tr");
    rows.forEach(function (row) {
        row.addEventListener("mouseenter", function () {
            row.style.background = "#dcfce7";
        });
        row.addEventListener("mouseleave", function () {
            row.style.background = "transparent";
        });
    });

    const approveButtons = document.querySelectorAll(".approve-btn");
    const rejectButtons = document.querySelectorAll(".reject-btn");
    approveButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            const confirmed = confirm("Approve this class request?");
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
    rejectButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            const confirmed = confirm("Reject this class request?");
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
});