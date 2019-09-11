function bullet(year, association, fre) {

    var percent = [];

    var isEmpty = function (value) {
        if (value == "" || value == null || value == undefined || (value != null && typeof value == "object" && !Object.keys(value).length)) {
            return true
        } else {
            return false
        }
    };

    alert_dialog(keyword,association,fre);
    // 데이터가 없으면, 알림창

    if(isEmpty(fre)){
        fre = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    }

    var max = (Math.max.apply(null, fre) < 1000) ? parseInt(Math.max.apply(null, fre)/100)*100 : parseInt(Math.max.apply(null, fre)/1000)*1000;
    var m = (max < 1000) ? max + 100 : max + 1000;
    // 최대치를 구해 동적으로 y축의 최대값을 조정

    // 비율 저장
    for(var i in fre){
        percent.push(fre[i]/(m) * 100);
    }

    var chart = '';

    for(var i = 0 ; i <= 1; i = i + 1 ) {
        // 첫번째, 다섯번쨰 연관어 그래프
        chart += '<h4 class="small font-weight-bold chart-font">' + association[0 + 5*i] + '<span class="float-right">' + fre[0 + 5*i] + '</span></h4>';
        chart += '<div class="progress mb-4">';
        chart += '<div class="progress-bar bg-danger" role="progressbar" style=\"width:' + percent[0 + 5*i] + '%\" aria-valuenow=\"' + fre[0 + 5*i] + '\" aria-valuemin="0" aria-valuemax="100"></div>';
        chart += '</div>';

        // 두번째, 여섯번째 연관어 그래프
        chart += '<h4 class="small font-weight-bold chart-font">' + association[1 + 5*i ] + '<span class="float-right">' + fre[1 + 5*i] + '</span></h4>';
        chart += '<div class="progress mb-4">';
        chart += '<div class="progress-bar bg-warning" role="progressbar" style=\"width:' + percent[1 + 5*i] + '%\" aria-valuenow=\"' + fre[1 + 5*i] + '\" aria-valuemin="0" aria-valuemax="100"></div>'
        chart += '</div>';

        // 세번쨰, 여덟번째 연관어 그래프
        chart += ' <h4 class="small font-weight-bold chart-font">' + association[2 + 5*i] + '<span class="float-right">' + fre[2 + 5*i] + '</span></h4>';
        chart += '<div class="progress mb-4">';
        chart += '<div class="progress-bar" role="progressbar" style=\"width:' + percent[2 + 5*i] + '%\" aria-valuenow=\"' + fre[2 + 5*i] + '\" aria-valuemin="0" aria-valuemax="100"></div>';
        chart += '</div>';

        // 네번째, 아홉번째 연관어 그래프
        chart += '<h4 class="small font-weight-bold chart-font">' + association[3 + 5*i] + '<span class="float-right">' + fre[3 + 5*i] + '</span></h4>';
        chart += '<div class="progress mb-4">';
        chart += '<div class="progress-bar bg-info" role="progressbar" style=\"width:' + percent[3 + 5*i] + '%\" aria-valuenow=\"' + fre[3 + 5*i] + '\" aria-valuemin="0" aria-valuemax="100"></div>';
        chart += '</div>';

        // 다섯번째,열번째 연관어 그래프
        chart += ' <h4 class="small font-weight-bold chart-font">' + association[4+ 5*i] + '<span class="float-right">' + fre[4 + 5*i] + '</span></h4>';
        chart += '<div class="progress mb-4">';
        chart += '<div class="progress-bar bg-success" role="progressbar" style=\"width:' + percent[4 + 5*i] + '%\" aria-valuenow=\"' + fre[4 + 5*i] + '\" aria-valuemin="0" aria-valuemax="100"></div>';
        chart += '</div>';
    }

    $( "#chart" ).empty();
    // 이전 차트 삭제

    $( "#chart" ).append( chart );

}

