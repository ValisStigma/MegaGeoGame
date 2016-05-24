function update_ranking() {
    "use strict";
    if (manual_mode === 0) {
        $.getJSON('/_get_current_ranking', {current_level: current_level, current_state: current_state}, function (data) {
            var place1, place2, place3, place4, place5, place6;
            var ranking = data.ranking;
            for(var i = 0; i < ranking.length; i++) {
                $("#place" + (i + 1) ).html((i + 1) + '. ' + ranking[i]);
            }
            if(current_level === 1 && data.instruction && data.instruction !== undefined) {
                var canvas = $('<canvas id="myChart" width="282" height="200"></canvas>');
                $("#statistics").html(data.instruction);
                $("#statistics").html(canvas);
                var stats = data.instruction;
                stats.sort(function(a, b){return b.points-a.points});
                var labels = [];
                var points = [];
                for(var j = 0; j < 6; j++) {
                    labels.push(stats[j].name);
                    points.push(stats[j].points);
                }
                var myChart = new Chart(canvas, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Points',
                            fillColor: "rgba(150, 0, 0, 1)",
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
            else if(current_level === 3 && data.instruction && data.instruction !== undefined) {
                var canvas = $('<canvas id="myChart" width="282" height="200"></canvas>');
                $("#statistics").html(data.instruction);
                $("#statistics").html(canvas);
                var stats = data.instruction;
                stats.sort(function(a, b){return b.points-a.points});
                var labels = [];
                var points = [];
                for(var j = 0; j < 6; j++) {
                    labels.push(stats[j].name);
                    points.push(stats[j].points);
                }
                var myChart = new Chart(canvas, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Bikes',
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

            else if(current_level === 4 && data.instruction && data.instruction !== undefined) {
                var canvas = $('<canvas id="myChart" width="282" height="200"></canvas>');
                $("#statistics").html(data.instruction);
                $("#statistics").html(canvas);
                var stats = data.instruction;
                stats.sort(function(a, b){return b.points-a.points});
                var labels = [];
                var points = [];
                for(var j = 0; j < 6; j++) {
                    labels.push(stats[j].name);
                    points.push(stats[j].points);
                }
                var myChart = new Chart(canvas, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Android Users',
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

            else if(data.instruction && data.instruction !== undefined) {
                var canvas = $('<canvas id="myChart" width="282" height="200"></canvas>');
                $("#statistics").html(data.instruction);
                $("#statistics").html(canvas);
                var stats = data.instruction;
                stats.sort(function(a, b){return b.points-a.points});
                var labels = [];
                var points = [];
                for(var j = 0; j < 6; j++) {
                    labels.push(stats[j].name);
                    points.push(stats[j].points);
                }
                var myChart = new Chart(canvas, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Points',
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
            //$("#statistics").html(data.instruction);
        });
    }
    setTimeout("update_ranking()", 10000);
}
update_ranking();