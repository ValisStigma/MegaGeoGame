function update_ranking() {
    "use strict";
    if (manual_mode === 0) {
        $.getJSON('/_get_current_ranking', {current_level: current_level, current_state: current_state}, function (data) {
            var place1, place2, place3, place4, place5, place6;
            place1 = data.place1;
            place2 = data.place2;
            place3 = data.place3;
            place4 = data.place4;
            place5 = data.place5;
            place6 = data.place6;
            $("#place1").html('1. ' + place1);
            $("#place2").html('2. ' + place2);
            $("#place3").html('3. ' + place3);
            $("#place4").html('4. ' + place4);
            $("#place5").html('5. ' + place5);
            $("#place6").html('6. '  + place6);
            $("#statistics").html(data.instruction);
        });
    }
    setTimeout("update_ranking()", 10000);
}
update_ranking();