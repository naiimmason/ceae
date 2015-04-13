// =============================================================================
// MODULES
// =============================================================================

var twilio         = require("twilio");
    express        = require("express");
    app            = express();
    http           = require("http");
    util           = require("util");
    morgan         = require("morgan");
    bodyParser     = require("body-parser");
    cookieParser   = require("cookie-parser");
    methodOverride = require("method-override");
    mongoose       = require("mongoose");

// =============================================================================
// CONFIGURATION
// =============================================================================
var auth = require("./config/auth");

// configure Express and express middlewear
app.use(express.static(__dirname + '/client'));
app.set('views', __dirname + '/client/html');
app.use(morgan("combined"));
app.use(cookieParser());
app.use(bodyParser.urlencoded({ extended: false}));
app.use(methodOverride());

// =============================================================================
// DATABASE
// =============================================================================
var dbConfig = require("./config/db");
mongoose.connect(dbConfig.url);

// =============================================================================
// ROUTES
// =============================================================================
var api = require("./routes/api");
var routes = require("./routes/routes");
app.use("/api", api);
app.use("/", routes);

// The last middle wear to use is the 404 middlewear. If they didn't get
// anywhere show them the 404
app.use(function(req, res){
  res.sendStatus(404);
});

// =============================================================================
// START SERVER
// =============================================================================
var server = http.createServer(app);

// Start the server (taken from Andy which is taken from Cloud9)
server.listen(process.env.PORT || 3100, process.env.IP || "0.0.0.0", function() {
  var address = server.address();
  console.log("Server is now started on ", address.address + ":" + address.port);
});
