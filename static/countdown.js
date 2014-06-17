var has_begun = 1;
function showTimeLeft() {
    "use strict";
    var Digital, hours, minutes, hoursleft, minutesleft, day;
    Digital = new Date();
    day = Digital.getDate();
    hours = Digital.getHours();
    minutes = Digital.getMinutes();
    if (has_begun === 1) {
        $("#timer").html("03:00");
        if (hours - 11 >= 0 && minutes >= 0) {
            has_begun = 0;
        }
    } else {
        var endzeitpunkt = 14 * 60;
        var bis_zeitpunkt = hours * 60 + minutes;
        var rest = endzeitpunkt - bis_zeitpunkt;
        var minutesleft = rest % 60;
        var hoursleft = (rest - minutesleft) / 60;
        if (minutesleft < 10) {
            minutesleft = "0" + minutesleft;
        }
        if (hoursleft < 10) {
            hoursleft = "0" + hoursleft;
        }
        $("#timer").html(hoursleft + ":" + minutesleft);
    }

    $("#timer").html("00:00")
    
    setTimeout("showTimeLeft()", 1000);
}
showTimeLeft();