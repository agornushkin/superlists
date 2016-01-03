$(function(){
    init();
});

function init(){
    $("input#id_text").on('keypress', function(){
        $(".has-error").hide();
    });

    $("input#id_text").click(function(){
        $(".has-error").hide();
    });
}

