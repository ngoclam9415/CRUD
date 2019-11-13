var getDistrictByCity = (e) => {

    var cityId = e.options[e.selectedIndex].value;

    $.ajax({
        url: '/address/district' + `?city_id=${cityId}`,
        method: 'GET',
        contentType: 'application/json',
        beforeSend: function () {
            $("#select-district").empty();
            $('#select-district').prop("disabled", false);
        },
        success: function (data) {
            console.log(data.length)
            if (data.length > 0) {
                $('#select-district').prop("disabled", false);

                for (let i = 0; i < data.length; i++) {
                    $('#select-district').append($('<option>', {
                        value: data[i]['id'],
                        text: data[i]['name'],
                    }));
                }

            } else {
                $("#select-district").attr("disabled", true);
            }
            $('#foo').replaceWith(data);
        }
    });
}
