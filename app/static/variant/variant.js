var edit_url = "/variants/api/edit";
$
$("#modify").on("click", function (event) {
    event.preventDefault();
    var id = $("#id_edit").val();
    var product_id = $("#product_edit").val();
    var store_id = $("#store_edit").val();
    var color_id = $("#color_edit").val();
    var price = $("#price_edit").val();

    var data = {
        id: id,
        product_id: product_id,
        store_id: store_id,
        color_id: color_id,
        price: price,
    };


    send_product_variant_info(edit_url, data).then(response => {
        window.location.href = window.location.href;
    });
});

$(".btn.btn-info").on("click", function () {
    var this_row = $(this).closest("tr");
    var id = this_row
        .find("td")
        .eq(0)
        .text();

    var product = this_row
        .find("td")
        .eq(1)
        .attr("value");

    var color = this_row
        .find("td")
        .eq(2)
        .attr("value");

    var store = this_row
        .find("td")
        .eq(3)
        .attr("value");

    var price = this_row
        .find("td")
        .eq(4)
        .text();

    $("#id_edit").val(id);
    $("#product_edit").val(product);
    $("#store_edit").val(store);
    $("#color_edit").val(color);
    $("#price_edit").val(price);
});

async function send_product_variant_info(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    return await response.json();
}
