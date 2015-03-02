$(function() {
  console.log("Loaded results.js");
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

      var ctx = $("#majorityChart").get(0).getContext("2d");
      var majChart = new Chart(ctx).Pie(data)
    }
  });
});
