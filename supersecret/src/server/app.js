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
var NUMROUNDS = 6;


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
  this.subj_finished_rnd = 0;
  this.numrounds = NUMROUNDS;
  this.partnum = 1;
};

Experiment.prototype.dividePlayers = function() {
  split = {
    player1s: [],
    player2s: []
  };

  if(this.partnum === 1) {
    for(var i = 0, len = this.subjects.ids.length/2; i < len; i++) {
      do {
        randid = Math.floor(Math.random() * this.subjects.ids.length);
      } while(randid === i &&
        this.subjects[this.subjects.ids[i]].hasPlayed(this.subjects[this.subjects.ids[randid]].subj_id, this.partnum) &&
        this.subjects[this.subjects.ids[randid]].hasPlayed(this.subjects[this.subjects.ids[i]].subj_id, this.partnum));

      this.subjects[this.subjects.ids[i]]['playedpart' + this.partnum].push(this.subjects.ids[randid]);
      this.subjects[this.subjects.ids[randid]]['playedpart' + this.partnum].push(this.subjects.ids[i]);

      split.player1s.push(this.subjects.ids[i]);
      split.player2s.push(this.subjects.ids[randid]);
    }
  } else {
    for(var i = 0, len = this.subjects.ids.length/2; i < len; i++) {
      do {
        randid = Math.floor(Math.random() * this.subjects.ids.length);
      } while(randid != i && this.subjects.ids[i]);
    }
  }

  return split;
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
  this.gameover = false;
};

Game.prototype.addPlayer = function(player) {
  console.log('ADDING PLAYER');
  console.log(player);
  //console.log(this);
  // Add the player to the correct role in the game
  if(this.p1id === -1) {
    this.p1id = player.subj_id;
  }
  else if (this.p2id === -1) {
    this.p2id = player.subj_id;
    exp.subjects[this.p1id]['playedpart' + exp.partnum].push(this.p2id);
    exp.subjects[this.p2id]['playedpart' + exp.partnum].push(this.p1id);
  }
  else {
    return false;
  }

  return true;
};

Game.prototype.submitchoices = function(player, choices) {
  if(this.p1id === player.subj_id && !this.p1submitted) {
    this.p1submitted = true;
    this.p1choices.push(choices);
  }
  else if(this.p2id === player.subj_id && !this.p2submitted) {
    this.p2submitted = true;
    this.p2choices.push(choices);
  }
  else {
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
  var timestamps = 6.00;
  var initialbalance = 25.00;

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
    p2earn: null,
    p1totalearn: null,
    p2totalearn: null,
    turn: this.turn
  };

  // Update sales
  result.p1sales = p1xinp * R;
  result.p2sales = p2xinp * R;

  // Update damage
  if(this.turn === 1) {
    result.dmg = D0 * D1 + D2 * (p1xinp + p2xinp);
  }
  else {
    result.dmg = this.results[this.turn - 2].dmg * D1 + D2 * (p1xinp + p2xinp);
  }

  // Update infrastructure
  if(this.turn === 1) {
    result.p1inf = C * p1iinp;
    result.p2inf = C * p2iinp;
  } else {
    result.p1inf = capdelta * this.results[this.turn - 2].p1inf + C * p1iinp;
    result.p2inf = capdelta * this.results[this.turn - 2].p2inf + C * p2iinp;
  }

  // Update actual earnings
  var p1realearnings = result.p1sales - result.dmg - p1iinp;
  var p2realearnings = result.p2sales - result.dmg- p2iinp;


  if(result.p1inf * A < result.dmg) {
    p1realearnings += result.p2inf * A;
  } else {
    p1realearnings += result.dmg;
  }

  if(result.p2inf * A < result.dmg) {
    p2realearnings += result.p2inf * A;
  } else {
    p2realearnings += result.dmg;
  }

  // Update earnings
  result.p1earn = { 'timestamp': this.turn - 1, 'profit': p1realearnings * profscaling };
  result.p2earn = { 'timestamp': this.turn - 1, 'profit': p2realearnings * profscaling };


  if(this.turn === 1) {
    result.p1totalearn = initialbalance + result.p1earn.profit;
    result.p2totalearn = initialbalance + result.p2earn.profit;
  } else {
    result.p1totalearn = this.results[this.turn - 2].p1totalearn + result.p1earn.profit;
    result.p2totalearn = this.results[this.turn - 2].p2totalearn + result.p2earn.profit;
  }

  this.results.push(result);

  this.turn++;
  this.p1submitted = false;
  this.p2submitted = false;
};

// Subject class containing everything about the subject
var Subject = function(id) {
  this.subj_id = id;
  this.isplayer1 = false;
  this.isplayer2 = false;
  this.curgame = 0;
  this.playedpart1 = [];
  this.playedpart2 = [];
  this.game1id = '';
  this.game2id = '';
  this.game3id = '';
  this.game4id = '';
};

Subject.prototype.hasPlayed = function(playerid, part) {
  console.log('Checking has played ' + playerid + ' and part ' + part);
  for(var i = 0, len = this['playedpart' + part].length; i < len; i++) {
    if(this['playedpart' + part][i] === playerid) {
      return true;
    }
  }

  return false;
};
// create the main experiment object
var exp = new Experiment();
//console.log(exp.dividePlayers());

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

    console.log(exp.dividePlayers());

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

    // Tell clients to start the game
    io.sockets.in('waiting').emit('startGame', gamesinfo);
  });

  // Join the game, create a game if it does not already exist for that number
  socket.on('joinGame', function(data) {
    console.log('JOINING GAME:');
    console.log(data);
    gametojoin = data.gameids[data.curgame - 1];
    if (!exp.games[gametojoin]) {
      exp.games[gametojoin] = new Game(0, gametojoin);
    }

    socket.leave('waiting');
    socket.join(gametojoin);

    // Add the player to the game respectively
    var res = exp.games[gametojoin].addPlayer(exp.subjects[data.subj_id]);
    if(!res) {
      console.log('ERR: That game is full');
    } else {
      console.log('Player has successfully joined the game!');
    }
  });

  // When a person submits a move add the choices to the game object and then
  // go to the next turn
  socket.on('submitMove', function(data) {
    console.log('SUBMITTED MOVE:');
    console.log(data);
    exp.games[data.gameid].submitchoices(exp.subjects[data.subj_id], { x: data.output, i: data.investment });

    // If the game has ended send an end packet otherwise just wait for the next
    // turn upon sending the data to the client
    if(exp.games[data.gameid].submitted()) {
      exp.games[data.gameid].nextTurn();
      if (exp.games[data.gameid].turn === exp.numrounds + 1) {
        console.log(data.gameid + ': END GAME!!!!!');
        exp.games[data.gameid].gameover = true;
        io.sockets.in(data.gameid).emit('endGame', exp.games[data.gameid]);
      } else {
        console.log(data.gameid + ': Continue to turn ' + exp.games[data.gameid].turn);
        io.sockets.in(data.gameid).emit('nextTurn', exp.games[data.gameid]);
      }
    }

    if(exp.games[data.gameid].turn === exp.numrounds + 1 && exp.games[data.gameid].submitted()) {
      socket.leave(data.gameid);
      socket.join('waiting');
      exp.subj_finished_rnd++;

      // Divide players again
      if(exp.subj_finished_rnd === exp.num_subj) {
        //split = exp.dividePlayers();
        //console.log(split);
      }
    }
  });

  socket.on('checknameRec', function(data) {
    console.log('Name check!');
    if(exp.subjects[data.subj_id]) {
      console.log('It exists!');
      if(exp.subjects[data.subj_id].game1id !== '') {
        console.log('Game already created!');
        socket.emit('safeToGraphReconnect');
        setTimeout(function() { socket.emit('reconnectGame', {
          game: exp.games[exp.subjects[data.subj_id]['game' + exp.subjects[data.subj_id].curgame +'id']],
          player: exp.subjects[data.subj_id] }); }, 1000);
      } else {
        console.log('Game not created!');
        socket.emit('safeToWaitingReconnect');
      }
    } else {
      console.log('It doesn\'t exist!');
    }
  });
});

// =============================================================================
// EXPORT SERVER
// =============================================================================
module.exports = server;
