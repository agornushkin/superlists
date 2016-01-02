// global $, test, equal

test("errors are visible unless there is a keypress", function(){
    equal($(".has-error").is(":visible"), true);
});

test("errors should be hidden on keypress", function(){
    $('input').trigger('keypress');
    equal($(".has-error").is(":visible"), false);
});