function emptyfield() {
    var allowance = document.getElementById("allowance").value;
    if (allowance === "") {
        document.getElementById("allowance").value = document.getElementById("allowance").placeholder

    }
}