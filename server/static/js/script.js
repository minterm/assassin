// I don't know JavaScript
// or jQuery
// - Micah Cliffe :)

var EMPTY_SELECT = "--";

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
    for (i = 1; i < 10; i++) { 
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
    var ul   = document.querySelector("#infoList");
    var form = document.querySelector("#pInfoForm");

    // Remove any existing player fields
    while(form.hasChildNodes()) {
        form.removeChild(form.lastChild);
    }

    // Create new player fields
    for (i = 0; i < playerNum; i++) { 
        var j = i + 1;
        var playerField = document.createElement("LI");
        var p_id = "p_" + j.toString();
        playerField.setAttribute("id", p_id);
        playerField.setAttribute("class", "playerInfo");
        playerField.innerHTML = "Player " + j.toString() + ": ";

        var playerName = document.createElement("INPUT");
        playerName.setAttribute("type", "text");
        playerName.setAttribute("class", "playerNames");
        name = "p" + j.toString()
        playerName.setAttribute("name", name);
        playerName.setAttribute("value", "name");

        playerField.appendChild(playerName);
        form.appendChild(playerField);
    }
    if (playerNum > 0) {
        var submit = document.createElement("INPUT");
        submit.setAttribute("type", "submit");
        submit.setAttribute("value", "Start Game");
        form.appendChild(document.createElement("BR"));
        form.appendChild(submit);
    }
};

var nameCheck = function() {
    var playerFields = document.getElementById('pInfoForm').getElementsByTagName('*');
    var players      = [];
    for (var i = 0; i < playerFields.length; i++) {
        if (playerFields[i].tagName === "INPUT") {
            if (playerFields[i].type === "text")
                players.push(playerFields[i].value);
        }
    }
    conflict = false;
    for (var i = 0; i < players.length; i++) {
        for (var j = 0; j < players.length; j++) {
            if (j === i) continue;
            if (players[i] === players[j]) conflict = true;
        }
    }
    if (conflict) {
        alert("Please use unique names.");
        return false;
    }
    return true;
};

var download = function() {
    if (conflict) {
        alert("Please use unique names.");
        return false;
    }
    return true;
};

