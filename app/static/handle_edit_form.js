$(".mb-2.btn.btn-primary.mr-2.w-100").attr("disabled", true);

$(".btn.btn-info").on("click", function(){
    $("#modify").attr("disabled", true);
})

$('form').find("input").keyup(function() {
    var empty = false;
    $('form').find("input").each(function() {
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
    $('form').find("input").each(function() {
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