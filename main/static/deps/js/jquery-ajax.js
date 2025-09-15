// When the HTML document is ready (fully rendered)
$(document).ready(function () {
    // Store in a variable the markup element with id jq-notification for AJAX notifications
    var successMessage = $("#jq-notification");

    // Catch the click event on the "add to cart" button
    $(document).on("click", ".add-to-cart", function (e) {
        // Prevent the default action
        e.preventDefault();

        // Get the cart counter element and read its value
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Get the product id from the data-product-id attribute
        var product_id = $(this).data("product-id");

        // Get the link to the Django controller from the href attribute
        var add_to_cart_url = $(this).attr("href");

        // Make a POST request via AJAX without reloading the page
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Show a notification
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Hide the notification after 7 seconds
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Increase the cart item count (render in the template)
                cartCount++;
                goodsInCartCount.text(cartCount);

                // Replace the cart content with the new HTML returned by Django
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Error while adding product to cart");
            },
        });
    });




    // Catch the click event on the "remove from cart" button
    $(document).on("click", ".remove-from-cart", function (e) {
        // Prevent the default action
        e.preventDefault();

        // Get the cart counter element and read its value
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Get the cart id from the data-cart-id attribute
        var cart_id = $(this).data("cart-id");
        // Get the link to the Django controller from the href attribute
        var remove_from_cart = $(this).attr("href");

        // Make a POST request via AJAX without reloading the page
        $.ajax({

            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Show a notification
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Hide the notification after 7 seconds
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Decrease the cart item count (rendering)
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                // Replace the cart content with the new HTML returned by Django
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Error while removing product from cart");
            },
        });
    });




    // Now handle + and - for product quantity
    // Event handler for decreasing the value
    $(document).on("click", ".decrement", function () {
        // Get the Django controller URL from the data-cart-change-url attribute
        var url = $(this).data("cart-change-url");
        // Get the cart ID from the data-cart-id attribute
        var cartID = $(this).data("cart-id");
        // Find the nearest input with the quantity
        var $input = $(this).closest('.input-group').find('.number');
        // Get the current value of the quantity
        var currentValue = parseInt($input.val());
        // If the quantity is more than one, only then subtract 1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Call the function defined below
            // with arguments (cart id, new quantity, whether quantity decreased or increased, url)
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Event handler for increasing the value
    $(document).on("click", ".increment", function () {
        // Get the Django controller URL from the data-cart-change-url attribute
        var url = $(this).data("cart-change-url");
        // Get the cart ID from the data-cart-id attribute
        var cartID = $(this).data("cart-id");
        // Find the nearest input with the quantity
        var $input = $(this).closest('.input-group').find('.number');
        // Get the current value of the quantity
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Call the function defined below
        // with arguments (cart id, new quantity, whether quantity decreased or increased, url)
        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                 // Show a notification
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                 // Hide the notification after 7 seconds
                setTimeout(function () {
                     successMessage.fadeOut(400);
                }, 7000);

                // Update the total item count in the cart
                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                // Replace the cart content
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Error while updating cart");
            },
        });
    }
});
