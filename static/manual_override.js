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
                            if(data.instruction && data.instruction.length > 0) {
                var canvas = $('<canvas id="myChart" width="282" height="200"></canvas>');
                $("#statistics").html(canvas);
                var stats = data.ranking;
                stats.sort(function(a, b){return b.points-a.points});
                var labels = [];
                var points = [];
                for(var j = 0; j < 6; j++) {
                    labels.push(stats[j].name);
                    points.push(stats[j].points);
                }
                var label = "Points";
                if(levelChosen === 3) {
                    label = 'Bikes';
                }

                else if(levelChosen === 4) {
                    label = 'Android Users';
                }

                var myChart = new Chart(canvas, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: label,
                            backgroundColor: "rgba(150, 0, 0, 1)",
                            data: points
                        }]
                    },
                    options: {
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero:true
                                }
                            }]
                        }
                    }
                });
            }
            });
            $("#live-button").removeClass('invisible-button');
            $("#rect" + current_level_chosen.toString()).removeClass('rect-chosen');
            $("#tri" + current_level_chosen.toString()).removeClass('tri-chosen');
            $("#rect" + levelChosen).addClass('rect-chosen');
            $("#tri" + levelChosen).addClass('tri-chosen');
            manual_mode = levelChosen;
            current_level_chosen = levelChosen;
        }
        return false;
    });
});