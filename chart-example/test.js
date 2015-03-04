$(function() {
    labels = ["$0-$5", "$5-$10", "$10-$15", "$15-$20", "$20-$25", "$25-$30", "$40-$5000"];
    data = [2, 4, 6, 8, 2, 1, 1];
    console.log(labels);
    if($("#myChart").get(0)) {
      // var data = [
      // {
      //   value: parseInt($("#yes").attr("value")),
      //   color: "#46BFBD",
      //   highlight: "#5AD3D1",
      //   label: "Yes"
      // },
      // {
      //   value: parseInt($("#no").attr("value")),
      //   color: "#F7464A",
      //   highlight: "#FF5A5E",
      //   label: "No"
      // }
      // ];
      var data = {
        labels: labels,
        datasets: [
            {
                label: "My First dataset",
                fillColor: "#00539f",
                strokeColor: "rgba(220,220,220,0.8)",
                highlightFill: "rgba(220,220,220,0.75)",
                highlightStroke: "rgba(220,220,220,1)",
                data: data
            }
        ]
      };


      var options =  {
        //Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
        scaleBeginAtZero : true,

        //Boolean - Whether grid lines are shown across the chart
        scaleShowGridLines : true,

        //String - Colour of the grid lines
        scaleGridLineColor : "rgba(0,0,0,.05)",

        //Number - Width of the grid lines
        scaleGridLineWidth : 1,

        //Boolean - Whether to show horizontal lines (except X axis)
        scaleShowHorizontalLines: true,

        //Boolean - Whether to show vertical lines (except Y axis)
        scaleShowVerticalLines: true,

        //Boolean - If there is a stroke on each bar
        barShowStroke : true,

        //Number - Pixel width of the bar stroke
        barStrokeWidth : 2,

        //Number - Spacing between each of the X value sets
        barValueSpacing : 5,

        //Number - Spacing between data sets within X values
        barDatasetSpacing : 1,

        //String - A legend template
        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].fillColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"


      };

      var ctx = $("#myChart").get(0).getContext("2d");
      var majChart = new Chart(ctx).Bar(data, options)
}
});
