var create_district = window.location.origin + "/district/api/create";
var edit_district = window.location.origin + "/district/api/edit";

$("#exampleModal").on("shown.bs.modal", function () {
  console.log("POP UP");
});

$("#modify").on("click", function (event) {
  event.preventDefault();
  var district_name = $("#district_edit").val();
  var city_id = $("#city_edit").val();
  var district_id = $("#id_edit").val();
  var data = {
    district_name: district_name,
    city_id: city_id,
    district_id: district_id
  };
  send_district_info(edit_district, data).then(response => {
    window.location.href = window.location.href;
  });
});

$(".btn.btn-info").on("click", function () {
  var this_row = $(this).closest("tr");
  console.log(this_row);
  var district_id = this_row
    .find("td")
    .eq(0)
    .text();
  var city_id = this_row
    .find("td")
    .eq(1)
    .attr("value");
  var district_name = this_row
    .find("td")
    .eq(2)
    .text();
  console.log(this_row.find("td").eq(1));
  console.log(city_id);
  $("#district_edit").val(district_name);
  $("#city_edit").val(city_id);
  $("#id_edit").val(district_id);
});

async function send_district_info(url, data) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });
  return await response.json();
}
