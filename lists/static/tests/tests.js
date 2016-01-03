// global $, test, equal, module

module( "module lists", {
    beforeEach: function() {
        init();
    },
    afterEach: function() {}
});


test("errors are visible unless there is a keypress", function(){
    equal($(".has-error").is(":visible"), true);
});

test("errors should be hidden on keypress", function(){
    $('#id_text').trigger('keypress');
    equal($(".has-error").is(":visible"), false);
});

test("errors should be hidden on click", function(){
    $('#id_text').click();
    equal($(".has-error").is(":visible"), false);
});