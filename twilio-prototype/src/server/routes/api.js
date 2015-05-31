var router = require('express').Router();
var twilio = require('twilio');
var auth = require('../config/auth').twilioAuth;
var twilioclient = new twilio.RestClient(auth.sid, auth.token);
var Message = require('../models/Message');
var User = require('../models/User');
var ReportPeriod = require('../models/ReportPeriod');
var WaterMeter = require('../models/WaterMeter');
var admins = require('../config/admins');
var schedule = require('node-schedule');
var m = require('../config/messages');
var c = require('../config/contracts');

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

// Get all of the water meters associate with a user
router.get('/u/id/:id/w', loggedIn, isAdmin, function(req, res, next) {
  User.findById(req.params.id, function(err, user) {
    if(err) next(err);

    WaterMeter.find({user: user._id}, function(err, meters) {
      if (err) next(err);
      res.json(meters);
    });
  });
});

// ______________________________reporting period______________________________
// Get a specific meter
router.get('/w/id/:id', loggedIn, isAdmin, function(req, res, next) {
  WaterMeter.findById(req.params.id, function(err, meter) {
    if (err) next(err);
    res.json(meter);
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
router.get('/p/id/:id/w', loggedIn, isAdmin, function(req, res, next) {
  ReportPeriod.findById(req.params.id, function(err, period) {
    if (err) next(err);

    WaterMeter.find({ '_id': { $in: period.submittedMeters }}, function(err, meters) {
      res.json(meters);
    });
  });
});

router.get('/p/id/:id/u', loggedIn, isAdmin, function(req, res, next) {
  ReportPeriod.findById(req.params.id, function(err, period) {
    if(err) next(err);

    Message.find({ '_id': { $in: period.messageids }}, function(err2, messages) {
      if(err2) next(err);
      res.json(messages);
    });
  });
});

// return a reporting periods submitted meters

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

    now = Date.now();

    User.findOne({ number: amessage.sender }, function(err, user) {
      if (err) next(err);
      if (user === null) {
        sendMessage(null, 'You are not part of our database! Contact a program ' +
                    'administrator for further details.', amessage.sender);
      } else {
        amessage.invitationid = user.invitationid;
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

        // METERS COMMAND
        else if(amessage.body.toUpperCase() === 'METERS') {
          WaterMeter.find({ user: user._id }, function(err, meters) {
            tosend = 'Your registered meters are: \n';
            for(var i = 0, len = meters.length; i < len; i++) {
              tosend += meters[i].serialnumber + ' \n';
            }

            sendMessage(null, tosend, amessage.sender);
          });
        }

        // Check to see if it is a reporting period or not.
        else {
          // Check message to make sure it is a valid format
          var validmsg = true;
          var snumber = '';
          var rnumber = '';

          if(amessage.body.split(',').length === 2) {
            snumber = amessage.body.split(',')[0].replace(/[^0-9]/g, '');
            rnumber = amessage.body.split(',')[1].replace(/[^0-9]/g, '');
          }

          if(amessage.body.split(',').length != 2) {
            validmsg = false;
            sendMessage(null, m.ALL.nocomma, amessage.sender);
          }

          else if(snumber.length != 7) {
            validmsg = false;
            sendMessage(null, m.ALL.serialerror.replace('%theirtext%', '"'  + amessage.body + '"'), amessage.sender);
          }

          else if(rnumber.length != 6) {
            validmsg = false;
            sendMessage(null, m.ALL.readingerror.replace('%theirtext%', '"'  + amessage.body + '"'), amessage.sender);
          }

          // Iterate through all reporting periods checking against the current
          // date
          if(validmsg) {
            ReportPeriod.find(function(err, periods) {
              if (err) next(err);

              // THIS WHOLE THING
              reporting = false;
              for(var i = 0, len = periods.length; i < len; i++) {
                console.log(periods[i]);
                // If there is a reporting period tell them, update stuff as well
                if(periods[i].startDate < now && periods[i].endDate > now) {
                  var submitted = false;
                  reporting = true;
                  var messagestart = 'Thank you for your report, ' + user.salutation +
                    ' ' + user.lastname + '!';
                  var periodid = periods[i]._id;

                  // Find the water meter they are reporting for.
                  (function (periodid) {
                    WaterMeter.findOne({ 'serialnumber': snumber }, function(err, meter) {
                      if(meter === null) {
                        sendMessage(err, m.ALL.invalidmeter, amessage.sender);
                      } else {
                        // Iterate through all of the user's submitted periods to check to see
                        // if they ahve submitted already for this period
                        // TODO: FIX
                        console.log('PERIOD ID ' + periodid);
                        for(var j = 0, lenj = meter.submittedPeriods.length; j < lenj; j++) {
                          if(meter.submittedPeriods[j].equals(periodid)) {
                            submitted = true;
                            sendMessage(err, messagestart + ' Both this value and your previous '  +
                              'value(s) were recorded. We will use the most recent one.', amessage.sender);
                          }
                        }

                        meter.submittedValues.push({ period: periodid, value: rnumber});
                        meter.save();
                        console.log(submitted);

                        if(!submitted) {
                          // If they haven't submitted then update their shit
                          var tosend = '';
                          // Depending on user contract type send different messages
                          if(user.contractType === 'A') {
                            user.bank += m.A.reportamt;
                            tosend += m.A.thankyou.replace('%accountbalance%', user.bank);
                          }
                          else if (user.contractType === 'B') {
                            user.bank += m.B.reportamt;
                            tosend += m.B.thankyou.replace('%accountbalance%', user.bank);
                          }
                          else if(user.contractType === 'C') {
                            tosend += m.C.thankyou.replace('%accountbalance%', user.bank);
                          }
                          else if(user.contractType === 'D') {
                            tosend += m.D.thankyou.replace('%accountbalance%', user.bank);
                          }
                          else {
                            tosend += 'Your value of \'' + rnumber + '\' has been stored.';
                          }

                          sendMessage(null, tosend, amessage.sender);

                          // Update the period and user objects then save them
                          ReportPeriod.findById(periodid, function(err, period) {
                            if (err) next(err);
                            period.messageids.push(amessage._id);
                            period.submittedMeters.push(meter._id);
                            period.save();
                          });
                          reporting = true;
                          user.save();
                          meter.submittedPeriods.push(periodid);
                          meter.save();
                        }
                      }
                    });
                 } (periodid));
                }
              }

              if(!reporting){
                sendMessage(null, m.ALL.noperiod, amessage.sender);
              }
            });
          }
        }
      }
    });

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

  // Check the invite id against the contract to check which contract they have
  if(c[req.body.invitationid]) {
    req.body.contractType = c[req.body.invitationid];
  } else {
    req.body.contractType = 'A';
  }

  console.log(req.body);

  // Create the user and send a message
  User.create(req.body, function(err, user) {
    if (err) next(err);
    res.json(user);

    msgbody = m.ALL.welcome.replace('%salutation%', req.body.salutation).replace('%lastname%', req.body.lastname);

    sendMessage(err, msgbody, req.body.number);
  });
});

// ______________________________water meters______________________________
// TODO: Fix crops
// TODO: Fix asynchronous bank addition
router.post('/w', function(req, res, next) {
  console.log(req.body);
  WaterMeter.create(req.body, function(err, meter) {
    if(err) next(err);
    res.json(meter);

    User.findById(req.body.user, function(err, user) {
      if(err) next(err);
      user.watermeters.push(meter._id);
      if(user.contractType === 'C' || user.contractType === 'D') {
        user.bank += 350;
      }
      user.save();
    });
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

          if(users[i].contractType === 'A') {
            tosend += m.A.opening.replace('%startdate%', period.startDate.toDateString())
              .replace('%enddate%', period.endDate.toDateString())
              .replace('%accountbalance%', users[i].bank);
          } else if(users[i].contractType === 'B'){
            tosend += m.B.opening.replace('%startdate%', period.startDate.toDateString())
              .replace('%enddate%', period.endDate.toDateString())
              .replace('%accountbalance%', users[i].bank);
          } else if(users[i].contractType === 'C') {
            tosend += m.C.opening.replace('%startdate%', period.startDate.toDateString())
              .replace('%enddate%', period.endDate.toDateString())
              .replace('%accountbalance%', users[i].bank);
          } else if(users[i].contractType === 'D') {
            tosend += m.D.opening.replace('%startdate%', period.startDate.toDateString())
              .replace('%enddate%', period.endDate.toDateString())
              .replace('%accountbalance%', users[i].bank);
          }
          sendMessage(err, tosend, users[i].number);
        }
      });
    });

    //Message.find({ '_id': { $in: period.messageids }}, function(err, messages) {
    // Create job to run with 24 hours left in reporting period
    // Change this to meters instead of users
    var endingReminder = schedule.scheduleJob(eveningEnding, function() {
      ReportPeriod.findById(period._id, function(err, theperiod) {
        if (err) next(err);
        WaterMeter.find({ '_id': { $nin: theperiod.submittedMeters }}, function(err, meters) {
          if (err) next(err);
          console.log('ENDING REMINDER');
          console.log(meters);

          var userids = [];
          for(var i = 0, len = meters.length; i < len; i++) {
            if(userids.indexOf(meters[i].user) === -1) {
              userids.push(meters[i].user);
            }
          }

          for(i = 0, len = userids.length; i < len; i++) {
            User.findOne({ '_id': userids[i] }, function(err, user) {
              tosend = '';
              if (err) next(err);

              if(user.contractType === 'A') {
                tosend += m.A.closing.replace('%startdate%', theperiod.startDate.toDateString())
                  .replace('%enddate%', theperiod.endDate.toDateString())
                  .replace('%accountbalance%', user.bank);
              }
              else if(user.contractType === 'B') {
                tosend += m.B.closing.replace('%startdate%', theperiod.startDate.toDateString())
                  .replace('%enddate%', theperiod.endDate.toDateString())
                  .replace('%accountbalance%', user.bank);
              }
              else if(user.contractType === 'C') {
                tosend += m.C.closing.replace('%startdate%', theperiod.startDate.toDateString())
                  .replace('%enddate%', theperiod.endDate.toDateString())
                  .replace('%accountbalance%', user.bank);
              }
              else if(user.contractType === 'D') {
                tosend += m.D.closing.replace('%startdate%', theperiod.startDate.toDateString)
                  .replace('%enddate%', theperiod.endDate.toDateString())
                  .replace('%accountbalance%', user.bank);
              }

              sendMessage(err, tosend, user.number);
            });
          }
        });
      });
    });//.bind(null, period._id);

    // Create a job to run at the end of the period to tell people who have
    // failed to submit that they have failed.

    // Change this to meters instead of users
    var failedReminder = schedule.scheduleJob(period.endDate, function() {
      ReportPeriod.findById(period._id, function(err, theperiod) {
        if (err) next(err);

        WaterMeter.find({ '_id': { $nin: theperiod.submittedMeters }}, function(err, meters) {
          if (err) next(err);

          var userids = [];
          var usermiss = {

          };
          for(var i = 0, len = meters.length; i < len; i++) {
            if(userids.indexOf(meters[i].user) === -1) {
              userids.push(meters[i].user);
            }
            if(usermiss[meters[i].user]) {
              usermiss[meters[i].user] += 1;
            } else {
              usermiss[meters[i].user] = 1;
            }

            meters[i].missedPeriods.push(theperiod._id);
            meters[i].save();
            theperiod.missedMeters.push(meters[i]._id);
            theperiod.save();
          }

          for(i = 0, len = userids.length; i < len; i++) {
            User.findOne({ '_id': userids[i] }, function(err, user) {
              tosend = '';
              if (err) next(err);

              tosend = 'Dear ' + user.salutation + ' ' + user.lastname +
                ', the reporting window from ' + theperiod.startDate.toDateString() + ' to ' +
                theperiod.endDate.toDateString() + ' has closed. Unfortunately we did not ' +
                'receive a report for all of your meters from you and thus cannot reward you fully. We hope that you ' +
                'will be able to submit a report next month. Please text \'HELP\' ' +
                'if you wish to speak to us via phone, or call directly at XXX-XXX-XXXX ' +
                'or email us at GAwaterreporting@h2opolicycenter.org';

              if(user.contractType === 'C') {
                user.bank -= (usermiss[users._id] * m.C.reportamt);
              } else if(user.contractType === 'D') {
                user.bank -= (usermiss[users._id] * m.C.reportamt);
              }

              user.save();
              sendMessage(err, tosend, user.number);
            });
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
