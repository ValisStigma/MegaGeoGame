function update_ranking() {
    "use strict";
    if (manual_mode === 0) {
        $.getJSON('/_get_current_ranking', {current_level: current_level, current_state: current_state}, function (data) {
            var place1, place2, place3, place4, place5, place6;
            var ranking = data.ranking;
            for(var i = 1; i < ranking.length; i++) {
                $("#place" + i).html(i + '. ' + ranking[i]);
            }
            $("#statistics").html(data.instruction);
        });
    }
    setTimeout("update_ranking()", 10000);
}
update_ranking();