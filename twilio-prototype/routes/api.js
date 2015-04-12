var router = require("express").Router();
var twilio = require("twilio");
var auth = require("../config/auth");
var twilioclient = new twilio.RestClient(auth.sid, auth.token);
var Message = require("../models/Message");
var User = require("../models/User");

// =============================================================================
// GET
// =============================================================================
// Retrieve all messages from the database
router.get("/m", function(req, res, next) {
  Message.find(function(err, messages) {
    if (err) next(err);
    res.json(messages);
  });
});

// Retreieve the message by the specified id
router.get("/m/:id", function(req, res, next) {
  Message.findById(req.params.id, function(err, message) {
    if (err) next(err);
    res.json(message);
  });
});

router.get("/u", function(req, res, next) {
  User.find(function(err, users) {
    if (err) next(err);
    res.json(users);
  });
});

router.get("/u/:id", function(req, res, next) {
  User.findById(req.params.id, function(err, user) {
    if (err) next(err);
    res.json(user);
  });
});

router.get("/u/:id/m", function(req, res, next) {
  User.findById(req.params.id, function(err, user) {
    if(err) next(err);

    Message.find({sender: user.number}, function(err, messages) {
      if (err) next(err);
      res.json(messages);
    });
  });
});

// =============================================================================
// POST
// =============================================================================
// Receive a post a request from 
router.post("/m/receive", function(req, res, next) {
  //console.log(req.body);
  // client.messages.list(function(err, data) {
  //   data.messages.forEach(function(message) {
  //     console.log(message.body);
  //   });
  // });
  // Receive the twilio message and tell the user, thank you
  twilioclient.sendMessage({
    to: req.body.From,
    from: auth.number,
    body: "Thank you for submitting your value!"
  }, function(err, text) {
    if(!err) {
      console.log("To: " + req.body.From);
      console.log('You sent: '+ text.body);
    } else {
      console.log(err);
    }
  });

  // Make a json object in the schema of our mongodb
  amessage = {
    sender: req.body.From,
    body: req.body.Body,
    sid: req.body.sid
  };

  User.find({ number: amessage.sender }, function(err, user) {
    if (err) next(err);
    if (user.length === 0) {
      User.create({number: req.body.From}, function(err2, user) {
        if (err2) next(err2);
      });
    }
  });

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

  User.find({ number: amessage.sender }, function(err, user) {
    if (err) next(err);
    if (user.length === 0) {
      User.create({number: req.body.From}, function(err2, user) {
        if (err2) next(err2);
      });
    }
  });

  Message.create(amessage, function(err, message) {
    if (err) next(err);
    res.json(message);
  });
});

router.post("/u", function(req, res, next) {
  auser = {
    number: req.body.number
  };

  User.create(auser, function(err, user) {
    if (err) next(err);
    res.json(user);
  });
});

// =============================================================================
// DELETE
// =============================================================================
router.delete("/m/:id", function(req, res, next) {
  Message.findByIdAndRemove(req.params.id, req.body, function(err, message) {
    if(err) next(err);
    res.json(message);
  });
});

router.delete("/u/:id", function(req, res, next) {
  User.findByIdAndRemove(req.params.id, req.body, function(err, user) {
    if(err) next(err);
    res.json(user);
  });
});

module.exports = router;
