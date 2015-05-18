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
    .when('/reconnect', {
      templateUrl: 'html/partials/reconnect.html',
      controller: 'RecController'
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
    curgame: -1,
    player2: false
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
    },
    setPlayer2: function(value) {
      user.player2 = value;
    },
    isPlayer2: function() {
      return user.player2;
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
    $scope.sequential = false;
    $scope.game = -1;
    var GRAPH_WIDTH = 600;
    var GRAPH_HEIGHT = 350;
    $scope.results = [];
    $scope.turn = 1;
    $scope.waiting = false;
    $scope.playeroutput = 0;
    $scope.playerinvestment = 0;
    $scope.gameover = false;
    $scope.turns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    // ============================================================================
    // MODEL VARIABLES AND EQUATIONS
    // ============================================================================
    // CONSTANTS
    var R = 1.40;
    var alpha = 1.0;
    var D0 = 0.0;
    var D1 = 0.5;
    var D2 = 1.50;
    var capdelta = 0.9;
    var C = 1.0;
    var A = 2.2;
    var beta = 0.7;
    var profdelta = 0.7;
    var profscaling = 0.1;
    var timestamps = 10.00;
    var initialbalance = 25.00;

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
    $scope.p1x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    $scope.p1i = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    var p1acearns = [];

    // Player 2 variables
    $scope.p2x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    $scope.p2i = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    var p2acearns = [];

    function genResults() {
      // RESET VARIABLES
      // Player 1 variables
      p1acearns = [];
      $scope.p1sales = [];
      $scope.p1inf = [];
      $scope.p1earns = [];
      $scope.p1totalearns = [];

      // Player 2 variables
      p2acearns = [];
      $scope.p2sales = [];
      $scope.p2inf = [];
      $scope.p2earns = [];
      $scope.p2totalearns = [];
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
            $scope.p1x[temp1] = ($scope.game.p1choices[temp1].x);
            $scope.p1i[temp1] = ($scope.game.p1choices[temp1].i);

            $scope.p2x[temp1] = ($scope.game.p2choices[temp1].x);
            $scope.p2i[temp1] = ($scope.game.p2choices[temp1].i);

            $scope.p1sales.push($scope.results[temp1].p1sales);
            $scope.p2sales.push($scope.results[temp1].p2sales);

            $scope.p1inf.push($scope.results[temp1].p1inf);
            $scope.p2inf.push($scope.results[temp1].p2inf);

            $scope.dmg.push($scope.results[temp1].dmg);

            $scope.p1earns.push($scope.results[temp1].p1earn);
            $scope.p2earns.push($scope.results[temp1].p2earn);

            $scope.p1totalearns.push($scope.results[temp1].p1totalearn);
            $scope.p2totalearns.push($scope.results[temp1].p2totalearn);
          } else {
            $scope.p1x[temp1] = ($scope.game.p2choices[temp1].x);
            $scope.p1i[temp1] = ($scope.game.p2choices[temp1].i);

            $scope.p2x[temp1] = ($scope.game.p1choices[temp1].x);
            $scope.p2i[temp1] = ($scope.game.p1choices[temp1].i);

            $scope.p1sales.push($scope.results[temp1].p2sales);
            $scope.p2sales.push($scope.results[temp1].p1sales);

            $scope.p1inf.push($scope.results[temp1].p2inf);
            $scope.p2inf.push($scope.results[temp1].p1inf);

            $scope.dmg.push($scope.results[temp1].dmg);

            $scope.p1earns.push($scope.results[temp1].p2earn);
            $scope.p2earns.push($scope.results[temp1].p1earn);

            $scope.p1totalearns.push($scope.results[temp1].p2totalearn);
            $scope.p2totalearns.push($scope.results[temp1].p1totalearn);
          }
        }
      }

      // Loop through and predict the following rounds
      for(var temp = $scope.turn - 1; temp < timestamps; temp++){
        // Update Sales
        $scope.p1sales.push($scope.p1x[temp] * R);
        $scope.p2sales.push($scope.p2x[temp] * R);

        // Update damage
        if(temp === 0) {
          $scope.dmg.push(D0 * D1 + D2 * ($scope.p1x[temp] + $scope.p2x[temp]));
        } else {
          $scope.dmg.push($scope.dmg[temp - 1] * D1 + D2 * ($scope.p1x[temp] + $scope.p2x[temp]));
        }

        // Update infrastructure
        if (temp === 0) {
          $scope.p1inf.push(C * $scope.p1i[temp]);
          $scope.p2inf.push(C * $scope.p2i[temp]);
        }
        else {
          $scope.p1inf.push(capdelta * $scope.p1inf[temp - 1] + C * $scope.p1i[temp]);
          $scope.p2inf.push(capdelta * $scope.p2inf[temp - 1] + C * $scope.p2i[temp]);
        }

        // Update actual earnings
        var p1realearnings = 0;
        var p2realearnings = 0;
        p1realearnings = $scope.p1sales[temp] - $scope.dmg[temp] - $scope.p1i[temp];
        p2realearnings = $scope.p2sales[temp] - $scope.dmg[temp] - $scope.p2i[temp];

        if($scope.p1inf[temp] * A < $scope.dmg[temp]) {
          p1realearnings += $scope.p1inf[temp] * A;
        } else {
          p1realearnings += $scope.dmg[temp];
        }

        if($scope.p2inf[temp] * A < $scope.dmg[temp]) {
          p2realearnings += $scope.p2inf[temp] * A;
        } else {
          p2realearnings += $scope.dmg[temp];
        }

        // Update earnings
        $scope.p1earns.push({ 'timestamp': temp, 'profit': p1realearnings * profscaling });
        $scope.p2earns.push({ 'timestamp': temp, 'profit': p2realearnings * profscaling });

        // Update total earnings
        if(temp === 0) {
          $scope.p1totalearns.push(initialbalance + $scope.p1earns[temp].profit);
          $scope.p2totalearns.push(initialbalance + $scope.p2earns[temp].profit);
        } else {
          $scope.p1totalearns.push($scope.p1totalearns[temp - 1] + $scope.p1earns[temp].profit);
          $scope.p2totalearns.push($scope.p2totalearns[temp - 1] + $scope.p2earns[temp].profit);
        }
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
    y.domain([-3, 3]);

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
      genResults();

      data1 = $scope.p1earns;
      data2 = $scope.p2earns;
      mins = [d3.min(data1, function(d) { return d.profit; }), d3.min(data2, function(d) { return d.profit; })];
      maxs = [d3.max(data1, function(d) { return d.profit; }), d3.max(data2, function(d) { return d.profit; })];

      x.domain([0, timestamps - 1]);
      y.domain([-3, 3]);

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

    $scope.waitingroom = function() {
      $location.path('waiting');
    };

    $scope.incrementValue = function(array, index) {
      if(array === 'p1x' || array === 'p2x') {
        if($scope[array][index] !== 10) {
          $scope[array][index]++;
        }
      }

      var temp = $scope[array][index] + 1;

      if(array === 'p1i') {
        if(temp <= $scope.p1sales[index]) {
          $scope[array][index]++;
          $scope[array][index] = Math.round($scope[array][index]);
        } else {
          $scope[array][index] = $scope.p1sales[index];
        }
      }

      if(array === 'p2i') {
        if(temp <= $scope.p2sales[index]) {
          $scope[array][index]++;
          $scope[array][index] = Math.round($scope[array][index]);
        } else {
          $scope[array][index] = $scope.p2sales[index];
        }
      }
      $scope.updateData();
    };

    $scope.decrementValue = function(array, index) {
      if(array === 'p1x' || array === 'p2x') {
        if($scope[array][index] !== 0) {
          $scope[array][index]--;
          $scope.updateData();

          if(array === 'p1x') {
            if($scope['p1i'][index] > $scope.p1sales[index]) {
              $scope['p1i'][index] = $scope.p1sales[index];
            }
          }

          if(array === 'p2x') {
            if($scope['p2i'][index] > $scope.p2sales[index]) {
              $scope['p2i'][index] = $scope.p2sales[index];
            }
          }
        }
      }

      var temp = $scope[array][index] - 1;
      if(array === 'p1i' || array === 'p2i') {
        if($scope[array][index] >= 1) {
          $scope[array][index]--;
          $scope[array][index] = Math.round($scope[array][index]);
          if($scope[array][index] > 0 && $scope[array][index] < 0.1) {
            $scope[array][index] = 0;
          }
        } else {
          $scope[array][index] = 0;
        }
      }

      $scope.updateData();
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
      if(UserProps.isPlayer2()) {
        waiting = true;
      }
      $scope.$apply();
    });

    socket.on('endGame', function(data) {
      console.log('END THE GAME!');
      console.log(data);
      $scope.results = data.results;
      $scope.game = data;
      $scope.gameover = true;
      $scope.$apply();
      genResults();
      $scope.updateData();
      $scope.$apply();
    });

    socket.on('player2move', function() {
      if(UserProps.isPlayer2()) {
        waiting = false;
      }
    });

    socket.on('reconnectGame', function(data) {
      console.log('RECONNECTING TO GAME!');
      console.log(data);
      UserProps.setCurGame(data.player.curgame);
      UserProps.setSubjId(data.player.subj_id);
      UserProps.addGameID(data.player.game1id);
      if(data.player.game2id !== '') UserProps.addGameID(data.player.game2id);
      if(data.player.game3id !== '') UserProps.addGameID(data.player.game3id);
      if(data.player.game4id !== '') UserProps.addGameID(data.player.game4id);
      $scope.turn = data.game.turn;
      $scope.results = data.game.results;
      $scope.game = data.game;
      $scope.gameover = data.game.gameover;
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

app.controller('RecController', ['$scope', '$location' ,
  function($scope, $location) {
    $scope.subj_id = '';
    $scope.reconnectGame = function() {
      console.log('Checking name!');
      socket.emit('checknameRec', { subj_id: $scope.subj_id });
    };

    socket.on('safeToGraphReconnect', function(data) {
      $location.path('graph');
      $scope.$apply();
    });

    socket.on('safeToWaitingReconnect', function() {
      console.log('Going to waiting...');
      $location.path('waiting');
      $scope.$apply();
    });
  }
]);
