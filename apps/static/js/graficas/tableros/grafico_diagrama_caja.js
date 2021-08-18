am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    var chart = am4core.create("chartdiv", am4charts.XYChart);
    chart.paddingRight = 20;
    
    var dateAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    dateAxis.dataFields.category = "elemento_eje_X";
    dateAxis.renderer.minGridDistance = 40;
    dateAxis.renderer.grid.template.location = 0;

    dateAxis.renderer.labels.template.adapter.add("dy", function(dy, target) {
        if (target.dataItem && target.dataItem.index & 2 == 2) {
          return dy + 25;
        }
        return dy;
      });
    
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    
    var series = chart.series.push(new am4charts.CandlestickSeries());
    series.dataFields.categoryX = "elemento_eje_X";
    series.dataFields.valueY = "close";
    series.dataFields.openValueY = "open";
    series.dataFields.lowValueY = "low";
    series.dataFields.highValueY = "high";
    series.simplifiedProcessing = true;
    series.tooltipText = "Open:${openValueY.value}\nLow:${lowValueY.value}\nHigh:${highValueY.value}\nClose:${valueY.value}\nMediana:{mediana}";
    series.riseFromOpenState = undefined;
    series.dropFromOpenState = undefined;
    
    chart.cursor = new am4charts.XYCursor();
    
    var medianaSeries = chart.series.push(new am4charts.StepLineSeries());
    medianaSeries.noRisers = true;
    medianaSeries.startLocation = 0.1;
    medianaSeries.endLocation = 0.9;
    medianaSeries.dataFields.valueY = "mediana";
    medianaSeries.dataFields.categoryX = "elemento_eje_X";
    medianaSeries.strokeWidth = 2;
    medianaSeries.stroke = am4core.color("#fff");
    
    
    var topSeries = chart.series.push(new am4charts.StepLineSeries());
    topSeries.noRisers = true;
    topSeries.startLocation = 0.2;
    topSeries.endLocation = 0.8;
    topSeries.dataFields.valueY = "high";
    topSeries.dataFields.categoryX = "elemento_eje_X";
    topSeries.stroke = chart.colors.getIndex(0);
    topSeries.strokeWidth = 2;
    
    var bottomSeries = chart.series.push(new am4charts.StepLineSeries());
    bottomSeries.noRisers = true;
    bottomSeries.startLocation = 0.2;
    bottomSeries.endLocation = 0.8;
    bottomSeries.dataFields.valueY = "low";
    bottomSeries.dataFields.categoryX = "elemento_eje_X";
    bottomSeries.stroke = chart.colors.getIndex(0);
    bottomSeries.strokeWidth = 2;
    
    
    chart.scrollbarX = new am4core.Scrollbar();
    
    chart.data = informacion_grafica;
    
      addMediana();
    
      function addMediana(){
          for(var i = 0; i < chart.data.length; i++){
              var dataItem = chart.data[i];
              dataItem.mediana = Number(dataItem.low) + (Number(dataItem.high) - Number(dataItem.low)) / 2;
          }
      }
    
    }); // end am4core.ready()