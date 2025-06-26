document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        axios.post("/app/api/token/", {
            username: username,
            password: password
        })
        .then(response => {
            localStorage.setItem("access", response.data.access);
            localStorage.setItem("refresh", response.data.refresh);

            alert("Login successful!");
            window.location.href = "/app/products-page/";  // ან გადამისამართე სადაც გინდა, მაგ: /cart/
        })
        .catch(error => {
            alert("Login failed: " + (error.response?.data?.detail || "Unknown error"));
        });
    });
});
