function emptyfield(){
    var username = document.getElementById("e-username").value;
    var name = document.getElementById("e-name").value;
    var email = document.getElementById("e-email").value;
    if (username === ""){
        document.getElementById("e-username").value = document.getElementById("e-username").placeholder
    }
    if (name === ""){
        document.getElementById("e-name").value = document.getElementById("e-name").placeholder
    }
    if (email === ""){
        document.getElementById("e-email").value = document.getElementById("e-email").placeholder
    }

}