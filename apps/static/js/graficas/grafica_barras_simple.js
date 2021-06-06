function construir_grafica_barra_simple(id_grafica, datos){    
    am4core.ready(function() {
        
        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end
        
        // Create chart instance
        var chart = am4core.create(id_grafica, am4charts.XYChart);
        
        // Add data
        chart.data = datos      
        
        // Create axes
        
        var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "actividad";
        categoryAxis.renderer.grid.template.location = 0;
        categoryAxis.renderer.minGridDistance = 30;

        
        categoryAxis.renderer.labels.template.adapter.add("dy", function(dy, target) {
        if (target.dataItem && target.dataItem.index & 2 == 2) {
            return dy + 25;
        }
        return dy;
        });
        
        var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        
        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries());
        series.dataFields.valueY = "cantidad";
        series.dataFields.categoryX = "actividad";
        series.name = "cantidad";
        series.columns.template.tooltipText = "{categoryX}: [bold]{valueY}[/]";
        series.columns.template.fillOpacity = .8;
        
        var columnTemplate = series.columns.template;
        columnTemplate.strokeWidth = 2;
        columnTemplate.strokeOpacity = 1;
        
    }); // end am4core.ready()
}