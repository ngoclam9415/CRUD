var edit_url = window.location.origin + "/color/api/edit";

$("#exampleModal").on("shown.bs.modal", function() {
  console.log("POP UP");
});

$("#modify").on("click", function(event) {
  event.preventDefault();
  var id = $("#id_edit").val();
  var value = $("#value_edit").val();
  var data = {
    id: id,
    value: value
  };
  send_district_info(edit_url, data).then(response => {
    window.location.href = window.location.href;
  });
});

$(".btn.btn-info").on("click", function() {
  var this_row = $(this).closest("tr");
  console.log(this_row);
  var id = this_row
    .find("td")
    .eq(0)
    .text();
  var value = this_row
    .find("td")
    .eq(1)
    .text();
  console.log(this_row.find("td").eq(1));
  console.log(value + id);
  $("#id_edit").val(id);
  $("#value_edit").val(value);
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
