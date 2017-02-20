// I don't know JavaScript
// or jQuery
// - Micah Cliffe :)

var beep = function() {
    alert("Hello!");
};


$(function() {
    $("#btnAlert").click(function() {
        $.ajax({
            url: "/alert",
            data: $("form").serialize(),
            type: "POST",
            success: otherFunctionnnnnnnn,
            error: function(error) {
                console.log(error);
            }
        });
    });
});
