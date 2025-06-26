document.addEventListener("DOMContentLoaded", function () {
    const authDiv = document.getElementById("auth-buttons");
    const access = localStorage.getItem("access");

    if (authDiv) {
        if (access) {
            authDiv.innerHTML = `
                <button class="btn btn-outline-danger btn-sm" onclick="logout()">Logout</button>
            `;
        } else {
            authDiv.innerHTML = `
                <a href="/login/" class="btn btn-outline-primary btn-sm">Login</a>
            `;
        }
    }
});

function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    alert("Logged out successfully.");
    window.location.href = "/app/login/";  // ან "/app/login/" თუ ეგ არის სწორი
}
