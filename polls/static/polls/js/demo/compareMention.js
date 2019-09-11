// Set new default font family and font color to mimic Bootstrap's default styling
function lineChart4(year,mention1,mention2) {
    Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#292b2c';

    var isEmpty = function (value) {
        if (value == "" || value == null || value == undefined || (value != null && typeof value == "object" && !Object.keys(value).length)) {
            return true
        } else {
            return false
        }
    };

    alert_dialog(compareKeyword,mention1,mention2);

    if(isEmpty(mention1)){
        mention1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    }
    if(isEmpty(mention2)) {
        mention2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    }

    var max1 = Math.max.apply(null, mention1);
    var max2 = Math.max.apply(null, mention2);
    var max = (Math.max(max1,max2) < 1000) ? parseInt((Math.max(max1,max2) / 100))*100: parseInt((Math.max(max1,max2) / 1000))*1000;
    var m = (max < 1000) ? max + 100 : max + 1000;

// Area Chart Example
    var ctx = document.getElementById("compareMention");
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"],
            datasets: [{
                label: keyword,
                lineTension: 0.3,
                backgroundColor: "rgba(54,188,226,0.2)",
                borderColor: "rgba(54,188,226,1)",
                pointRadius: 3,
                pointBackgroundColor: "rgba(54,188,226,1)",
                pointBorderColor: "rgba(54,188,226,1)",
                pointHoverRadius: 3,
                pointHoverBackgroundColor: "rgba(54,188,226,1)",
                pointHoverBorderColor: "rgba(54,188,226,1)",
                pointHitRadius: 50,
                pointBorderWidth: 2,
                data: mention1
            },{
                label: compareKeyword,
                lineTension: 0.3,
                backgroundColor: "rgba(127,255,142,0.2)",
                borderColor: "rgba(127,255,142,1)",
                pointRadius: 3,
                pointBackgroundColor: "rgba(127,255,142,1)",
                pointBorderColor: "rgba(127,255,142,1)",
                pointHoverRadius: 3,
                pointHoverBackgroundColor: "rgba(127,255,142,1)",
                pointHitRadius: 50,
                pointBorderWidth: 2,
                data: mention2
            }],
        },
        options: {
            responsive: true,
            //title: {
            //    display: true,
            //    text: year
            //},
            layout: {
                padding: {
                  left: 10,
                  right: 25,
                  top: 25,
                  bottom: 0
                }
            },
            tooltips: {
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                titleMarginBottom: 10,
                titleFontColor: '#6e707e',
                titleFontSize: 14,
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: true,
                intersect: false,
                mode: 'index',
                caretPadding: 10,
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    time: {
                        unit: 'date'
                    },
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 7
                    },
                    //scaleLabel: {
                    //    display: true,
                    //    labelString: 'Month'
                    //}
                }],
                yAxes: [{
                    ticks: {
                        min: 0,
                        max: m,
                        maxTicksLimit: 5
                    },
                    gridLines: {
                        color: "rgb(234, 236, 244)",
                        zeroLineColor: "rgb(234, 236, 244)",
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    },
                    //scaleLabel: {
                    //    display: true,
                    //   labelString: '언급량'
                    //}
                }],
            },
            legend: {
                display: false
            }
        }
    });
}

