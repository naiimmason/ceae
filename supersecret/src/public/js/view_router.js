var app = angular.module('super-secret-graph', ['ngRoute']);

app.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {
    $routeProvider
    .when('/', {
      templateUrl: 'html/partials/welcome.html',
      controller: 'WelcomeController'
    })
    .when('/waiting', {
      templateUrl: 'html/partials/waiting.html',
      controller: 'WaitingController'
    })
    .when('/graph', {
      templateUrl: 'html/partials/graph.html',
      controller: 'GraphController'
    })
    .when('/admin', {
      templateUrl: 'html/partials/admin.html',
      controller: 'AdminController'
    })
    .otherwise({
      redirectTo: '/'
    });
  }
]);

// Create the user object that should persist across all controllers
app.service('UserProps', function() {
  var user = {
    gameids: [],
    subj_id: '',
    curgame: -1
  };

  return {
    getUser: function() {
      return user;
    },
    getCurGameID: function() {
      console.log(user);
      return user.gameids[curgame - 1];
    },
    addGameID: function(value) {
      user.gameids.push(value);
    },
    setSubjId: function(value) {
      user.subj_id = value;
    },
    setCurGame: function(value) {
      user.curgame = value;
    }
  };
});

// Connect to the server using socket.io
var socket = io.connect();


socket.on('disconnect', function() {
  console.log('disconnect');
  socket.disconnect();
});

// Controls the home screen where the user signs in
app.controller('WelcomeController', ['$scope', '$location', 'UserProps',
  function($scope, $location, UserProps) {
    $scope.subj_id = null;
    $scope.consent = false;

    // Use http post to communicate with the server that the person has started
    // and to add them to the list of users
    $scope.startExperiment = function() {
      if($scope.subj_id === 'econadmin012') {
        $location.path('admin');
      }
      else if($scope.subj_id !== null && $scope.subj_id !== "" && $scope.consent) {
        console.log('USERNAME CHECK');
        socket.emit('usernameCheck', $scope.subj_id);
      }
      else {
        // TODO: Add warning popup that they do not have a name or have not
        // consented
      }
    };

    // TODO: Add warning popup that displays that the username is taken
    socket.on('takenUsername', function() {
      console.log('Username is taken!');
    });

    // The server has told us that the name is available
    socket.on('freeUsername', function() {
      console.log('Username is free!');
      UserProps.setSubjId($scope.subj_id);
      $location.path('waiting');
      $scope.$apply();
    });
  }
]);

// Waiting page
app.controller('WaitingController', ['$scope', '$location', 'UserProps',
  function($scope, $location, UserProps) {

    // Server told us to start the game, we have been passed all of the games
    socket.on('startGame', function(data) {
      console.log(data);
      // Log the data
      console.log('START GAME!');
      gameid = data[UserProps.getUser().subj_id].gameid;
      curgame = data[UserProps.getUser().subj_id].curgame;
      console.log('Joining game ' + gameid);

      // Join the correct game room and then go to the graph page
      UserProps.addGameID(gameid);
      UserProps.setCurGame(curgame);
      socket.emit('joinGame', UserProps.getUser());
      $location.path('/graph');
      $scope.$apply();
    });
  }
]);

app.controller('GraphController', ['$scope', '$location', 'UserProps',
  function($scope, $location, UserProps) {
    $scope.game = -1;
    var GRAPH_WIDTH = 900;
    var GRAPH_HEIGHT = 400;
    $scope.results = [];
    $scope.turn = 1;
    $scope.waiting = false;
    $scope.playeroutput = 0;
    $scope.playerinvestment = 0;

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
    $scope.p1xinp = 0;
    $scope.p1iinp = 0;
    $scope.p2xinp = 0;
    $scope.p2iinp = 0;

    $scope.p1xinpreal = 0;
    $scope.p1iinpreal = 0;
    $scope.p2xinpreal = 0;
    $scope.p2iinpreal= 0;

    // Player 1 variables
    var p1x = [];
    var p1i = [];

    // Player 2 variables
    var p2x = [];
    var p2i = [];

    function genResults() {
      // RESET VARIABLES
      // Player 1 variables
      p1x = [];
      p1i = [];
      $scope.p1sales = [];
      $scope.p1inf = [];
      $scope.p1earns = [];

      // Player 2 variables
      p2x = [];
      p2i = [];
      $scope.p2sales = [];
      $scope.p2inf = [];
      $scope.p2earns = [];
      $scope.dmg = [];

      if($scope.game != -1) {
        // console.log('Going throug old data');
        var firstplayer = false;
        // console.log(' I AM - ' + UserProps.getUser().subj_id);
        // console.log('FIRST PLAYER IS  - ' + $scope.game.p1id);
        if($scope.game.p1id === UserProps.getUser().subj_id) {
          firstplayer = true;
        } else {
          firstplayer = false;
        }

        // console.log('FIRSTPLAYER = ' + firstplayer);

        // Deal with old data from previous rounds, push to correct places depending
        // on if they are first player or second player
        for(var temp1 = 0, len = $scope.results.length; temp1 < len; temp1++) {
          if (firstplayer) {
            p1x.push($scope.game.p1choices[temp1].x);
            p1i.push($scope.game.p1choices[temp1].i);

            p2x.push($scope.game.p2choices[temp1].x);
            p2i.push($scope.game.p2choices[temp1].i);

            $scope.p1sales.push($scope.results[temp1].p1sales);
            $scope.p2sales.push($scope.results[temp1].p2sales);

            $scope.p1inf.push($scope.results[temp1].p1inf);
            $scope.p2inf.push($scope.results[temp1].p2inf);

            $scope.dmg.push($scope.results[temp1].dmg);

            $scope.p1earns.push($scope.results[temp1].p1earn);
            $scope.p2earns.push($scope.results[temp1].p2earn);
          } else {
            p1x.push($scope.game.p2choices[temp1].x);
            p1i.push($scope.game.p2choices[temp1].i);

            p2x.push($scope.game.p1choices[temp1].x);
            p2i.push($scope.game.p1choices[temp1].i);

            $scope.p1sales.push($scope.results[temp1].p2sales);
            $scope.p2sales.push($scope.results[temp1].p1sales);

            $scope.p1inf.push($scope.results[temp1].p2inf);
            $scope.p2inf.push($scope.results[temp1].p1inf);

            $scope.dmg.push($scope.results[temp1].dmg);

            $scope.p1earns.push($scope.results[temp1].p2earn);
            $scope.p2earns.push($scope.results[temp1].p1earn);
          }
        }
      }

      // Loop through and predict the following rounds
      for(var temp = $scope.turn - 1; temp < timestamps; temp++){
        // Update xs and is
        p1x.push($scope.p1xinpreal);
        p1i.push($scope.p1iinpreal);

        p2x.push($scope.p2xinpreal);
        p2i.push($scope.p2iinpreal);

        // Update Sales
        $scope.p1sales.push(p1x[temp] * R);
        $scope.p2sales.push(p2x[temp] * R);

        // Update damage
        if(temp === 0) {
          $scope.dmg.push(D0 * D1 + D2 * p1x[temp] + D2 * p2x[temp]);
        } else {
          $scope.dmg.push($scope.dmg[temp - 1] * D1 + D2 * (p1x[temp] + p2x[temp]));
        }

        // Update infrastructure
        if (temp === 0) {
          if(C * p1i[temp] < $scope.dmg[temp]) {
            $scope.p1inf.push(C * p1i[temp]);
          } else {
            $scope.p1inf.push($scope.dmg[temp]);
          }

          if(C * p2i[temp] < $scope.dmg[temp]) {
            $scope.p2inf.push(C * p2i[temp]);
          } else {
            $scope.p2inf.push($scope.dmg[temp]);
          }
        }
        else {
          if((capdelta * p1i[temp - 1] + C * p1i[temp]) < $scope.dmg[temp]) {
            $scope.p1inf.push(capdelta * p1i[temp - 1] + C * p1i[temp]);
          } else {
            $scope.p1inf.push($scope.dmg[temp]);
          }

          if((capdelta * p2i[temp - 1] + C * p2i[temp]) < $scope.dmg[temp]) {
            $scope.p2inf.push(capdelta * p2i[temp - 1] + C * p2i[temp]);
          } else {
            $scope.p2inf.push($scope.dmg[temp]);
          }
        }

        // Update earnings
        $scope.p1earns.push({ 'timestamp': temp, 'profit': $scope.p1sales[temp] - $scope.dmg[temp] - p1i[temp] + $scope.p1inf[temp] * A });
        $scope.p2earns.push({ 'timestamp': temp, 'profit': $scope.p2sales[temp] - $scope.dmg[temp] - p2i[temp] + $scope.p2inf[temp] * A });
      }
    }

    genResults();
    console.log($scope.p1earns);

    // ============================================================================
    // GRAPH COMPONENTS AND UPDATE
    // ============================================================================

    var margin = {top: 30, right: 20, bottom: 30, left: 50},
        width  = GRAPH_WIDTH - margin.left - margin.right,
        height = GRAPH_HEIGHT - margin.top - margin.bottom;

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

    data1 = $scope.p1earns;
    data2 = $scope.p2earns;
    mins = [d3.min(data1, function(d) { return d.profit; }), d3.min(data2, function(d) { return d.profit; })];
    maxs = [d3.max(data1, function(d) { return d.profit; }), d3.max(data2, function(d) { return d.profit; })];

    x.domain([0, timestamps - 1]);
    y.domain([d3.min(mins), d3.max(maxs)]);

    svg.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0, ' + height + ')')
        .call(xAxis)
      .append('text')
        .attr('x', width/2 + 25)
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
        .attr('data-legend', 'YOU')
        .attr('d', line);

    svg.append('path')
        .datum(data2)
        .attr('class', 'line-2')
        .attr('data-legend', 'Competition')
        .attr('d', line);

    legend = svg.append('g')
      .attr('class', 'legend')
      .attr('transform', 'translate(50, 30)')
      .style('font-size', '12px')
      .call(d3.legend);

    $scope.updateData = function() {
      $scope.p1xinpreal = $scope.p1xinp;
      $scope.p1xinpreal *= -1;
      $scope.p1iinpreal = $scope.p1iinp;
      $scope.p1iinpreal *= -1;

      $scope.p2xinpreal = $scope.p2xinp;
      $scope.p2xinpreal *= -1;
      $scope.p2iinpreal = $scope.p2iinp;
      $scope.p2iinpreal *= -1;

      genResults();

      data1 = $scope.p1earns;
      data2 = $scope.p2earns;
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

    $scope.submitNextMove = function() {
      console.log('SUBMITTING THINGS');
      console.log('OUTPUT = ' + $scope.playeroutput);
      console.log('INVESTMENT = ' + $scope.playerinvestment);
      $scope.waiting = true;
      var userinput = {
        gameid: UserProps.getCurGameID(),
        subj_id: UserProps.getUser().subj_id,
        output: $scope.playeroutput,
        investment: $scope.playerinvestment,
        turn: $scope.turn
      };

      socket.emit('submitMove', userinput);
    };

    socket.on('nextTurn', function(data) {
      console.log('Next turn!!!!!');
      console.log(data);
      $scope.waiting = false;
      $scope.turn = data.turn;
      $scope.results = data.results;
      $scope.game = data;
      $scope.$apply();
      genResults();
      $scope.updateData();
      $scope.$apply();
    });
  }
]);


// ============================================================================
// ADMIN CONTROLS AND SUCH
// ============================================================================

app.controller('AdminController', ['$scope', '$location',
  function($scope, $location) {
    $scope.numusers = 0;
    socket.emit('getNumUsers');

    socket.on('returnNumUsers', function(data) {
      $scope.numusers = data.numusers;
      $scope.$apply();
    });

    $scope.startGame = function() {
      socket.emit('startGame');
    };
  }
]);
