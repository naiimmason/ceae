// =============================================================================
// MODULES
// =============================================================================

var twilio         = require('twilio');
    express        = require('express');
    app            = express();
    http           = require('http');
    util           = require('util');
    morgan         = require('morgan');
    bodyParser     = require('body-parser');
    cookieParser   = require('cookie-parser');
    methodOverride = require('method-override');
    mongoose       = require('mongoose');
    passport       = require('passport');
    GoogleStrategy = require('passport-google-oauth').OAuth2Strategy;
    session        = require('express-session');
    path           = require('path');

// =============================================================================
// CONFIGURATION
// =============================================================================
var GoogleAuth = require('./config/auth').GoogleAuth;

// Allow passport to serialize and deserialize users
passport.serializeUser(function(user, done) {
  done(null, user);
});

passport.deserializeUser(function(obj, done) {
  done(null, obj);
});

// Use the facebook strategy for authentication purposes
passport.use(new GoogleStrategy({
    clientID: GoogleAuth.clientID,
    clientSecret: GoogleAuth.clientSecret,
    callbackURL: GoogleAuth.callbackURL
  },
  function(accessToken, refreshToken, profile, done) {
    console.log(profile);
    done(null, profile);
  }
));

// configure Express and express middlewear
app.use(express.static(path.resolve('./src/client')));
app.set('views', path.resolve('./src/client/html'));
app.use(morgan('combined'));
app.use(cookieParser());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(methodOverride());
app.use(session({
  secret: GoogleAuth.clientSecret,
  resave: false,
  saveUninitialized: true
}));

// Initialize Passport!  Also use passport.session() middleware, to support
// persistent login sessions
app.use(passport.initialize());
app.use(passport.session());

// =============================================================================
// DATABASE
// =============================================================================
var dbConfig = require('./config/db');
mongoose.connect(dbConfig.url);

// =============================================================================
// ROUTES
// =============================================================================
var routes = require('./routes/routes');
var api = require('./routes/api');
var auth = require('./routes/auth');

app.use('/', routes);
app.use('/api', api);
app.use('/auth', auth);

// The last middle wear to use is the 404 middlewear. If they didn't get
// anywhere show them the 404
app.use(function(req, res){
  res.sendStatus(404);
});

// =============================================================================
// START SERVER
// =============================================================================
var server = http.createServer(app);
module.exports = server;

