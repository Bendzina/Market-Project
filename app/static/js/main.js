document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            fetch( "/app/token/",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, password })
            })
            .then(res => res.json())
            .then(data => {
                if (data.access && data.refresh) {
                    localStorage.setItem("access_token", data.access);
                    localStorage.setItem("refresh_token", data.refresh);
                    alert("შესვლა წარმატებით შესრულდა!");
                    window.location.href = "/app/products-page/";  
                } else {
                    alert("არასწორი მონაცემები!");
                }
            })
            .catch(err => console.error("Login error:", err));
        });
    }

    // ========================== ავტორიზაციის ღილაკები ==========================
    const authButtonsContainer = document.getElementById("auth-buttons");
    const accessToken = localStorage.getItem("access_token");

    if (authButtonsContainer) {
        if (accessToken) {
            // შესული
            authButtonsContainer.innerHTML = `
                <button id="logout" style="padding: 5px 10px;">გამოსვლა</button>
            `;

            document.getElementById("logout").addEventListener("click", function () {
                localStorage.clear();
                alert("გამოსვლა შესრულდა");
                window.location.href = "/app/login/"; ///აქ შევცვალე
            });
        } else {
            // არ შესული
            authButtonsContainer.innerHTML = `
                <a href="/login/" style="padding: 5px 10px; background: #eee;">შესვლა</a>
            `;
        }
    }

    // ========================== კალათაში დამატება ==========================
    const addToCartButtons = document.querySelectorAll(".add-to-cart");

    addToCartButtons.forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.getAttribute("data-product-id");
            const accessToken = localStorage.getItem("access_token");

            fetch(`/orders/cart/add/${productId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${accessToken}`,
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ quantity: 1 }),
                credentials: "include"
            })
            .then(async response => {
                if (response.status === 401) {
                    await refreshToken();
                    return addToCartAgain(productId);
                } else if (response.ok) {
                    alert("პროდუქტი დაემატა კალათაში!");
                } else {
                    alert("დამატება ვერ მოხერხდა!");
                }
            });
        });
    });

    async function addToCartAgain(productId) {
        const newAccessToken = localStorage.getItem("access_token");

        const response = await fetch(`/orders/cart/add/${productId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${newAccessToken}`,
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ quantity: 1 }),
            credentials: "include"
        });

        if (response.ok) {
            alert("პროდუქტი დაემატა კალათაში (განახლებული ტოკენით)!");
        } else {
            alert("ტოკენის განახლების შემდეგაც ვერ დაემატა!");
        }
    }

    async function refreshToken() {
        const refresh = localStorage.getItem("refresh_token");

        const res = await fetch("/app/token/refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ refresh: refresh })
        });

        const data = await res.json();

        if (data.access) {
            localStorage.setItem("access_token", data.access);
        } else {
            alert("ტოკენის განახლება ვერ მოხერხდა, გთხოვთ გაიაროთ ხელახლა შესვლა.");
            localStorage.clear();
        }
    }
// ========================== კალათის ნახვა ==========================
const cartPage = document.getElementById("cart-items-container"); // ეს ელემენტი უნდა იყოს cart.html-ში

if (cartPage) {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        alert("გთხოვთ, გაიარეთ ავტორიზაცია კალათის სანახავად.");
    } else {
        fetch("/orders/cart/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            }
        })
        .then(res => res.json())
        .then(data => {
            if (Array.isArray(data) && data.length > 0) {
                cartPage.innerHTML = "";
                data.forEach(item => {
                    const div = document.createElement("div");
                    div.innerHTML = `
                        <p>პროდუქტი: ${item.product.name}</p>
                        <p>რაოდენობა: ${item.quantity}</p>
                        <p>ფასი: ${item.product.price}₾</p>
                        <hr>
                    `;
                    cartPage.appendChild(div);
                });
            } else {
                cartPage.innerHTML = "<p>კალათა ცარიელია.</p>";
            }
        })
        .catch(error => {
            console.error("კალათის ჩატვირთვის შეცდომა:", error);
        });
    }
}

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
const checkoutBtn = document.getElementById("checkout-btn");

if (checkoutBtn) {
    checkoutBtn.addEventListener("click", function () {
        const accessToken = localStorage.getItem("access_token");

        if (!accessToken) {
            alert("გთხოვთ, გაიაროთ ავტორიზაცია");
            return;
        }

        fetch("/orders/cart/checkout/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            },
        })
        .then(res => res.json())
        .then(data => {
            const messageDiv = document.getElementById("checkout-message");

            if (data.status === "success") {
                messageDiv.innerText = `შეკვეთა წარმატებით განხორციელდა. შეკვეთის ID: ${data.order_id}, თანხა: ${data.total_amount}₾`;
            } else {
                messageDiv.innerText = data.message || "შეცდომა გადახდისას.";
            }
        })
        .catch(error => {
            console.error("Checkout error:", error);
        });
    });
}
