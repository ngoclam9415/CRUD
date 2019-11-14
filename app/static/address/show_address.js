EDIT_ADDRESS_API = '/address/edit'

$("#modify").on("click", function (event) {
    event.preventDefault();

    var dictrictId = $("#district_edit").val();
    var cityId = $("#city_edit").val();
    var addressDetail = $("#address-edit").val();
    var addressId = $("#id_edit").val();

    var data = {
        district_id: dictrictId,
        city_id: cityId,
        address_detail: addressDetail,
        address_id: addressId,
    };

    send_address_info(EDIT_ADDRESS_API, data).then(response => {
        window.location.href = window.location.href;
    });
});

$(".mb-2.btn.btn-md.btn-info.mr-1").on("click", function () {
    var currentRow = $(this).closest("tr");

    var addressId = currentRow
        .find("td")
        .eq(0)
        .text();

    var cityRow = currentRow
        .find("td")
        .eq(3);

    let cityName = cityRow.text();
    let cityId = cityRow.data("cityId");

    getDistrictByCity(cityId);

    var addressDetail = currentRow
        .find("td")
        .eq(1)
        .text();


    $("#address-edit").val(addressDetail);
    $("#city_edit option:contains(" + cityName + ")").prop("selected", true);
    $("#id_edit").val(addressId);
});

async function send_address_info(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    return await response;
}

var getDistrictByCity = (cityId) => {
    if (cityId == undefined) {

        cityId = $("#city_edit :selected").val();
    }

    $.ajax({
        url: '/address/district' + `?city_id=${cityId}`,
        method: 'GET',
        contentType: 'application/json',
        beforeSend: function () {
            $("#district_edit").empty();
            $('#district_edit').prop("disabled", false);
        },
        success: function (data) {

            if (data.length > 0) {
                $('#district_edit').prop("disabled", false);

                for (let i = 0; i < data.length; i++) {
                    $('#district_edit').append($('<option>', {
                        value: data[i]['id'],
                        text: data[i]['name'],
                    }));
                }

            } else {
                $("#district_edit").attr("disabled", true);
            }
        }
    });
}
