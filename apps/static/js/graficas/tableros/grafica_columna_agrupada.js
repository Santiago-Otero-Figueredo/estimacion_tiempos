am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    var chart = am4core.create("chartdiv", am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
    
    let info = [
      {
        category: "One",
        value1: 1,
        value6: 5,
        value3: 3
      },
      {
        category: "Two",
        value1: 2,
        value2: 5,
        value3: 3
      },
      {
        category: "Three",
        value1: 3,
        value2: 5,
        value3: 4
      },
      {
        category: "Four",
        value1: 4,
        value2: 5,
        value3: 6
      },
      {
        category: "Five",
        value1: 3,
        value2: 5,
        value3: 4
      },
      {
        category: "Six",
        value1: 2,
        value2: 13,
        value3: 1
      }
    ];

    chart.data = informacion_grafica
    
    chart.colors.step = 2;
    chart.padding(30, 30, 10, 30);
    chart.legend = new am4charts.Legend();
    
    var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "category";
    categoryAxis.renderer.grid.template.location = 0;
    console.log(informacion_grafica)
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.min = 0;
    valueAxis.max = 100;
    valueAxis.strictMinMax = true;
    valueAxis.calculateTotals = true;
    valueAxis.renderer.minWidth = 50;

    conjunto_series = new Set();
    informacion_grafica.forEach( (informacion) => {
      
      Object.entries(informacion).forEach(([key, value]) => {
        if (key!='category'){
          conjunto_series.add(key)
        }
      })
    })
    console.log(conjunto_series)

    conjunto_series.forEach( (serie) => {
        crear_serie(chart, "", serie)
    })

    chart.scrollbarX = new am4core.Scrollbar();
    
}); // end am4core.ready()

function crear_serie(chart, nombre_serie, valor){
  var series1 = chart.series.push(new am4charts.ColumnSeries());
  series1.columns.template.width = am4core.percent(80);
  series1.columns.template.tooltipText = "{name}: {valueY.totalPercent.formatNumber('#.00')}%";
  series1.name = valor;
  series1.dataFields.categoryX = "category";
  series1.dataFields.valueY = valor;
  series1.dataFields.valueYShow = "totalPercent";
  series1.dataItems.template.locations.categoryX = 0.5;
  series1.stacked = true;
  series1.tooltip.pointerOrientation = "vertical";

  var bullet1 = series1.bullets.push(new am4charts.LabelBullet());
  bullet1.interactionsEnabled = false;
  bullet1.label.text = "{valueY.totalPercent.formatNumber('#.00')}%";
  bullet1.label.fill = am4core.color("#ffffff");
  bullet1.locationY = 0.5;
}