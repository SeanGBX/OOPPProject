function updateprofile(){
    var newusername = document.getElementById("e-username").value;
    alert("Profile was successfully saved.");

    var element;
    element = document.getElementById("username");
    if (element) {
        element.innerHTML = newusername;
    }

}