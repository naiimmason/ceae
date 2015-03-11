$(function() {
  console.log("Loaded results.js");

  var barchartGen = function(num){
    var labels = ["$0-$5", "$5-$10", "$10-$15", "$15-$20", "$20-$25", "$25-$30", "$30-$5000"];
    var dataset = [parseInt($("#0").attr("value")), parseInt($("#1").attr("value")), parseInt($("#2").attr("value")), parseInt($("#3").attr("value")), parseInt($("#4").attr("value")), parseInt($("#5").attr("value")), parseInt($("#6").attr("value"))];
    console.log(dataset);
    var data = 
    {
      labels: labels,
      datasets: [
        {
          label: "Bar Chart",
          fillColor: "#00539f",
          strokeColor: "rgba(220,220,220,0.8)",
          highlightFill: "rgba(220,220,220,0.75)",
          highlightStroke: "rgba(220,220,220,1)",
          data: dataset
        }
      ]
    };
    console.log(data)

    var ctx = $("#barChart" + num).get(0).getContext("2d");
    var barChart = new Chart(ctx).Bar(data);
  }

  $(document).arrive("#barChart1", function() {
    barchartGen(1);
  });
  $(document).arrive("#barChart2", function() {
    barchartGen(2);
  });
  $(document).arrive("#barChart3", function() {
    barchartGen(3);
  });
  
  $(document).arrive("#majorityChart", function() {
    console.log("RESULTS");
    if($("#majorityChart").get(0)) {
      var data = [
      {
        value: parseInt($("#yes").attr("value")),
        color: "#46BFBD",
        highlight: "#5AD3D1",
        label: "Yes"
      },
      {
        value: parseInt($("#no").attr("value")),
        color: "#F7464A",
        highlight: "#FF5A5E",
        label: "No"
      }
      ];

      var options = {
        //Boolean - Whether we should show a stroke on each segment
        segmentShowStroke : true,

        //String - The colour of each segment stroke
        segmentStrokeColor : "#fff",

        //Number - The width of each segment stroke
        segmentStrokeWidth : 2,

        //Number - The percentage of the chart that we cut out of the middle
        percentageInnerCutout : 0, // This is 0 for Pie charts

        //Number - Amount of animation steps
        animationSteps : 1,

        //String - Animation easing effect
        animationEasing : "easeOutBounce",

        //Boolean - Whether we animate the rotation of the Doughnut
        animateRotate : false,

        //Boolean - Whether we animate scaling the Doughnut from the centre
        animateScale : false,

        //String - A legend template
        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"

      }

      var ctx = $("#majorityChart").get(0).getContext("2d");
      var majChart = new Chart(ctx).Pie(data, options);
    }
  });
});
