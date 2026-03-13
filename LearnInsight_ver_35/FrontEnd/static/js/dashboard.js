document.addEventListener(
    "DOMContentLoaded",
    function () {
        const role =
            document.body.getAttribute(
                "data-role"
            );
        console.log(
            "Dashboard role:",
            role
        );
        applyRoleTheme(role);
    }
);

function applyRoleTheme(role) {
    const body =
        document.body;
    if (role === "student") {
        body.classList.add(
            "theme-student"
        );
    }
    if (role === "teacher") {
        body.classList.add(
            "theme-teacher"
        );
    }
    if (role === "schooladministrator") {
        body.classList.add(
            "theme-school-admin"
        );
    }
    if (role === "systemadministrator") {
        body.classList.add(
            "theme-system-admin"
        );
    }
}