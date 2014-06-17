$(function () {
    "use strict";
    $('button#live-button').bind('click', function () {
        manual_mode = 0;
        var new_level, state, state_text;
        state = current_state;
        new_level = current_level;
        state_text = '';
        if (state === 1) {
            state_text = 'Instruction <img style=\"margin-left: 20px;\" alt=\"state\" src=\"static/images/instruction-phase.png\" />';
            $("#instruction-header").removeClass('instruction-header-non-trafficlight');
            $("#instruction-header").addClass('instruction-header-trafficlight');
        }
        if (state === 2) {
            state_text = 'Playing <img style=\"margin-left: 20px;\" alt=\"state\" src=\"static/images/playing-phase.png\" />';
            $("#instruction-header").removeClass('instruction-header-non-trafficlight');
            $("#instruction-header").addClass('instruction-header-trafficlight');
        }
        if (state === 3) {
            state_text = 'Stop <img style=\"margin-left: 20px;\" alt=\"state\" src=\"static/images/stop-phase.png\" />';
            $("#instruction-header").removeClass('instruction-header-non-trafficlight');
            $("#instruction-header").addClass('instruction-header-trafficlight');
        }
        $("#rect" + curr_level.toString()).removeClass('rect-curr');
        $("#tri" + curr_level.toString()).removeClass('tri-curr');
        $("#rect" + new_level.toString()).addClass('rect-curr');
        $("#tri" + new_level.toString()).addClass('tri-curr');
        $.getJSON('/_update_level', {current_level: new_level, current_state: state}, function (datas) {
            $("#level-title").html(state_text + "<img style=\"float:right;\" alt=\"Color\" src=\"static/images/instruction.png\" />");
            $("#instruction-text").text(datas.instruction);
            $("#mapper").html(datas.map);
            $("#legendholder").html(datas.image);
        });
        state_text = '';
        if (state === 1) {
            state_text = 'Instruction <img style=\"margin-left: 20px;\" alt=\"state\" src=\"static/images/instruction-phase.png\" />';
            $("#instruction-header").removeClass('instruction-header-non-trafficlight');
            $("#instruction-header").addClass('instruction-header-trafficlight');
        }
        if (state === 2) {
            state_text = 'Playing <img style=\"margin-left: 20px;\" alt=\"state\" src=\"static/images/playing-phase.png\" />';
            $("#instruction-header").removeClass('instruction-header-non-trafficlight');
            $("#instruction-header").addClass('instruction-header-trafficlight');
        }
        if (state === 3) {
            state_text = 'Stop <img style=\"margin-left: 20px;\" alt=\"state\" src=\"static/images/stop-phase.png\" />';
            $("#instruction-header").removeClass('instruction-header-non-trafficlight');
            $("#instruction-header").addClass('instruction-header-trafficlight');
        }
        $.getJSON('/_update_level', {current_level: new_level, current_state: state}, function (datas) {
            $("#level-title").html(state_text + "<img style=\"float:right;\" alt=\"Color\" src=\"static/images/instruction.png\" />");
            $("#instruction-text").text(datas.instruction);
            $("#mapper").html(datas.map);
        });
        $("#live-button").addClass('invisible-button');
        $("#rect" + current_level_chosen.toString()).removeClass('rect-chosen');
        $("#tri" + current_level_chosen.toString()).removeClass('tri-chosen');
        current_level_chosen = 0;
        return false;
    });
});