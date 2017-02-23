// I don't know JavaScript
// or jQuery
// - Micah Cliffe :)

var beep = function() {
    alert("Hello!");
};

var numPlayers = function() {
    // Find div element. Use # to find an ID. Use . to find a class.
    // "In general, you should just use querySelector and querySelectorAll.
    // These two functions are easier to use and far more powerful than 
    // what you could do with the getElement* functions. Like a wise 
    // person once said, life is too short to spend time learning about 
    // old JavaScript functions."
    var div = document.querySelector("#playerInfo");
    var num = document.createElement("SELECT");
    alert("wooOOOOOOt");
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
