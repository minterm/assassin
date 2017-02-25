// I don't know JavaScript
// or jQuery
// - Micah Cliffe :)

var EMPTY_SELECT = "--";

var startGame = function() {
    alert("Not implemented yet. Soz.");
};

var numPlayers = function() {
    // Find div element. Use # to find an ID. Use . to find a class.
    // "In general, you should just use querySelector and querySelectorAll.
    // These two functions are easier to use and far more powerful than 
    // what you could do with the getElement* functions. Like a wise 
    // person once said, life is too short to spend time learning about 
    // old JavaScript functions."
    var selDrop = document.querySelector("#playerNumberDrop");
    var numOpt  = document.createElement("OPTION");
    numOpt.setAttribute("value","0");
    numOpt.innerHTML = EMPTY_SELECT;
    selDrop.appendChild(numOpt);
    for (i = 0; i < 10; i++) { 
        var j = i + 1;
        var numOpt  = document.createElement("OPTION");
        numOpt.setAttribute("value",j.toString());
        numOpt.innerHTML = j.toString();
        selDrop.appendChild(numOpt);
    }
};

var playerFields = function(playerNumberDrop) {
    var playerNum = parseInt(playerNumberDrop.value);
    if (isNaN(playerNum)) return;
    var ul = document.querySelector("#infoList");

    // Remove any existing player fields
    while(ul.hasChildNodes()) {
        ul.removeChild(ul.lastChild);
    }

    // Create new player fields
    for (i = 0; i < playerNum; i++) { 
        var j = i + 1;
        var playerField = document.createElement("LI");
        var p_id = "p_" + j.toString();
        playerField.setAttribute("id", p_id);
        playerField.setAttribute("class", "playerInfo");
        playerField.innerHTML = "Player " + j.toString() + ": ";
        ul.appendChild(playerField);

        // TODO: add input things to playerField
    }
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
