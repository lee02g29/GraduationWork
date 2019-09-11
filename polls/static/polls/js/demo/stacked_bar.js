Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

function barChart(str) {

    var ctx = document.getElementById("barChart");
    var myLineChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"],
            datasets: [{
                label: 'Dataset 1',
                backgroundColor: "#F7464A",
                data: [53, 72, 67, 98, 13, 57, 70, 97, 64, 15, 34, 26]

            }, {
                label: 'Dataset 2',
                backgroundColor: "#46BFBD",
                data: [50, 69, 64, 95, 10, 54, 67, 94, 61, 12, 31, 23]
            }, {
                label: 'Dataset 3',
                backgroundColor: "#FDB45C",
                data: [46, 65, 60, 91, 6, 50, 63, 90, 57, 8, 27, 19]
            }]
        },
        options: {
            title: {
                display: true,
                text: str
            },
            tooltips: {
                mode: 'index',
                intersect: false
            },
            responsive: true,
            scales: {
                xAxes: [{
                    stacked: true,
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    });
}



