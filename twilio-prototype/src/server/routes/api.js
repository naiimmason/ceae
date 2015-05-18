var router = require('express').Router();
var twilio = require('twilio');
var auth = require('../config/auth').twilioAuth;
var twilioclient = new twilio.RestClient(auth.sid, auth.token);
var Message = require('../models/Message');
var User = require('../models/User');
var ReportPeriod = require('../models/ReportPeriod');
var admins = require('../config/admins');
var schedule = require('node-schedule');

// CONSTANTS
var submitAmount = 100;

// =============================================================================
// GET
// =============================================================================

// ______________________________messages_____________________________

// Retrieve all messages from the database
router.get('/m', loggedIn, isAdmin, function(req, res, next) {
  Message.find(function(err, messages) {
    if (err) next(err);
    res.json(messages);
  });
});

// Retreieve the message by the specified id
router.get('/m/id/:id', loggedIn, isAdmin, function(req, res, next) {
  Message.findById(req.params.id, function(err, message) {
    if (err) next(err);
    res.json(message);
  });
});

// ______________________________users______________________________

// retrieve a list of all users
router.get('/u', loggedIn, isAdmin, function(req, res, next) {
  User.find(function(err, users) {
    if (err) next(err);
    res.json(users);
  });
});

// retrieve just the specific user based on id
router.get('/u/id/:id', loggedIn, isAdmin, function(req, res, next) {
  User.findById(req.params.id, function(err, user) {
    if (err) next(err);
    res.json(user);
  });
});

// find all messages sent by a user with a specific id
router.get('/u/id/:id/m', loggedIn, isAdmin, function(req, res, next) {
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
router.get('/p', loggedIn, isAdmin, function(req, res, next) {
  ReportPeriod.find(function(err, periods) {
    if (err) next(err);
    res.json(periods);
  });
});


// return a reporting period based on its id
router.get('/p/id/:id', loggedIn, isAdmin, function(req, res, next) {
  ReportPeriod.findById(req.params.id, function(err, period) {
    if (err) next(err);
    res.json(period);
  });
});

// return a reporting periods messages
router.get('/p/id/:id/m', loggedIn, isAdmin, function(req, res, next) {
  ReportPeriod.findById(req.params.id, function(err, period) {
    if (err) next(err);

    Message.find({ '_id': { $in: period.messageids }}, function(err, messages) {
      res.json(messages);
    });
  });
});

// return a reporting periods submitted users
router.get('/p/id/:id/u', loggedIn, isAdmin, function(req, res, next) {
  ReportPeriod.findById(req.params.id, function(err, period) {
    if (err) next(err);

    User.find({ '_id': { $in: period.submittedUsers }}, function(err, users) {
      res.json(users);
    });
  });
});

// ______________________________misc.______________________________
// Check to see if the user is an admin or not
router.get('/u/me', loggedIn, isAdmin, function(req, res, next) {
  req.user.admin = true;
  res.json(req.user);
});

// =============================================================================
// POST
// =============================================================================

// _____________________________messags______________________________

// Receive a post a request from
router.post('/m/receive', function(req, res, next) {
  //  console.log(req);
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
    sid: req.body.sid,
  };

  // Create the message object and store it in our database
  Message.create(amessage, function(err, message) {
    if (err) next(err);
    amessage = message;
  });

  now = Date.now();

  User.findOne({ number: amessage.sender }, function(err, user) {
    if (err) next(err);
    if (user === null) {
      sendMessage(null, 'You are not part of our database! Contact a program ' +
                  'administrator for further details.', amessage.sender);
    } else {
      amessage.farmerid = user.farmerid;
      amessage.save();

      // Check to see which command they sent.
      // HELP COMMAND
      if(amessage.body.toUpperCase() === 'HELP') {
        sendMessage(null, 'Please call XXX-XXX-XXXX with your question and we will be sure' +
          ' to get back to you within 24 hours. You can also email GAwaterreporting@h2opolicycenter.org with' +
          ' any questions.', amessage.sender);
      }
      // BALANCE COMMAND
      else if(amessage.body.toUpperCase() === 'BALANCE') {
        sendMessage(null, 'Dear ' + user.salutation + ' ' + user.lastname + ', '  +
          'your current account balance is $'  + user.bank, amessage.sender);
      }
      // Check to see if it is a reporting period or not.
      else {
        // Iterate through all reporting periods checking against the current
        // date
        ReportPeriod.find(function(err, periods) {
          if (err) next(err);

          reporting = false;
          for(var i = 0, len = periods.length; i < len; i++) {
            // If there is a reporting period tell them, update stuff as well
            if(periods[i].startDate < now && periods[i].endDate > now) {
              var messagestart = 'Thank you for your report, ' + user.salutation +
                ' ' + user.lastname + '!';


              // Iterate through all of the user's submitted periods to check to see
              // if they ahve submitted already for this period
              // TODO: FIX
              console.log('PERIOD ID ' + periods[i]._id);
              var submitted = false;
              for(var j = 0, lenj = user.submittedPeriods.length; j < lenj; j++) {
                if(periods[i]._id == user.submittedPeriods[j]) {
                  submitted = true;
                  sendMessage(err, messagestart + ' Both this value and your previous '  +
                    'value(s) were recorded. We will use the most recent one.', amessage.sender);
                }
              }

              console.log(submitted);

              if(!submitted) {
                // If they haven't submitted then update their shit
                var tosend = messagestart;
                // Depending on user contract type send different messages
                if(user.contractType === 'A') {
                  tosend += ' $' + submitAmount + ' hass been add to your VISA card ' +
                    'for a total of $' + (user.bank + submitAmount) + ' this year.';
                }
                else if (user.contractType === 'B') {
                  tosend += ' $' + submitAmount + ' has remained on your VISA ' +
                    'card for a total remaining of $' + (user.bank + submitAmount) + ' this year.';
                }
                else {
                  tosend += 'Your value of \'' + amessage.body + '\' has been stored.';
                }
                sendMessage(null, tosend, amessage.sender);

                // Update the period and user objects then save them
                periods[i].messageids.push(amessage._id);
                periods[i].submittedUsers.push(user._id);
                periods[i].save();
                reporting = true;

                user.bank = user.bank + submitAmount;
                user.submittedPeriods.push(periods[i]._id);
                user.save();
              }
            }
          }

          if(!reporting){
            sendMessage(null, 'Reporting is not available right now.', amessage.sender);
          }
        });
      }
    }
  });

  res.json(amessage);
});

// Broadcast a uniform message to every participent
router.post('/m/broadcast', loggedIn, isAdmin, function(req, res, next){
  User.find(function(err, users) {
    if (err) next(err);
    for(var i = 0; i < users.length; i++) {
      sendMessage(err, req.body.message, users[i].number);
    }
    res.json(users);
  });
});


// ______________________________users______________________________
router.post('/u', function(req, res, next) {
  //console.log(req.body);
  User.create(req.body, function(err, user) {
    if (err) next(err);
    res.json(req.body);

    sendMessage(err, 'Dear ' + req.body.salutation + ' ' + req.body.lastname +
     ', \nYou have been registered for the CBEAR water reporting program. Text HELP ' +
     'to receive help or if you have any questions. You may also text BALANCE to ' +
     'this number to view your current account balance.', req.body.number);
  });
});

// ______________________________reporting period______________________________
// Store the reporting periods
router.post('/p', loggedIn, isAdmin, function(req, res, next) {
  ReportPeriod.create(req.body, function(err, period) {
    if (err) next(err);
    // Create schduled jobs to send messages to everyone at certain points

    // If the period has already started send out a message to all users saying
    // that the period has started
    var alreadyStart = false;
    if(period.startDate < Date.now() && period.endDate > Date.now()) {
      alreadyStart = true;
    }
    alreadyStart = false;

    // Calculate the evening before and the day before ending and print out to
    // console just to be sure
    var eveningBefore = new Date(period.startDate.toISOString());
    eveningBefore.setDate(period.startDate.getDate() - 1);
    eveningBefore.setHours(17);
    console.log(eveningBefore.toString());

    var eveningEnding = new Date(period.endDate.toISOString());
    eveningEnding.setDate(period.endDate.getDate() -1);
    console.log(eveningEnding.toString());

    // Create job to run on evening before to remind people that a reporting
    // period is coming up
    var eveningReminder = schedule.scheduleJob(eveningBefore, function() {
      User.find(function(err, users) {
        if(err) next(err);

        for(var i = 0, len = users.length; i < len; i++) {
          tosend = '';
          if(alreadyStart) {
            tosend += 'Dear ' + users[i].salutation + ' ' + users[i].lastname +
              ', a new reporting period has started between ' + period.startDate.toDateString() +
              ' and ' + period.endDate.toDateString() + '. ';
          } else {
            tosend += 'Dear ' + users[i].salutation + ' ' + users[i].lastname +
              ', a new reporting period begins between ' + period.startDate.toDateString() +
              ' and ' + period.endDate.toDateString() + '. ';
          }

          if(users[i].contractType === 'A') {
            tosend += 'If you text your meter reading in the next three days ' +
              'you will receive $' + submitAmount + ' on your VISA card.';
          } else if(users[i].contractType === 'B'){
            tosend += 'If you text your meter reading in the next three days ' +
              'you will keep $' + submitAmount + ' on your VISA card.';
          }
          sendMessage(err, tosend, users[i].number);
        }
      });
    });

    //Message.find({ '_id': { $in: period.messageids }}, function(err, messages) {
    // Create job to run with 24 hours left in reporting period
    var endingReminder = schedule.scheduleJob(eveningEnding, function() {
      ReportPeriod.findById(period._id, function(err, theperiod) {
        if (err) next(err);
        User.find({ '_id': { $nin: theperiod.submittedUsers }}, function(err, users) {
          if (err) next(err);
          console.log('ENDING REMINDER');
          console.log(users);

          for(var i = 0, len = users.length; i < len; i++) {
            tosend = 'Dear ' + users[i].salutation + ' ' + users[i].lastname +
              ', only 24 hours are left to text your meter reading and ';

            if(users[i].contractType === 'A') {
              tosend += 'receive $' + submitAmount + ' on your VISA card.';
            } else if(users[i].contractType === 'B') {
              tosend += 'keep $' + submitAmount + ' on your VISA card.';
            }

            sendMessage(err, tosend, users[i].number);
          }
        });
      });
    });//.bind(null, period._id);

    // Create a job to run at the end of the period to tell people who have
    // failed to submit that they have failed.
    var failedReminder = schedule.scheduleJob(period.endDate, function() {
      ReportPeriod.findById(period._id, function(err, theperiod) {
        if (err) next(err);

        User.find({ '_id': { $nin: theperiod.submittedUsers }}, function(err, users) {
          if (err) next(err);

          for(var i = 0, len = users.length; i < len; i++) {
            tosend = 'Dear ' + users[i].salutation + ' ' + users[i].lastname +
              ', the reporting window from ' + theperiod.startDate.toDateString() + ' to ' +
              theperiod.endDate.toDateString() + ' has closed. Unfortunately we did not ' +
              'receive a report from you and thus cannot reward you. We hope that you ' +
              'will be able to submit a report next month. Please text \'HELP\' ' +
              'if you wish to speak to us via phone, or call directly at XXX-XXX-XXXX ' +
              'or email us at GAwaterreporting@h2opolicycenter.org';
            sendMessage(err, tosend, users[i].number);

            theperiod.missedUsers.push(users[i]._id);
            users[i].missedPeriods.push(theperiod._id);
            users[i].save();
          }

          theperiod.save();
        });
      });
    });

    res.json(period);
  });
});

// Just a test of schedule to make sure it works alright
var date = new Date(2015, 4, 18, 0, 56, 0);
console.log(date);
var now = new Date(Date.now());
console.log(now);

var j = schedule.scheduleJob(date, function() {
  console.log('HERE IT IS');
});

// =============================================================================
// PUT
// =============================================================================
router.put('/u', loggedIn, isAdmin, function(req, res, next) {
  console.log(req.body);
  User.findById(req.body._id, function(err, user) {
    if(err) next(err);
    user.firstname = req.body.firstname;
    user.lastname = req.body.lastname;
    user.salutation = req.body.salutation;
    user.bank = req.body.bank;
    user.contractType = req.body.contractType;
    user.farmerid = req.body.farmerid;
    user.updated = Date.now();
    user.save();
    res.json(user);
  });
});

// =============================================================================
// DELETE
// =============================================================================

// ______________________________messages______________________________
router.delete('/m/id/:id', loggedIn, isAdmin, function(req, res, next) {
  Message.findByIdAndRemove(req.params.id, req.body, function(err, message) {
    if(err) next(err);
    res.json(message);
  });
});

// ______________________________users______________________________
router.delete('/u/id/:id', loggedIn, isAdmin, function(req, res, next) {
  User.findByIdAndRemove(req.params.id, req.body, function(err, user) {
    if(err) next(err);
    res.json(user);
  });
});

// ______________________________reporting period______________________________
router.delete('/p/id/:id', loggedIn, isAdmin, function(req, res, next) {
  ReportPeriod.findByIdAndRemove(req.params.id, req.body, function(err, period) {
    if (err) next(err);
    res.json(period);
  });
});

// Check to see if a user is logged in, if not, redirect them
function loggedIn(req, res, next) {
  if (req.isAuthenticated()) {
    next();
  } else {
    console.log('not logged in');
    res.redirect('/');
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
    res.redirect('/');
  }
}

// Send a message to the specified number with that specific message, basically
// a wrapper for the twilioclient
function sendMessage(err, text, number) {
  textmessage = {
    to: number,
    from: auth.number,
    body: text
  };
  twilioclient.sendMessage(textmessage, messageSent(err, textmessage, number));
}

// Calls when you send a message
function messageSent(err, text, number) {
  if (!err) {
    console.log('To: ' + number);
    console.log('You Sent: ' + text.body);
  } else {
    console.log(err);
  }
}

// Method for checking access level
module.exports = router;
