function related(year,association,fre) {

    am4core.useTheme(am4themes_animated);
// Themes end

    var isEmpty = function (value) {
        if (value == "" || value == null || value == undefined || (value != null && typeof value == "object" && !Object.keys(value).length)) {
            return true
        } else {
            return false
        }
    };

    alert_dialog(keyword,association,fre);

    if(isEmpty(association)){

    }
    if(isEmpty(fre)){
        fre = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    }

    var chart = am4core.create("related", am4plugins_forceDirected.ForceDirectedTree);
    var networkSeries = chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())

    chart.data = [
        {
            name: year + "\n" + keyword,
            children: [
                {
                    name: association[0],
                    value: fre[0]
                },
                {
                    name: association[1],
                    value: fre[1]
                },
                {
                    name: association[2],
                    value: fre[2]

                },
                {
                    name: association[3],
                    value: fre[3]
                },
                {
                    name: association[4],
                    value: fre[4]
                },
                {
                    name: association[5],
                    value: fre[5]
                },
                {
                    name: association[6],
                    value: fre[6]
                },
                {
                    name: association[7],
                    value: fre[7]
                },
                {
                    name: association[8],
                    value: fre[8]
                },
                {
                    name: association[9],
                    value: fre[9]
                }

            ]
        }
    ];

    networkSeries.dataFields.value = "value";
    networkSeries.dataFields.name = "name";
    networkSeries.dataFields.children = "children";
    networkSeries.nodes.template.tooltipText = "{name}:{value}";
    networkSeries.nodes.template.fillOpacity = 1;
    networkSeries.manyBodyStrength = -20;
    networkSeries.links.template.strength = 0.8;
    networkSeries.minRadius = am4core.percent(7.5);

    networkSeries.nodes.template.label.text = "{name}"
    networkSeries.fontSize = 25;
}