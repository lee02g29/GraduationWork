// Set new default font family and font color to mimic Bootstrap's default styling
function lineChart3(options, pos, neg) {
    Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#292b2c';

    var isEmpty = function (value) {
        if (value == "" || value == null || value == undefined || (value != null && typeof value == "object" && !Object.keys(value).length)) {
            return true
        } else {
            return false
        }
    };

    alert_dialog(keyword,pos,neg);
    // 데이터가 없으면, 알림창

    if(isEmpty(pos)){
        pos =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    }
    if(isEmpty(neg)){
        neg =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    }

    var max1 = Math.max.apply(null, pos);
    var max2 = Math.max.apply(null, neg);

    var max = (Math.max(max1,max2) < 1000) ? parseInt((Math.max(max1,max2) / 100))*100: parseInt((Math.max(max1,max2) / 1000))*1000;
    var m = (max < 1000) ? max + 100 : max + 1000;
    // 최대치를 구해 동적으로 y축의 최대값을 조정

// Area Chart Example
    var ctx = document.getElementById("optionsChart");
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"],
            datasets: [{
                label: "Positive",
                lineTension: 0.3,
                backgroundColor: "rgba(78, 115, 223, 0.05)",
                borderColor: "rgba(78, 115, 223, 1)",
                pointRadius: 3,
                pointBackgroundColor: "rgba(78, 115, 223, 1)",
                pointBorderColor: "rgba(78, 115, 223, 1)",
                pointHoverRadius: 3,
                pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                pointHitRadius: 50,
                pointBorderWidth: 2,
                data: pos
            },{
                label: "Negative",
                lineTension: 0.3,
                backgroundColor: "rgba(216,35,2,0.2)",  //선 밑에 색상
                borderColor: "rgba(216,35,2,1)",        //선 색상
                pointRadius: 3,
                pointBackgroundColor: "rgba(216, 35, 2 , 1)", //점안쪽
                pointBorderColor: "rgba(216, 35, 2 , 1)",
                pointHoverRadius: 3,
                pointHoverBackgroundColor: "rgba(216,35,2,1)",
                pointHoverBorderColor:"rgba(216, 35, 2 , 1)",
                pointHitRadius: 50,
                pointBorderWidth: 2,
                data: neg
            }],
        },
        options: {
            responsive: true,
            // title: {
            //     display: true,
            //     text: options
            // },
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
                     //   display: true,
                     //   labelString: 'Month'
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
                     //   display: true,
                     //   labelString: '리뷰수'
                    //}
                }],
            },
            legend: {
                display: false
            }
        }
    });
}

