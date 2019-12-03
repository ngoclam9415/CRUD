var suggest_search_url = "/search/suggestion"

$(".mb-2.btn.btn-primary.mr-2.w-100").attr("disabled", true);

$(".btn.btn-info").on("click", function(){
    $("#modify").attr("disabled", true);
})

$('form').find("input").keyup(function() {
    var empty = false;
    $('form').find("input").not($("#search")).each(function() {
        if ($(this).val() == '') {
            console.log($(this))
            empty = true;
        }
    });

    if (empty) {
        $('#modify').attr('disabled', true);
        $(".mb-2.btn.btn-primary.mr-2.w-100").attr("disabled", true);
    } else {
        $('#modify').removeAttr('disabled');
        $(".mb-2.btn.btn-primary.mr-2.w-100").removeAttr("disabled");
    }
});

$('select').change(function() {
    var empty = false;
    $('form').find("input").not($("#search")).each(function() {
        if ($(this).val() == '') {
            console.log($(this))
            empty = true;
        }
    });

    if (empty) {
        $(".mb-2.btn.btn-primary.mr-2.w-100").attr("disabled", true);
        $('#modify').attr('disabled', true);
    } else {
        $(".mb-2.btn.btn-primary.mr-2.w-100").removeAttr("disabled");
        $('#modify').removeAttr('disabled');
    }
});

$("#search").keyup(function(){
    var empty = false;
    var search_text = $(this).val();
    if (search_text == ""){
        empty = true;
    } else {
        // send_suggest_search(suggest_search_url, search_text).then(response => {
        //     var options = {
        //         data : response.results
        //     }
        //     $(this).easyAutocomplete(options)
        // })
    }

    if (empty) {
        $(".btn.btn-outline-success.my-2.my-sm-0").attr("disabled", true);
    } else {
        $(".btn.btn-outline-success.my-2.my-sm-0").removeAttr("disabled");
    }

})

async function send_suggest_search(url, text){
    const response = await fetch(url, {
        method : "POST",
        headers : {
          'Content-Type' : 'application/json'
        },
        body : JSON.stringify({"text" : text}),
      }); 
      return await response.json();
}

var options = {
            url : function(phrase){
                    return suggest_search_url + "?text=" + phrase
                        },
            listLocation : "results"
            };
$("#search").easyAutocomplete(options)