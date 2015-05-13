
// ============================================================================
// MODEL VARIABLES AND EQUATIONS
// ============================================================================
// CONSTANTS
var R = 6.00;
var alpha = 1.0;
var D0 = 1.0;
var D1 = 0.5;
var D2 = 2.00;
var capdelta = 0.9;
var C = 1.0;
var A = 2.0;
var beta = 0.7;
var profdelta = 0.7;
var profscaling = 0.02;
var timestamps = 11.000;

// Player inputs
var p1xinp = 0;
var p1iinp = 0;
var p2xinp = 0;
var p2iinp= 0;

// Player 1 variables
var p1x = [];
var p1i = [];
var p1dmg = [];
var p1inf = [];
var p1effdmg = [];
var p1rev = [];
var p1prof = [];
var p1discprof = [];

// Player 2 variables
var p2x = [];
var p2i = [];
var p2dmg = [];
var p2inf = [];
var p2effdmg = [];
var p2rev = [];
var p2prof = [];
var p2discprof = [];

function genResults() {
  // RESET VARIABLES
  // Player 1 variables
  p1x = [];
  p1i = [];
  p1dmg = [];
  p1inf = [];
  p1effdmg = [];
  p1rev = [];
  p1prof = [];
  p1discprof = [];

  // Player 2 variables
  p2x = [];
  p2i = [];
  p2dmg = [];
  p2inf = [];
  p2effdmg = [];
  p2rev = [];
  p2prof = [];
  p2discprof = [];


  for(var temp = 0; temp < timestamps; temp++){
    // Update xs and is
    p1x.push(p1xinp);
    p1i.push(p1iinp);

    p2x.push(p2xinp);
    p2i.push(p2iinp);

    // Update damage
    if(temp === 0) {
      p1dmg.push(D0 * D1 + D2 * p1x[temp] + D2 * p2x[temp]);
      p2dmg.push(D0 * D1 + D2 * p2x[temp] + D2 * p1x[temp]);
    } else {
      p1dmg.push(p1dmg[temp - 1] * D1 + D2 * (p1x[temp] + p2x[temp]));
      p2dmg.push(p2dmg[temp - 1] * D1 + D2 * (p2x[temp] + p1x[temp]));
    }

    // Update infrastructure
    if (temp === 0) {
      if(C * p1i[temp] < p1dmg[temp]) {
        p1inf.push(C * p1i[temp]);
      } else {
        p1inf.push(p1dmg[temp]);
      }

      if(C * p2i[temp] < p2dmg[temp]) {
        p2inf.push(C * p2i[temp]);
      } else {
        p2inf.push(p2dmg[temp]);
      }
    }
    else {
      if((capdelta * p1i[temp - 1] + C * p1i[temp]) < p1dmg[temp]) {
        p1inf.push(capdelta * p1i[temp - 1] + C * p1i[temp]);
      } else {
        p1inf.push(p1dmg[temp]);
      }

      if((capdelta * p2i[temp - 1] + C * p2i[temp]) < p2dmg[temp]) {
        p2inf.push(capdelta * p2i[temp - 1] + C * p2i[temp]);
      } else {
        p2inf.push(p2dmg[temp]);
      }
    }

    // Update effective damage
    p1effdmg.push(p1dmg[temp] - A * p1inf[temp]);
    p2effdmg.push(p2dmg[temp] - A * p2inf[temp]);

    // Update revenue
    p1rev.push(R * p1x[temp]);
    p2rev.push(R * p2x[temp]);

    // Update profit
    p1prof.push({ 'timestamp': temp, 'profit': p1rev[temp] - p1effdmg[temp] - p1i[temp] });
    p2prof.push({ 'timestamp': temp, 'profit': p2rev[temp] - p2effdmg[temp] - p2i[temp] });

    // Update discprofit
    p1discprof.push({ 'timestamp': temp, 'profit': p1prof[temp] * Math.pow(beta, temp) });
    p2discprof.push({ 'timestamp': temp, 'profit': p2prof[temp] * Math.pow(beta, temp)});
  }
}

genResults();
console.log(p1prof);

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
}
