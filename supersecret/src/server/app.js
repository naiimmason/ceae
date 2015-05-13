// =============================================================================
// This is the main server file that starts up the NodeJS application using
// express and all other required modules to get the server off of the ground.
// Any configuration or deep level changes (think authentication methods) are
// made here and will be changed in this file if need be.
// =============================================================================

// =============================================================================
// MODULES
// =============================================================================

// Import required NodeJS modules
var express        = require('express');
    app            = express();
    http           = require('http');
    util           = require('util');
    morgan         = require('morgan');
    session        = require('express-session');
    bodyParser     = require('body-parser');
    cookieParser   = require('cookie-parser');
    methodOverride = require('method-override');
    path           = require('path');
    socketio       = require('socket.io');

// =============================================================================
// CONFIGURATIONS
// =============================================================================
var authConfig = require('./config/auth');

// configure Express and express middlewear
app.use(express.static(path.resolve('src/public')));
app.set('views', path.resolve('src/public/html'));
//app.use(morgan('dev'));
app.use(cookieParser());
app.use(bodyParser.json());
app.use(methodOverride());
app.use(session({
  secret: authConfig.sessionSecret,
  resave: false,
  saveUninitialized: true
}));

// =============================================================================
// ROUTES
// =============================================================================
var routes = require('./routes/routes');

app.use('/', routes);

// The last middle wear to use is the 404 middlewear. If they didn't get
// anywhere show them the 404
app.use(function(req, res){
    res.sendStatus(404);
});

// =============================================================================
// START SERVER
// =============================================================================
var server = http.createServer(app);


// =============================================================================
// GAME LOGIC AND IO
// =============================================================================
var NUMROUNDS = 10;


// Experiment class that holds everything
var Experiment = function() {
  this.games = {
    ids: []
  };
  this.subjects = {
    ids: []
  };
  this.gamenum = 0;
  this.num_subj = 0;
  this.numrounds = NUMROUNDS;
};

// ENUM for the two types of games
var GameType = {
  'SIMULTANEOUS' : 0,
  'SEQUENTIAL': 1
};

// Game class that stores all relavent information
var Game = function(gametype, gameid) {
  this.turn = 1;
  this.p1id = -1;
  this.p2id = -1;
  this.type = gametype;
  this.p1choices = [];
  this.p2choices = [];
  this.results = [];
  this.p1submitted = false;
  this.p2submitted = false;
  this.gameid = gameid;
};

Game.prototype.addPlayer = function(player) {
  console.log('ADDING PLAYER');
  console.log(player);
  //console.log(this);
  // Add the player to the correct role in the game
  if(this.p1id === -1) {
    this.p1id = player.subj_id;
  } else if (this.p2id === -1) {
    this.p2id = player.subj_id;
  } else {
    return false;
  }

  return true;
};

Game.prototype.submitchoices = function(player, choices) {
  if(this.p1id === player.subj_id && !this.p1submitted) {
    this.p1submitted = true;
    this.p1choices.push(choices);
  } else if(this.p2id === player.subj_id && !this.p2submitted) {
    this.p2submitted = true;
    this.p2choices.push(choices);
  } else {
    console.log('ERR submitting choices');
    return false;
  }

  console.log(this);
  return true;
};

Game.prototype.submitted = function() {
  return this.p1submitted && this.p2submitted;
};


Game.prototype.nextTurn = function() {
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
  console.log('CHOICES:');
  console.log(this.p1choices);
  console.log(this.p2choices);
  var p1xinp = this.p1choices[this.turn - 1].x;
  var p1iinp = this.p1choices[this.turn - 1].i;
  var p2xinp = this.p2choices[this.turn - 1].x;
  var p2iinp = this.p2choices[this.turn - 1].i;

  var result = {
    p1sales: null,
    p2sales: null,
    dmg: null,
    p1inf: null,
    p2inf: null,
    p1earn: null,
    p2earn: null
  };

  // Update sales
  result.p1sales = p1xinp * R;
  result.p2sales = p2xinp * R;

  // Update damage
  if(this.turn === 1) {
    result.dmg = D0 * D1 + D2 * p1xinp + D2 * p2xinp;
  }
  else {
    result.dmg = this.results[this.turn - 2].dmg * D1 + D2 * (p1xinp + p2xinp);
  }

  // Update infrastructure
  if(this.turn === 1) {
    if(C * p1iinp < result.dmg) {
      result.p1inf = C * p1iinp;
    }
    else {
      result.p1inf = result.dmg;
    }

    if(C * p2iinp < result.dmg) {
      result.p2inf = C * p1iinp;
    }
    else {
      result.p2inf = result.dmg;
    }
  }
  else {
    if((capdelta * this.p1choices[this.turn - 2].i + C * p1iinp) < result.dmg) {
      result.p1inf = (capdelta * this.p1choices[this.turn - 2].i + C * p1iinp);
    } else {
      result.p1inf = result.dmg;
    }

    if((capdelta * this.p2choices[this.turn - 2].i + C * p2iinp) < result.dmg) {
      result.p2inf = (capdelta * this.p2choices[this.turn - 2].i + C * p2iinp);
    } else {
      result.p2inf = result.dmg;
    }
  }

  // Update earnings
  result.p1earn = { 'timestamp': this.turn - 1, 'profit': result.p1sales - result.dmg - p1iinp + result.p1inf * A };
  result.p2earn = { 'timestamp': this.turn - 1, 'profit': result.p2sales - result.dmg - p2iinp + result.p2inf * A };
  this.results.push(result);

  this.turn++;
  this.p1submitted = false;
  this.p2submitted = false;
};

// Subject class containing everything about the subject
var Subject = function(id) {
  this.subj_id = id;
  this.curgame = 0;
  this.game1id = '';
  this.game2id = '';
  this.game3id = '';
  this.game4id = '';
};

// create the main experiment object
var exp = new Experiment();

// This communicates between the server and the client
var io = socketio.listen(server);

io.sockets.on('connection', function(socket) {
  console.log('New connection from: ' + socket.request.connection.remoteAddress);

  // Try to have one socket per one event and try not to go too many sockets
  // deep, EG: No emit inside an emit inside an emit
  socket.on('usernameCheck', function(data) {
    if(exp.subjects[data]) {
      socket.emit('takenUsername');
    }
    else {
      // Add player as a hash and increment number of players
      exp.subjects[data] = new Subject(data);
      exp.num_subj += 1;
      exp.subjects.ids.push(data);

      // Just print out everything in case something bad happens
      console.log(exp.subjects[data]);
      console.log('numplayers = '+ exp.num_subj);
      console.log('playerids');
      console.log(exp.subjects.ids);

      // Join the waiting room and let the client know to advance
      socket.join('waiting');
      socket.emit('freeUsername');

      // Let admins know the number of users
      io.sockets.in('admin').emit('returnNumUsers', { numusers: exp.num_subj });
    }
  });

  // // Handle a client disconnect
  // socket.on('disconnect', function() {
  //   console.log('User disconnected: ' + socket.request.connection.remoteAddress);
  //   exp.num_subj -= 1;
  //   io.sockets.in('admin').emit('userDisconnect', { numusers: exp.num_subj });
  // });

  // Get the number of players and add the socket as an admin
  socket.on('getNumUsers', function() {
    socket.join('admin');
    socket.emit('returnNumUsers', { numusers: exp.num_subj });
  });

  // Start the game from a button given in the admin panel
  socket.on('startGame', function() {
    console.log('START THE GAME');

    // Make sure there are at least four players and an even number of players
    if(exp.subjects.ids.length % 2 === 1 || exp.subjects.ids.length < 2) {
      console.log('ERR: Not an even amt of players or not enough players');
      socket.emit('amtPlayerError');
      return;
    }

    // Print out a list of players
    var strplayers = '';
    for(var i = 0, len = exp.subjects.ids.length; i < len; i++) {
      strplayers += exp.subjects.ids[i] + ', ';
    }
    console.log('PLAYERS: ' + strplayers);

    // Construct games packet to tell each client what game they are in
    var gamesinfo = {};
    for(i = 0, len = exp.subjects.ids.length; i < len; i += 2) {
      // Get the ids of all players
      var p1id = exp.subjects.ids[i];
      var p2id = exp.subjects.ids[i + 1];

      // Update current game number and the gameid they are playing
      exp.subjects[p1id].curgame = 1;
      exp.subjects[p1id].game1id = exp.gamenum;

      exp.subjects[p2id].curgame = 1;
      exp.subjects[p2id].game1id = exp.gamenum;

      gamesinfo[p1id] = { gameid: exp.gamenum, curgame: 1 };
      gamesinfo[p2id] = { gameid: exp.gamenum, curgame: 1 };

      exp.gamenum++;
    }

    io.sockets.in('waiting').emit('startGame', gamesinfo);
  });

  socket.on('joinGame', function(data) {
    console.log('JOINING GAME:');
    console.log(data);
    gametojoin = data.gameids[data.curgame - 1];
    if (!exp.games[gametojoin]) {
      exp.games[gametojoin] = new Game(GameType.SIMULTANEOUS, gametojoin);
    }
    socket.join(gametojoin);

    var res = exp.games[gametojoin].addPlayer(exp.subjects[data.subj_id]);
    if(!res) {
      console.log('ERR: That game is full');
    } else {
      console.log('Player has successfully joined the game!');
    }
  });

  socket.on('submitMove', function(data) {
    console.log('SUBMITTED MOVE:');
    console.log(data);
    exp.games[data.gameid].submitchoices(exp.subjects[data.subj_id], { x: data.output, i: data.investment });

    if(exp.games[data.gameid].submitted()) {
      exp.games[data.gameid].nextTurn();
      console.log(data.gameid + ': Continue to turn ' + exp.games[data.gameid].turn);
      io.sockets.in(data.gameid).emit('nextTurn', exp.games[data.gameid]);
    }
  });
});

// =============================================================================
// EXPORT SERVER
// =============================================================================
module.exports = server;
