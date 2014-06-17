var manual_mode = 0;
var current_level_chosen = 0;

$(function () {
    "use strict";
    $('#arrow1').bind('click', function () {
        if (current_level_chosen !== 1 && current_level !== 1) {
            $.getJSON('/_level1_selected', {current_level: current_level }, function (data) {
                $("#statistics").html(data.stats);
                $("#level-title").text(data.header);
                $("#instruction-text").text(data.instruction);
                $("#mapper").html(data.map);
                $("#legendholder").html(data.legend);
            });
            $("#live-button").removeClass('invisible-button');
            $("#rect" + current_level_chosen.toString()).removeClass('rect-chosen');
            $("#tri" + current_level_chosen.toString()).removeClass('tri-chosen');
            $("#rect1").addClass('rect-chosen');
            $("#tri1").addClass('tri-chosen');
            manual_mode = 1;
            current_level_chosen = 1;
            $("#instruction-header").removeClass('instruction-header-trafficlight');
            $("#instruction-header").addClass('instruction-header-non-trafficlight');
        }
        return false;
    });
});

$(function () {
    "use strict";
    $('#arrow2').bind('click', function () {
        if (current_level_chosen !== 2 && current_level !== 2) {
            $.getJSON('/_level2_selected', {current_level: current_level }, function (data) {
                $("#statistics").html(data.stats);
                $("#level-title").text(data.header);
                $("#instruction-text").text(data.instruction);
                $("#mapper").html(data.map);
                $("#legendholder").html(data.legend);
            });
            manual_mode = 1;
            $("#rect" + current_level_chosen.toString()).removeClass('rect-chosen');
            $("#tri" + current_level_chosen.toString()).removeClass('tri-chosen');
            $("#rect2").addClass('rect-chosen');
            $("#tri2").addClass('tri-chosen');
            current_level_chosen = 2;
            $("#live-button").removeClass('invisible-button');
            $("#instruction-header").removeClass('instruction-header-trafficlight');
            $("#instruction-header").addClass('instruction-header-non-trafficlight');
        }
        return false;
    });
});

$(function () {
    "use strict";
    $('#arrow3').bind('click', function () {
        if (current_level_chosen !== 3 && current_level !== 3) {
            $.getJSON('/_level3_selected', {current_level: current_level }, function (data) {
                $("#statistics").html(data.stats);
                $("#level-title").text(data.header);
                $("#instruction-text").text(data.instruction);
                $("#mapper").html(data.map);
                $("#legendholder").html(data.legend);
            });
            manual_mode = 1;
            $("#rect" + current_level_chosen.toString()).removeClass('rect-chosen');
            $("#tri" + current_level_chosen.toString()).removeClass('tri-chosen');
            $("#rect3").addClass('rect-chosen');
            $("#tri3").addClass('tri-chosen');
            current_level_chosen = 3;
            $("#live-button").removeClass('invisible-button');
            $("#instruction-header").removeClass('instruction-header-trafficlight');
            $("#instruction-header").addClass('instruction-header-non-trafficlight');
        }
        return false;
    });
});

$(function () {
    "use strict";
    $('#arrow4').bind('click', function () {
        if (current_level_chosen !== 4 && current_level !== 4) {
            $.getJSON('/_level4_selected', {current_level: current_level }, function (data) {
                $("#statistics").html(data.stats);
                $("#level-title").text(data.header);
                $("#instruction-text").text(data.instruction);
                $("#mapper").html(data.map);
                $("#legendholder").html(data.legend);
            });
            manual_mode = 1;
            $("#rect" + current_level_chosen.toString()).removeClass('rect-chosen');
            $("#tri" + current_level_chosen.toString()).removeClass('tri-chosen');
            $("#rect4").addClass('rect-chosen');
            $("#tri4").addClass('tri-chosen');
            current_level_chosen = 4;
            $("#live-button").removeClass('invisible-button');
            $("#instruction-header").removeClass('instruction-header-trafficlight');
            $("#instruction-header").addClass('instruction-header-non-trafficlight');
        }
        return false;
    });
});

$(function () {
    "use strict";
    $('#arrow5').bind('click', function () {
        if (current_level_chosen !== 5 && current_level !== 5) {
            $.getJSON('/_level5_selected', {current_level: current_level }, function (data) {
                $("#statistics").html(data.stats);
                $("#level-title").text(data.header);
                $("#instruction-text").text(data.instruction);
                $("#mapper").html(data.map);
                $("#legendholder").html(data.legend);
            });
            manual_mode = 1;
            $("#rect" + current_level_chosen.toString()).removeClass('rect-chosen');
            $("#tri" + current_level_chosen.toString()).removeClass('tri-chosen');
            $("#rect5").addClass('rect-chosen');
            $("#tri5").addClass('tri-chosen');
            current_level_chosen = 5;
            $("#live-button").removeClass('invisible-button');
            $("#instruction-header").removeClass('instruction-header-trafficlight');
            $("#instruction-header").addClass('instruction-header-non-trafficlight');
        }
        return false;
    });
});

$(function () {
    "use strict";
    $('#arrow6').bind('click', function () {
        if (current_level_chosen !== 6 && current_level !== 6) {
            $.getJSON('/_level6_selected', {current_level: current_level }, function (data) {
                $("#statistics").html(data.stats);
                $("#level-title").text(data.header);
                $("#instruction-text").text(data.instruction);
                $("#mapper").html(data.map);
                $("#legendholder").html(data.legend);
            });
            manual_mode = 1;
            $("#rect" + current_level_chosen.toString()).removeClass('rect-chosen');
            $("#tri" + current_level_chosen.toString()).removeClass('tri-chosen');
            $("#rect6").addClass('rect-chosen');
            $("#tri6").addClass('tri-chosen');
            current_level_chosen = 6;
            $("#live-button").removeClass('invisible-button');
            $("#instruction-header").removeClass('instruction-header-trafficlight');
            $("#instruction-header").addClass('instruction-header-non-trafficlight');
        }
        return false;
    });
});