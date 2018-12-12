function updateprofile(){
    var newusername = document.getElementById("e-username").value;
    alert(newusername);

    var element;
    element = document.getElementById("username");
    if (element) {
        element.innerHTML = newusername;
    }

}