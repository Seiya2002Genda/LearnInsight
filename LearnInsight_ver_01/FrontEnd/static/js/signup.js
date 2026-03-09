document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("signupForm");

    if (form) {
        form.addEventListener("submit", function (event) {
            const password = document.getElementById("password").value;
            const confirmPassword = document.getElementById("confirm_password").value;

            if (password !== confirmPassword) {
                event.preventDefault();
                alert("Passwords do not match.");
            }
        });
    }
});