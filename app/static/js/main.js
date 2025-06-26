// static/js/main.js

document.addEventListener("DOMContentLoaded", function () {
    loadCart();
});

function getAccessToken() {
    return localStorage.getItem("access");
}

function loadCart() {
    axios.get("/cart/", {
        headers: {
            Authorization: `Bearer ${getAccessToken()}`
        }
    })
    .then(response => {
        const cartContainer = document.getElementById("cart-container");
        const cart = response.data;
        cartContainer.innerHTML = "";

        if (cart.items.length === 0) {
            cartContainer.innerHTML = "<p>Your cart is empty.</p>";
            document.getElementById("cart-total").innerText = "0";
            return;
        }

        let total = 0;

        cart.items.forEach(item => {
            const product = item.sku.productid;
            total += item.quantity * product.price;

            const itemDiv = document.createElement("div");
            itemDiv.innerHTML = `
                <p><strong>${product.name}</strong> - ${item.quantity} x ${product.price} ₾</p>
                <input type="number" min="0" value="${item.quantity}" onchange="updateItem(${item.id}, this.value)">
                <button onclick="deleteItem(${item.id})">Remove</button>
                <hr>
            `;
            cartContainer.appendChild(itemDiv);
        });

        document.getElementById("cart-total").innerText = total.toFixed(2);
    })
    .catch(error => {
        console.error("Error loading cart:", error);
    });
}

function updateItem(itemId, quantity) {
    axios.post(`/cart/update/${itemId}/`, { quantity: parseInt(quantity) }, {
        headers: {
            Authorization: `Bearer ${getAccessToken()}`
        }
    })
    .then(() => {
        loadCart();
    })
    .catch(error => {
        alert("Failed to update item. " + error.response?.data?.message || "");
    });
}

function deleteItem(itemId) {
    axios.post(`/cart/delete/${itemId}/`, {}, {
        headers: {
            Authorization: `Bearer ${getAccessToken()}`
        }
    })
    .then(() => {
        loadCart();
    })
    .catch(error => {
        alert("Failed to remove item. " + error.response?.data?.message || "");
    });
}

function checkout() {
    axios.post("/cart/checkout/", {}, {
        headers: {
            Authorization: `Bearer ${getAccessToken()}`
        }
    })
    .then(response => {
        alert("Order placed successfully! Order ID: " + response.data.order_id);
        loadCart();
    })
    .catch(error => {
        alert("Checkout failed: " + error.response?.data?.message || "Unknown error");
    });
}
