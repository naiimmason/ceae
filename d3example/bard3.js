var data = [4, 8, 15, 16, 23, 42];

var width  = 420,
    barHeight = 20;

var scale = d3.scale.linear()
  .range([0, width]);

var chart = d3.select(".chart")
    .attr("width", width)

d3.tsv("data.tsv", type, function(error, data) {
  scale.domain([0, d3.max(data, function(d) { return d.value; })]);

  chart.attr("height", barHeight * data.length);

  var bar = chart.selectAll("g")
      .data(data)
    .enter().append("g")
      .attr("transform", function(d, i) { return "translate(0, " + i * barHeight
        + ")"; });

  bar.append("rect")
      .attr("width", function(d) { return scale(d.value); })
      .attr("height", barHeight - 1)

  bar.append("text")
      .attr("x", function(d) { return scale(d.value) - 10; })
      .attr("y", barHeight/2)
      .attr("dy", ".35em")
      .text(function(d) { return d.value; });
});

function type(d) {
  d.value = +d.value; // coerce to number
  return d;
}
