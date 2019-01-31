function saveChanges() {
    var date1 = document.getElementById("expiryDay").value;
    var month1 = document.getElementById("expiryMonth").value;
    var year1 = document.getElementById("expiryYear").value;
    date1 = parseInt(date1);
    month1 = parseInt(month1);
    year1 = parseInt(year1);
    n = new Date();
    currentYear = n.getFullYear();
    currentMonth = n.getMonth() + 1;
    currentDay = n.getDate();
    console.log(currentYear, currentMonth, currentDay, date1, month1, year1);
    if (year1 >= currentYear) {
        var yearDifference = year1 - currentYear;
        console.log(yearDifference);
        if (month1 >= currentMonth) {
            var monthDifference = month1 - currentMonth;
            console.log(monthDifference);
            if (date1 >= currentDay) {
                var dateDifference = date1 - currentDay;
                console.log(dateDifference)


            }
            else {
                dateDifference = 0;
            }
        }
        else if (date1 >= currentDay) {
            var dateDifference1 = date1 - currentDay;
        }
        else {
            dateDifference = 0;
            monthDifference = 0;
        }

    }


    else {
        if (month1 >= currentMonth) {
            var monthDifference1 = month1 - currentMonth;
            if (date1 >= currentDay) {
                var dateDifference1 = date1 - currentDay;
            }
            else {
                dateDifference = 0;
            }
        }
        else if (date1 >= currentDay) {
            var dateDifference = date1 - currentDay;
        }
        else {
            dateDifference = 0;
            monthDifference = 0;
        }
        alert("Food item data generated!")
    }
    //console.log(dateDifference)
    var totalDays = dateDifference + monthDifference * 30 + yearDifference * 365;
    console.log(totalDays);

    var name = document.getElementById("itemName").value;
    var x = totalDays.toString();
    var y = name.toString();
    console.log(x, y);
    document.getElementById("todoInput1").value = name.toString();
    document.getElementById("todoInput2").value = totalDays.toString();
    alert("Item saved!")
}

function sure() {
    confirm("Are you sure to save? Once saved it cannot be changed!")
}