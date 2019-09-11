// Set new default font family and font color to mimic Bootstrap's default styling
function lineChart(year, mention) {
    Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#858796'; 

    var isEmpty = function (value) {
        if (value == "" || value == null || value == undefined || (value != null && typeof value == "object" && !Object.keys(value).length)) {
            return true
        } else {
            return false
        }
    };

    if(!(isEmpty(keyword)) && isEmpty(mention)){
        swal("데이터를 찾을 수 없습니다!", "검색하신 키워드의 데이터 수집 이후 업데이트 됩니다.");
    }
    // 데이터가 없으면, 알림창

    if(isEmpty(mention)){
        mention =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    }

    var max = (Math.max.apply(null, mention)) < 1000 ? parseInt(Math.max.apply(null, mention)/100)*100: parseInt(Math.max.apply(null, mention)/1000)*1000;
    var m = (max < 1000) ? max + 100 : max + 1000;
    // 최대치를 구해 동적으로 y축의 최대값을 조정

// Area Chart Example
    var ctx = document.getElementById("mentionChart");
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"],
            datasets: [{
                label: keyword,
                lineTension: 0.3,
                backgroundColor: "rgba(78, 115, 223, 0.05)",
                borderColor: "rgba(78, 115, 223, 1)",
                pointRadius: 3,
                pointBackgroundColor: "rgba(78, 115, 223, 1)",
                pointBorderColor: "rgba(78, 115, 223, 1)",
                pointHoverRadius: 3,
                pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                pointBorderWidth: 2,
                data: mention
            }],
        },
        options: {
            responsive: true,
            // title: {
            //     display: true,
            //     text: year
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
                intersect: false
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
                    // scaleLabel: {
                    //     display: true,
                    //     labelString: 'Month'
                    // }
                }],
                yAxes: [{
                    ticks: {
                        min: 0,
                        max: m,
                        maxTicksLimit: 5
                    },
                    gridLines: {
                        // color: "rgba(0, 0, 0, .125)",
                        color: "rgb(234, 236, 244)",
                        zeroLineColor: "rgb(234, 236, 244)",
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    },
                    // scaleLabel: {
                    //     display: true,
                    //     labelString: '언급량'
                    // }
                }],
            },
            legend: {
                display: false
            }
        }
    });
}

