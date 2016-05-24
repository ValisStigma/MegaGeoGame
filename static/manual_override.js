var manual_mode = 0;
var current_level_chosen = 0;
$(function () {
    "use strict";
    $('.arrow').bind('click', function (event) {
        var buttonClicked = $(event.target).closest('.arrow');
        var levelChosen = parseInt(buttonClicked.data('level'));
        if (current_level_chosen !== levelChosen && current_level !== levelChosen) {
            $.getJSON('/_level_selected', {current_level: current_level, level_chosen: levelChosen }, function (data) {
                $("#statistics").html(data.stats);
                $("#level-title").text(data.header);
                $("#instruction-text").text(data.instruction);
                $("#mapper").html(data.map);
                $("#legendholder").html(data.legend);
            });
            $("#live-button").removeClass('invisible-button');
            $("#rect" + current_level_chosen.toString()).removeClass('rect-chosen');
            $("#tri" + current_level_chosen.toString()).removeClass('tri-chosen');
            $("#rect" + levelChosen).addClass('rect-chosen');
            $("#tri" + levelChosen).addClass('tri-chosen');
            manual_mode = levelChosen;
            current_level_chosen = levelChosen;
            $("#instruction-header").removeClass('instruction-header-trafficlight');
            $("#instruction-header").addClass('instruction-header-non-trafficlight');
        }
        return false;
    });
});