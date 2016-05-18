var curr_level = 10;
var curr_state = 10;
function update() {
    "use strict";
    var new_level, state, state_text;
    if (curr_level === 10) {
        $.getJSON('/_get_current_level', {current_level: current_level}, function (data) {
            current_level = data.level;
            current_state = data.state;
        });
    }
    state = current_state;
    new_level = current_level;
    if (curr_level !== new_level || (curr_level === 1 && curr_state !== state)) {
        state_text = '';
        if (state === 'schwarz') {
            state_text = 'Inaktiv <img style=\"margin-left: 20px;\" alt=\"state\" src=\"static/images/instruction-phase.png\" />';
            $("#instruction-header").removeClass('instruction-header-non-trafficlight');
            $("#instruction-header").addClass('instruction-header-trafficlight');
            $("#statistics-titel").text("Live Statistics");
        }
        if (state === 'weiss') {
            state_text = 'Läuft <img style=\"margin-left: 20px;\" alt=\"state\" src=\"static/images/playing-phase.png\" />';
            $("#instruction-header").removeClass('instruction-header-non-trafficlight');
            $("#instruction-header").addClass('instruction-header-trafficlight');
            $("#statistics-titel").text("Live Statistics");
        }
        $("#rect" + curr_level.toString()).removeClass('rect-curr');
        $("#tri" + curr_level.toString()).removeClass('tri-curr');
        $("#rect" + new_level.toString()).addClass('rect-curr');
        $("#tri" + new_level.toString()).addClass('tri-curr');
        $.getJSON('/_update_level', {current_level: new_level, current_state: state}, function (datas) {
            $("#level-title").html(datas.instruction_panel_heading + state_text + "<img style=\"float:right;\" alt=\"Color\" src=\"static/images/instruction.png\" />");
            $("#instruction-text").text(datas.instruction);
            $("#mapper").html(datas.map);
            $("#legendholder").html(datas.image);
        });
    }
    if (curr_state !== state) {
        state_text = '';
        if (state === 'schwarz') {
            state_text = 'Instruction <img style=\"margin-left: 20px;\" alt=\"state\" src=\"static/images/instruction-phase.png\" />';
            $("#instruction-header").removeClass('instruction-header-non-trafficlight');
            $("#instruction-header").addClass('instruction-header-trafficlight');
            $("#statistics-titel").text("Live Statistics");
        }
        if (state === 'weiss') {
            state_text = 'Playing <img style=\"margin-left: 20px;\" alt=\"state\" src=\"static/images/playing-phase.png\" />';
            $("#instruction-header").removeClass('instruction-header-non-trafficlight');
            $("#instruction-header").addClass('instruction-header-trafficlight');
            $("#statistics-titel").text("Live Statistics");
        }
        if (state === 0) {
            state_text = '';
            $("#instruction-header").removeClass('instruction-header-trafficlight');
            $("#instruction-header").addClass('instruction-header-non-trafficlight');
            $("#statistics-titel").text("Live Statistics");
        }
        $.getJSON('/_update_level', {current_level: new_level, current_state: state}, function (datas) {
            $("#level-title").html(datas.instruction_panel_heading + state_text + "<img style=\"float:right;\" alt=\"Color\" src=\"static/images/instruction.png\" />");
            $("#instruction-text").text(datas.instruction);
            $("#mapper").html(datas.map);
        });
    }
    curr_level = new_level;
    curr_state = state;
    setTimeout("update()", 10000);
}
update();
