
// ============================================================================
// MODEL VARIABLES AND EQUATIONS
// ============================================================================
// CONSTANTS
var delta = 0.700;
var beta = 0.700;
var alpha = 0.700;
var A = 2.000;
var timestamps = 11.000;
var D0 = 1.000;
var D1 = 0.000;
var D2 = 0.004;
var I0 = 1.000;
var I1 = 1.000;
var I2 = 0.200;
var I3 = -0.020;

// Player inputs
var p1xinp = 0;
var p1iinp = 0;
var p2xinp = 2;
var p2iinp= 0;

// Player 1 variables
var p1X = [];
var p1k = [];
var p1dam = [];
var p1inf = [];
var p1rev = [];
var p1prof = [];
var p1discprof = [];

// Player 2 variables
var p2X = [];
var p2k = [];
var p2dam = [];
var p2inf = [];
var p2rev = [];
var p2prof = [];
var p2discprof = [];

function genResults() {
  // RESET VARIABLES
  // Player 1 variables
  p1X = [];
  p1k = [];
  p1dam = [];
  p1inf = [];
  p1rev = [];
  p1prof = [];
  p1discprof = [];

  // Player 2 variables
  p2X = [];
  p2k = [];
  p2dam = [];
  p2inf = [];
  p2rev = [];
  p2prof = [];
  p2discprof = [];


  for(var temp = 0; temp < timestamps; temp++){
    // Initial temp = 0
    if(temp === 0) {
      p1X.push(p1xinp + p2xinp);
      p1k.push(p1iinp);

      p2X.push(p2xinp + p1xinp);
      p2k.push(p2iinp);
    } else {
      p1X.push(p1X[temp - 1] + p1xinp + p2xinp);
      p1k.push(p1k[temp - 1] * delta + p1iinp);

      p2X.push(p2X[temp - 1] + p2xinp + p1xinp);
      p2k.push(p2k[temp - 1] * delta + p2iinp);
    }

    // Update player 1 data
    p1dam.push(D2 * (p1X[temp] * p1X[temp]) + D1 * p1X[temp] + D0)

    p1inftemp = (I2 + I0 * p1k[temp] - I1 * p1k[temp] + I3 * p1X[temp] * p1k[temp])
    if(p1inftemp < p1dam[temp]) {
      p1inf.push(p1inftemp);
    } else {
      p1inf.push(p1dam[temp]);
    }

    p1rev.push(A * Math.pow(p1xinp, alpha));
    p1prof.push({ 'timestamp': temp, 'profit': p1rev[temp] - p1dam[temp] + p1inf[temp] });
    p1discprof.push({ 'timestamp': temp, 'profit': p1prof[temp].profit * Math.pow(beta, temp) });

    // Update player 2 data
    p2dam.push(D2 * (p2X[temp] * p2X[temp]) + D1 * p2X[temp] + D0)

    p2inftemp = (I2 + I0 * p2k[temp] - I1 * p2k[temp] + I3 * p2X[temp] * p2k[temp])
    if(p2inftemp < p2dam[temp]) {
      p2inf.push(p2inftemp);
    } else {
      p2inf.push(p2dam[temp]);
    }

    p2rev.push(A * Math.pow(p2xinp, alpha));
    p2prof.push({ 'timestamp': temp, 'profit': p2rev[temp] - p2dam[temp] + p2inf[temp] });
    p2discprof.push({ 'timestamp': temp, 'profit': p2prof[temp].profit * Math.pow(beta, temp) });
  }
};

genResults();
//console.log(p1prof);

// ============================================================================
// GRAPH COMPONENTS AND UPDATE
// ============================================================================

var margin = {top: 30, right: 20, bottom: 30, left: 50},
    width  = 960 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

//var parseDate = d3.time.format('%d-%b-%y').parse;

var x = d3.scale.linear()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient('bottom')
    .ticks(timestamps);

var yAxis = d3.svg.axis()
    .scale(y)
    .orient('left')
    .ticks(10);

var line = d3.svg.line()
    .x(function(d) { return x(d.timestamp); })
    .y(function(d) { return y(d.profit); });

var svg = d3.select('.chart').append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .attr('class', 'center-block')
  .append('g')
    .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

data1 = p1prof;
data2 = p2prof;
mins = [d3.min(data1, function(d) { return d.profit; }), d3.min(data2, function(d) { return d.profit; })];
maxs = [d3.max(data1, function(d) { return d.profit; }), d3.max(data2, function(d) { return d.profit; })];

x.domain([0, timestamps - 1]);
y.domain([d3.min(mins), d3.max(maxs)]);

svg.append('g')
    .attr('class', 'x axis')
    .attr('transform', 'translate(0, ' + height + ')')
    .call(xAxis)
  .append('text')
    .attr('x', width/2)
    .attr('y', 20)
    .attr('dy', '.71em')
    .style('text-anchor', 'end')
    .text('Game Period');

svg.append('g')
    .attr('class', 'y axis')
    .call(yAxis)
  .append('text')
    .attr('transform', 'rotate(-90)')
    .attr('y', 6)
    .attr('dy', '.71em')
    .style('text-anchor', 'end')
    .text('Profit ($)');

svg.append('path')
    .datum(data1)
    .attr('class', 'line-1')
    .attr('data-legend', 'Player 1 Profit')
    .attr('d', line);

svg.append('path')
    .datum(data2)
    .attr('class', 'line-2')
    .attr('data-legend', 'Player 2 Profit')
    .attr('d', line);

legend = svg.append('g')
  .attr('class', 'legend')
  .attr('transform', 'translate(50, 30)')
  .style('font-size', '12px')
  .call(d3.legend);

function updateData() {
  p1xinp = parseInt($('#p1xInput').val());
  p1xinp *= -1;
  p1iinp = parseInt($('#p1iInput').val());
  p1iinp *= -1;

  $('#showp1XValue').text(p1xinp);
  $('#showp1IValue').text(p1iinp);

  p2xinp = parseInt($('#p2xInput').val());
  p2xinp *= -1;
  p2iinp = parseInt($('#p2iInput').val());
  p2iinp *= -1;

  $('#showp2XValue').text(p2xinp);
  $('#showp2IValue').text(p2iinp);

  genResults();

  data1 = p1prof;
  data2 = p2prof;
  mins = [d3.min(data1, function(d) { return d.profit; }), d3.min(data2, function(d) { return d.profit; })];
  maxs = [d3.max(data1, function(d) { return d.profit; }), d3.max(data2, function(d) { return d.profit; })];

  x.domain([0, timestamps - 1]);
  y.domain([d3.min(mins), d3.max(maxs)]);

  var svg = d3.select('body').transition();

  svg.select('.line-1')
      .duration(750)
      .attr('d', line(data1));

  svg.select('.line-2')
      .duration(750)
      .attr('d', line(data2));

  svg.select('.x.axis')
      .duration(750)
      .call(xAxis);

  svg.select('.y.axis')
      .duration(750)
      .call(yAxis);
};
