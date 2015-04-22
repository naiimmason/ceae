var router = require("express").Router();
var twilio = require("twilio");
var auth = require("../config/auth").twilioAuth;
var twilioclient = new twilio.RestClient(auth.sid, auth.token);
var Message = require("../models/Message");
var User = require("../models/User");
var ReportPeriod = require("../models/ReportPeriod");
var admins = require("../config/admins");

// =============================================================================
// GET
// =============================================================================

// ______________________________messages_____________________________

// Retrieve all messages from the database
router.get("/m", loggedIn, isAdmin, function(req, res, next) {
  Message.find(function(err, messages) {
    if (err) next(err);
    res.json(messages);
  });
});

// Retreieve the message by the specified id
router.get("/m/id/:id", loggedIn, isAdmin, function(req, res, next) {
  Message.findById(req.params.id, function(err, message) {
    if (err) next(err);
    res.json(message);
  });
});

// ______________________________users______________________________

// retrieve a list of all users
router.get("/u", loggedIn, isAdmin, function(req, res, next) {
  User.find(function(err, users) {
    if (err) next(err);
    res.json(users);
  });
});

// retrieve just the specific user based on id
router.get("/u/id/:id", loggedIn, isAdmin, function(req, res, next) {
  User.findById(req.params.id, function(err, user) {
    if (err) next(err);
    res.json(user);
  });
});

// find all messages sent by a user with a specific id
router.get("/u/id/:id/m", loggedIn, isAdmin, function(req, res, next) {
  User.findById(req.params.id, function(err, user) {
    if(err) next(err);

    Message.find({ sender: user.number }, function(err, messages) {
      if (err) next(err);
      res.json(messages);
    });
  });
});

// ______________________________reporting period______________________________

// return all reporting periods
router.get("/p", loggedIn, isAdmin, function(req, res, next) {
  ReportPeriod.find(function(err, periods) {
    if (err) next(err);
    res.json(periods);
  });
});


// return a reporting period based on its id
router.get("/p/id/:id", loggedIn, isAdmin, function(req, res, next) {
  ReportPeriod.findById(req.params.id, function(err, period) {
    if (err) next(err);
    res.json(period);
  });
});

// return


// ______________________________misc.______________________________
// Check to see if the user is an admin or not
router.get("/u/me", loggedIn, isAdmin, function(req, res, next) {
  req.user.admin = true;
  res.json(req.user);
});



// =============================================================================
// POST
// =============================================================================

// _____________________________messags______________________________

// Receive a post a request from
router.post("/m/receive", function(req, res, next) {
  //console.log(req);
  // client.messages.list(function(err, data) {
  //   data.messages.forEach(function(message) {
  //     console.log(message.body);
  //   });
  // });
  // Receive the twilio message and tell the user, thank you

  // Make a json object in the schema of our mongodb
  amessage = {
    sender: req.body.From,
    body: req.body.Body,
    sid: req.body.sid
  };

  partof = true;
  reporting = false;
  now = Date.now();
  period = null;

  User.findOne({ number: amessage.sender }, function(err, user) {
    if (err) next(err);
    if (user === null) {
      sendMessage(null, "You are not part of our database! Contact a program " +
                  "administrator for further details.",  amessage.sender);
      partof = false;
    }
  });

  ReportPeriod.find(function(err, periods) {
    if (err) next(err);
    for(var i = 0; i < periods.length; i++) {
      if(periods[i].startDate < now && periods[i].endDate > now) {
        reporting = true;
        period = periods[i];
      }
    }
  });

  if(reporting && partof) {
    sendMessage(null, "Thank you for reporting! Your value of \"" + amessage.body +
                "\" has been stored.", amessage.sender);
  } else if(!reporting && partof) {
    sendMessage(null, "Reporting is not available right now.", amessage.sender);
  }

  // Create the message object and store it in our database
  Message.create(amessage, function(err, message) {
    if (err) next(err);
    res.json(message);
  });
});

// A test post method that puts a new message in the database
router.post("/m", function(req, res, next) {
  amessage = {
    sender: req.body.From,
    body: req.body.Body,
    sid: req.body.sid
  };

  console.log(amessage);

  User.findOne({ number: amessage.sender }, function(err, user) {
    if (err) next(err);
    if (user === null) {
      sendMessage(null, "You are not part of our database! Contact a program " +
                  "administrator for further details.",  req.body.From);
    }
  });

  Message.create(amessage, function(err, message) {
    if (err) next(err);
    res.json(message);
  });
});

router.post("/m/broadcast", loggedIn, isAdmin, function(req, res, next){
  User.find(function(err, users) {
    if (err) next(err);
    for(var i = 0; i < users.length; i++) {
      sendMessage(err, req.body.message, users[i].number);
    }
    res.json(users);
  });
});


// ______________________________users______________________________
router.post("/u", function(req, res, next) {
  User.create(req.body, function(err, user) {
    if (err) next(err);
    res.json(req.body);

    sendMessage(err, "You have been registered for the CBEAR water reporting program.", req.body.number);
  });
});

// ______________________________reporting period______________________________

router.post("/p", loggedIn, isAdmin, function(req, res, next) {
  ReportPeriod.create(req.body, function(err, period) {
    if (err) next(err);
    res.json(period);
  });
});

// =============================================================================
// DELETE
// =============================================================================

// ______________________________messages______________________________
router.delete("/m/:id", loggedIn, isAdmin, function(req, res, next) {
  Message.findByIdAndRemove(req.params.id, req.body, function(err, message) {
    if(err) next(err);
    res.json(message);
  });
});

// ______________________________users______________________________
router.delete("/u/:id", loggedIn, isAdmin, function(req, res, next) {
  User.findByIdAndRemove(req.params.id, req.body, function(err, user) {
    if(err) next(err);
    res.json(user);
  });
});

// Check to see if a user is logged in, if not, redirect them
function loggedIn(req, res, next) {
  if (req.user) {
    next();
  } else {
    console.log("not logged in");
    res.redirect("/");
  }
}

// Check to see if they are on the admin list or not
function isAdmin(req, res, next) {
  var admin = false;

  for(var i = 0; i < admins.length; i++) {
    if (req.user.emails[0].value === admins[i]) {
      admin = true;
    }
  }

  if (admin) {
    next();
  }
  else {
    res.redirect("/");
  }
}

function sendMessage(err, text, number) {
  textmessage = {
    to: number,
    from: auth.number,
    body: text
  };
  twilioclient.sendMessage(textmessage, messageSent(err, textmessage, number));
}

function messageSent(err, text, number) {
  if (!err) {
    console.log("To: " + number);
    console.log("You Sent: " + text.body);
  } else {
    console.log(err);
  }
}

// Method for checking access level
module.exports = router;
