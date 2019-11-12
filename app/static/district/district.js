var create_district = window.location.origin + "/district/create"

$("#exampleModal").on("shown.bs.modal", function(){
    console.log("POP UP")
})

$("form").on("submit", function(event){
    event.preventDefault();
    var district_name = $("#district").val();
    var city_name = $("#city").val();
    var data = {"district_name" : district_name, "city_name" : city_name};
    send_district_info(create_district, data).then(response => {
        console.log(response);
    })
    
})

$(".btn.btn-info").on("click", function(){
    var this_row = $(this).closest("tr");
    var district_id = this_row.find("td").eq(0).val();
    var district_name = this_row.find("td").eq(1).val();
    var city_name = this.row.find("td").eq(2).val();
})

async function send_district_info(url, data){
    const response = await fetch(url, {
        method: "POST",
        headers: {
            'Content-Type' : 'application/json'
        },
        body : JSON.stringify(data),
    });
    return await response.json();
}