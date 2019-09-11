<!-- Chart code -->
// Themes begin

function bubbleChart(str) {
    am4core.useTheme(am4themes_animated);
// Themes end

    var chart = am4core.create("chartdiv", am4plugins_forceDirected.ForceDirectedTree);

    var networkSeries = chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())

    networkSeries.data = [{
        name: 'Fruity',
        children: [{
            name: 'Berry',
            children: [{
                name: 'Blackberry', value: 1
            }, {
                name: 'Raspberry', value: 1
            }, {
                name: 'Blueberry', value: 1
            }, {
                name: 'Strawberry', value: 1
            }]
        }, {
            name: 'Dried Fruit',
            children: [{
                name: 'Raisin', value: 1
            }, {
                name: 'Prune', value: 1
            }]
        }, {
            name: 'Other Fruit',
            children: [{
                name: 'Coconut', value: 1
            }, {
                name: 'Cherry', value: 1
            }, {
                name: 'Pomegranate', value: 1
            }, {
                name: 'Pineapple', value: 1
            }, {
                name: 'Grape', value: 1
            }, {
                name: 'Apple', value: 1
            }, {
                name: 'Peach', value: 1
            }, {
                name: 'Pear', value: 1
            }]
        }, {
            name: 'Citrus Fruit',
            children: [{
                name: 'Grapefruit', value: 1
            }, {
                name: 'Orange', value: 1
            }, {
                name: 'Lemon', value: 1
            }, {
                name: 'Lime', value: 1
            }]
        }]
    }];

    networkSeries.dataFields.linkWith = "linkWith";
    networkSeries.dataFields.name = "name";
    networkSeries.dataFields.id = "name";
    networkSeries.dataFields.value = "value";
    networkSeries.dataFields.children = "children";
    networkSeries.links.template.distance = 1;
    networkSeries.nodes.template.tooltipText = "{name}";
    networkSeries.nodes.template.fillOpacity = 1;
    networkSeries.nodes.template.outerCircle.scale = 1;

    networkSeries.nodes.template.label.text = "{name}"
    networkSeries.fontSize = 8;
    networkSeries.nodes.template.label.hideOversized = true;
    networkSeries.nodes.template.label.truncate = true;
    networkSeries.minRadius = am4core.percent(2);
    networkSeries.manyBodyStrength = -5;
    networkSeries.links.template.strokeOpacity = 0;
}