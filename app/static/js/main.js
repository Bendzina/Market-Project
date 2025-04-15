document.addEventListener("DOMContentLoaded", function () {
    // ვუსმენთ ყველა ღილაკს კლასით 'add-to-cart'
    const addToCartButtons = document.querySelectorAll(".add-to-cart");

    addToCartButtons.forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.getAttribute("data-product-id");

            fetch(`/orders/cart/add/${productId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ quantity: 1 }) // შეგიძლია დინამიურადაც მიუთითო
            })
            .then(response => {
                if (response.ok) {
                    alert("პროდუქტი დაემატა კალათაში!");
                } else {
                    alert("შეცდომა კალათაში დამატებისას!");
                }
            })
            .catch(error => {
                console.error("Error adding to cart:", error);
            });
        });
    });

    // ფუნქცია CSRF ტოკენის ასაღებად
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
