var edit_url = "/store/api/edit";

$("#exampleModal").on("shown.bs.modal", function () {
  console.log("POP UP in store");
});

$("#modify").on("click", function (event) {
  event.preventDefault();
  var id = $("#id_edit").val();
  var name = $("#name_edit").val();
  var address_id = $("#address_edit").val();
  var data = {
    id: id,
    name: name,
    address_id: address_id
  };
  send_district_info(edit_url, data).then(response => {
    window.location.href = window.location.href;
  });
});

$(".btn.btn-info").on("click", function () {
  var this_row = $(this).closest("tr");
  console.log(this_row);
  var id = this_row
    .find("td")
    .eq(0)
    .text();
  var name = this_row
    .find("td")
    .eq(1)
    .text();
  var address_id = this_row
    .find("td")
    .eq(2)
    .attr("value");
  console.log(this_row.find("td").eq(1));
  console.log(address_id);
  $("#id_edit").val(id);
  $("#name_edit").val(name);
  $("#address_edit").val(address_id);
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
